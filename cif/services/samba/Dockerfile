FROM base AS samba

ARG SAMBA_PORT=139
ARG SAMBA_PORT_AD=445
ARG SAMBA_HOST=0.0.0.0

ENV SAMBA_PORT=${SAMBA_PORT}
ENV SAMBA_PORT_AD=${SAMBA_PORT_AD}
ENV SAMBA_HOST=${SAMBA_HOST}

RUN apt update && apt install -y \
    samba \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /sambashare -m 777

COPY entrypoint.sh /entrypoints
