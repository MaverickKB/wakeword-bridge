FROM python:3.11-alpine

# Install bash, curl, jq
RUN apk add --no-cache bash curl jq

# Install bashio properly with bash, not sh
RUN curl -sL https://raw.githubusercontent.com/hassio-addons/bashio/master/install.sh -o /tmp/install.sh && \
    chmod +x /tmp/install.sh && \
    /bin/bash /tmp/install.sh

# Install Python deps
RUN pip install --no-cache-dir paho-mqtt wyoming

# Copy in scripts
COPY run.sh /run.sh
COPY udp_to_wyoming_bridge.py /udp_to_wyoming_bridge.py

# Make script executable
RUN chmod +x /run.sh

# Entry point
CMD ["/run.sh"]
