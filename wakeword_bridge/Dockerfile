ARG BUILD_FROM
FROM $BUILD_FROM

# Install bash and tools
RUN apk add --no-cache bash curl jq \
    && pip install --no-cache-dir paho-mqtt wyoming

COPY run.sh /run.sh
COPY udp_to_wyoming_bridge.py /udp_to_wyoming_bridge.py

RUN chmod +x /run.sh

CMD [ "/run.sh" ]
