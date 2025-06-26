#!/usr/bin/env bashio
bashio::log.info "Starting Wake Word Bridge..."
# Read options: e.g., PORT=$(bashio::config 'port')
python3 /udp_to_wyoming_bridge.py
