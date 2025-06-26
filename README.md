# 🗣 Wake Word Bridge Add-on for Home Assistant

**Wake Word Bridge** is a custom Home Assistant add-on that listens for microphone audio streamed over UDP (e.g., from Rhasspy Mobile or another satellite device), passes that audio to a locally running [openWakeWord](https://github.com/rhasspy/openWakeWord) server (Wyoming protocol), and triggers a wake word detection event using MQTT.

This provides a fully offline, low-latency alternative to cloud voice services — and forms the critical first step of a fully self-hosted voice assistant pipeline using openWakeWord, faster-whisper, and your preferred LLM backend.

---

## 🔧 Features

- ✅ Listens for raw PCM audio over UDP
- ✅ Sends audio to openWakeWord via Wyoming
- ✅ Publishes MQTT hotword events to `hermes/hotword/<site_id>/detected`
- ✅ Lightweight Python bridge packaged as an HA-native add-on
- ✅ Compatible with Home Assistant 2025.6.3+ add-on structure
- ✅ Supports MQTT credentials and multiple architectures

---

## 📦 Installation

### Add this repository to Home Assistant:

1. Open **Settings → Add-ons → Add-on Store**
2. Click the **⋮ (three-dot menu)** in the upper-right
3. Select **Repositories**
4. Add: https://github.com/MaverickKB/wakeword-bridge
5. Click **Add**, then scroll to the bottom to find **Wake Word Bridge**
6. Click **Install**, configure, and **Start**

---

## ⚙️ Configuration

In `config.yaml`, you may optionally define:

```yaml
mqtt_host: homeassistant
mqtt_port: 1883
mqtt_username: mqttuser
mqtt_password: yourpassword
site_id: nspanel

These are injected into the container as environment variables, then used by the Python bridge.

⸻

📡 Requirements
	•	openWakeWord must be running on localhost:10400 (Wyoming port)
	•	A client device (e.g., Rhasspy Mobile or ESP32 mic) must stream 16-bit PCM audio over UDP to port 12202
	•	MQTT broker must be available and reachable using the provided credentials

⸻

🔄 Pipeline Overview

[Mic] → Rhasspy Mobile (UDP out)
      → Wake Word Bridge (UDP listener) 
      → openWakeWord (Wyoming protocol)
      → MQTT broker
      → Home Assistant Pipeline

When the hotword is detected, the bridge publishes:
    hermes/hotword/<site_id>/detected

This triggers any HA Assist Pipeline or automation expecting a wake word event.

⸻

🧪 Debugging
	•	Use mosquitto_sub -v -t 'hermes/hotword/#' to observe messages
	•	Add-on logs will show:   
        Listening for UDP audio on port 12202...
        Wake word detected: hey_jarvis

🧠 Credits

Inspired by the Rhasspy and openWakeWord ecosystems.

Built and maintained by @MaverickKB as part of a custom Jarvis-style offline voice assistant system.

⸻

📜 License

MIT License. Use it, fork it, improve it — but don't blame me if none of this is easy. 😏
