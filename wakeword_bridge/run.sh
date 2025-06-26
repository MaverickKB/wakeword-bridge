#!/usr/bin/with-contenv bashio
bashio::log.info "Starting Wake Word Bridge…"
bashio::config # to pull options
python3 /udp_to_wyoming_bridge.py