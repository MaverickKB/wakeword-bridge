ARG BUILD_FROM
FROM ${BUILD_FROM}

# Alpine user-space tools you actually need
RUN apk add --no-cache bash curl jq

# ─── Bashio is pre-installed in the base image ───
# - remove the broken curl line entirely
# RUN curl …bashio…install.sh   ←  DELETE

# Python deps
RUN pip install --no-cache-dir paho-mqtt wyoming

COPY run.sh /
COPY udp_to_wyoming_bridge.py /
RUN chmod +x /run.sh

CMD ["/run.sh"]
