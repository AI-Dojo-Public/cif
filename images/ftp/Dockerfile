FROM base AS ftp

ENV FTP_PORT=21
ENV FTP_HOST=127.0.0.1

RUN apt update && apt install -y \
    vsftpd \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoints

RUN sed -i 's/listen=NO/listen=YES/g' /etc/vsftpd.conf
RUN sed -i 's/listen_ipv6=YES/listen_ipv6=NO/g' /etc/vsftpd.conf
