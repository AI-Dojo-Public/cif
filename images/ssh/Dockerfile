FROM base AS ssh

ENV SSH_PORT=22
ENV SSH_HOST=127.0.0.1

RUN apt update && apt install -y openssh-server # sudo

COPY entrypoint.sh /entrypoints

#RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 test
#RUN  echo 'test:test' | chpasswd
