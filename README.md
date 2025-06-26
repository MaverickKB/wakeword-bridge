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
