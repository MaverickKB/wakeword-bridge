FROM python:3.11-alpine

# Install bash, curl (for bashio install), and any other dependencies
RUN apk add --no-cache bash curl jq

# Install bashio (for reading config values in run.sh)
RUN curl -sL https://raw.githubusercontent.com/hassio-addons/bashio/master/install.sh | bash

# Install Python dependencies
RUN pip install --no-cache-dir paho-mqtt wyoming

# Copy in your scripts
COPY run.sh /run.sh
COPY udp_to_wyoming_bridge.py /udp_to_wyoming_bridge.py

# Make sure run.sh is executable
RUN chmod +x /run.sh

# Set default command
CMD ["/run.sh"]
