FROM base AS vsftpd

ARG VSFTPD_PORT=21
ARG VSFTPD_HOST=0.0.0.0

ENV VSFTPD_PORT=${VSFTPD_PORT}
ENV VSFTPD_HOST=${VSFTPD_HOST}

RUN apt update && apt install -y \
    vsftpd \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoints

RUN sed -i 's/listen=NO/listen=YES/g' /etc/vsftpd.conf
RUN sed -i 's/listen_ipv6=YES/listen_ipv6=NO/g' /etc/vsftpd.conf
