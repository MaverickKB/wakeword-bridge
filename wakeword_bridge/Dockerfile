ARG BUILD_FROM
FROM ${BUILD_FROM}

# Add Alpine packages
RUN apk add --no-cache bash curl jq

# Add bashio (for reading add-on options in run.sh)
RUN curl -Lso /tmp/install.sh https://raw.githubusercontent.com/hassio-addons/bashio/master/install.sh \
 && bash /tmp/install.sh \
 && rm /tmp/install.sh

# Python deps
RUN pip install --no-cache-dir paho-mqtt wyoming

# Copy add-on files
COPY run.sh /
COPY udp_to_wyoming_bridge.py /

RUN chmod +x /run.sh

CMD [ "/run.sh" ]
