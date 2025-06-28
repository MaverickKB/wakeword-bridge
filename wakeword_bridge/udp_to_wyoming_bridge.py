#!/usr/bin/env python3
"""
UDP-to-Wyoming wake-word bridge for Home-Assistant add-on.
‣ Listens for 16-bit/16 kHz mono PCM packets on UDP 12202
‣ Streams each packet to an openWakeWord Wyoming server (default 127.0.0.1:10400)
‣ When it receives a “detection” event, publishes
      hermes/hotword/<site_id>/detected
"""

import asyncio
import os
import socket
import sys
import traceback

import paho.mqtt.client as mqtt
from wyoming.client import AsyncClient
from wyoming.audio import AudioChunk
from wyoming.event import Event

# ─── Config from env (set by run.sh / Bashio) ──────────────────────────────────
MQTT_HOST = os.getenv("MQTT_HOST", "homeassistant")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
SITE_ID = os.getenv("SITE_ID", "nspanel")

UDP_PORT = int(os.getenv("UDP_PORT", "12202"))
WYOMING_HOST = os.getenv("WYOMING_HOST", "127.0.0.1")
WYOMING_PORT = int(os.getenv("WYOMING_PORT", "10400"))
# ───────────────────────────────────────────────────────────────────────────────


async def main() -> None:
    # ── MQTT client (loop in background thread) ────────────────────────────────
    mqtt_client = mqtt.Client()
    if MQTT_USER or MQTT_PASSWORD:
        mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_HOST, MQTT_PORT, keepalive=30)
    mqtt_client.loop_start()

    # ── UDP listener socket (non-blocking) ────────────────────────────────────
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", UDP_PORT))
    sock.setblocking(False)
    print(f"[bridge] UDP listener bound to :{UDP_PORT}", flush=True)

    while True:
        try:
            audio_bytes, _ = await asyncio.get_event_loop().sock_recvfrom(sock, 4096)

            async with AsyncClient(host=WYOMING_HOST, port=WYOMING_PORT) as wy_client:
                chunk = AudioChunk(
                    audio=audio_bytes, rate=16000, width=2, channels=1
                )
                await wy_client.write_event(chunk.event())

                # Read a single response; many packets may stream before detection
                response: Event | None = await wy_client.read_event()
                if response and response.type == "detection":
                    name = response.payload.get("name", "wakeword")
                    print(f"[bridge] Wake-word detected: {name}", flush=True)

                    mqtt_client.publish(
                        f"hermes/hotword/{SITE_ID}/detected",
                        payload=f'{{"model":"{name}"}}',
                        qos=0,
                        retain=False,
                    )

        except Exception as err:
            # Log & continue (keeps add-on container alive)
            traceback.print_exception(err, file=sys.stderr)
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
