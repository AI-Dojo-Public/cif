FROM ubuntu:latest AS base

ENV DEBIAN_FRONTEND=noninteractive

COPY entrypoint.sh /entrypoint.sh

RUN mkdir /entrypoints

ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]
CMD [ "tail", "-f", "/dev/null" ]
