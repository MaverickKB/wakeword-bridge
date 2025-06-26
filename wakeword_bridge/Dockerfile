ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
      bash curl jq python3 py3-pip

RUN curl -sL https://raw.githubusercontent.com/hassio-addons/bashio/master/install.sh | bash

RUN pip install --no-cache-dir paho-mqtt wyoming

COPY run.sh /run.sh
COPY udp_to_wyoming_bridge.py /udp_to_wyoming_bridge.py
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]