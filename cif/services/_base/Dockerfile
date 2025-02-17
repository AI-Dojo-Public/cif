FROM ubuntu:latest AS base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    openssl \
    iproute2 \
    iptables \
    && rm -rf /var/lib/apt/lists/*

RUN userdel ubuntu

COPY entrypoint.sh /entrypoint.sh

RUN mkdir --parents /entrypoints

ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]
CMD [ "tail", "-f", "/dev/null" ]
