FROM base AS ftp

ARG FTP_PORT=21
ARG FTP_HOST=0.0.0.0

ENV FTP_PORT=${FTP_PORT}
ENV FTP_HOST=${FTP_HOST}

RUN apt update && apt install -y \
    vsftpd \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoints

RUN sed -i 's/listen=NO/listen=YES/g' /etc/vsftpd.conf
RUN sed -i 's/listen_ipv6=YES/listen_ipv6=NO/g' /etc/vsftpd.conf
