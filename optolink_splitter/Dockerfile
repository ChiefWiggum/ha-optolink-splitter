ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:3.21
FROM ${BUILD_FROM}

# Pinned upstream commit of philippoo66/optolink-splitter (main).
# To update: change the hash, bump 'version' in config.yaml, rebuild the add-on.
ARG SPLITTER_COMMIT=c1ee204a1421447721603c5f21c6da7337fdac97

RUN apk add --no-cache python3 py3-pip git \
    && pip3 install --no-cache-dir --break-system-packages \
        "pyserial>=3.5" \
        "paho-mqtt>=2.0,<3" \
    && git clone https://github.com/philippoo66/optolink-splitter.git /opt/optolink-splitter \
    && git -C /opt/optolink-splitter checkout ${SPLITTER_COMMIT} \
    && rm -rf /opt/optolink-splitter/.git \
    && apk del git

COPY run.sh /run.sh
COPY templates /opt/templates
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
