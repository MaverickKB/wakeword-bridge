#!/usr/bin/env python3
import asyncio, os, socket, sys, traceback
import paho.mqtt.client as mqtt
from wyoming.client import AsyncClient
from wyoming.audio import AudioChunk
from wyoming.event import Event

# ─── Config from env ──────────────────────────────────────────────
MQTT_HOST = os.getenv("MQTT_HOST", "homeassistant")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
SITE_ID = os.getenv("SITE_ID", "nspanel")

UDP_PORT = int(os.getenv("UDP_PORT", "12202"))
WYOMING_HOST = os.getenv("WYOMING_HOST", "127.0.0.1")
WYOMING_PORT = int(os.getenv("WYOMING_PORT", "10400"))
# ─────────────────────────────────────────────────────────────────

async def main() -> None:
    # MQTT
    mqtt_client = mqtt.Client()
    if MQTT_USER or MQTT_PASSWORD:
        mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_HOST, MQTT_PORT, 30)
    mqtt_client.loop_start()

    # UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", UDP_PORT))
    sock.setblocking(False)
    print(f"[bridge] UDP listener bound to :{UDP_PORT}", flush=True)

    while True:
        try:
            audio, _ = await asyncio.get_event_loop().sock_recvfrom(sock, 4096)
            async with AsyncClient(host=WYOMING_HOST, port=WYOMING_PORT) as wy:
                await wy.write_event(AudioChunk(audio, 16000, 2, 1).event())
                event: Event | None = await wy.read_event()
                if event and event.type == "detection":
                    name = event.payload.get("name", "wakeword")
                    print(f"[bridge] Wake-word detected: {name}", flush=True)
                    mqtt_client.publish(
                        f"hermes/hotword/{SITE_ID}/detected",
                        payload=f'{{"model":"{name}"}}',
                        qos=0,
                        retain=False,
                    )
        except Exception as err:
            traceback.print_exception(err, file=sys.stderr)
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
