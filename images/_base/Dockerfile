FROM ubuntu:latest AS base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    iproute2 \
    iptables \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh

RUN mkdir /entrypoints

ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]
CMD [ "tail", "-f", "/dev/null" ]
