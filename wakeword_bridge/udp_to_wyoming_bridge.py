
import socket
import asyncio
import struct
import paho.mqtt.client as mqtt
from wyoming.client import AsyncClient
from wyoming.audio import AudioChunk
from wyoming.event import Event
from wyoming.wake import WakeWordDetected
import os

MQTT_HOST = os.getenv("MQTT_HOST", "homeassistant")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
SITE_ID = os.getenv("SITE_ID", "nspanel")

UDP_PORT = 12202
WYOMING_HOST = "127.0.0.1"
WYOMING_PORT = 10400
WAKEWORD_MODEL = "hey_jarvis"

async def detect_wakeword():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
    mqtt_client.loop_start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", UDP_PORT))
    sock.setblocking(False)

    print(f"Listening for UDP audio on port {UDP_PORT}...")

    while True:
        try:
            audio_data, _ = await asyncio.get_event_loop().sock_recvfrom(sock, 4096)

            async with AsyncClient(host=WYOMING_HOST, port=WYOMING_PORT) as client:
                chunk = AudioChunk(audio=audio_data, rate=16000, width=2, channels=1)
                await client.write_event(chunk.event())

                # Read response from openWakeWord
                response = await client.read_event()
                if response and isinstance(response.payload, WakeWordDetected):
                    print(f"Wake word detected: {response.payload.model}")
                    mqtt_client.publish(
                        f"hermes/hotword/{SITE_ID}/detected",
                        payload='{"model": "' + response.payload.model + '"}',
                        qos=0,
                        retain=False
                    )
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(detect_wakeword())
