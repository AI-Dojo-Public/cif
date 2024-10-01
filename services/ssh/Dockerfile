FROM base AS ssh

ARG SSH_PORT=22
ARG SSH_HOST=0.0.0.0

ENV SSH_PORT=${SSH_PORT}
ENV SSH_HOST=${SSH_HOST}

RUN apt update && apt install -y \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoints
