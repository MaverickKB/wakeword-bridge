#!/usr/bin/env bash
set -e

# shellcheck disable=SC1091
source /usr/lib/bashio/bashio.sh

MQTT_HOST=$(bashio::config 'mqtt_host')
MQTT_PORT=$(bashio::config 'mqtt_port')
MQTT_USER=$(bashio::config 'mqtt_username')
MQTT_PASS=$(bashio::config 'mqtt_password')
SITE_ID=$(bashio::config 'site_id')

exec python3 /udp_to_wyoming_bridge.py \
     --host "$MQTT_HOST" --port "$MQTT_PORT" \
     --username "$MQTT_USER" --password "$MQTT_PASS" \
     --site-id "$SITE_ID"
