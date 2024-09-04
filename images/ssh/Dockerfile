FROM base AS ssh

ENV SSH_PORT=22
ENV SSH_HOST=127.0.0.1

RUN apt update && apt install -y \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoints
