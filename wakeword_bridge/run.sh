#!/usr/bin/env bash

# Load bashio config parser
source /usr/lib/bashio/bashio.sh

export MQTT_HOST=$(bashio::config 'mqtt_host')
export MQTT_PORT=$(bashio::config 'mqtt_port')
export MQTT_USERNAME=$(bashio::config 'mqtt_username')
export MQTT_PASSWORD=$(bashio::config 'mqtt_password')
export SITE_ID=$(bashio::config 'site_id')

echo "Starting Wake Word Bridge for site: $SITE_ID"
python3 /udp_to_wyoming_bridge.py
