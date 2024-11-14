FROM base as production

ARG TCHAT_HOST=0.0.0.0
ARG TCHAT_PORT=80
ARG TCHAT_DB_HOST=127.0.0.1
ARG TCHAT_DB_NAME=tchat
ARG TCHAT_DB_CHARSET=utf8mb4
ARG TCHAT_DB_USER=tchat
ARG TCHAT_DB_PASSWORD=tchat


ENV TCHAT_HOST=${TCHAT_HOST}
ENV TCHAT_PORT=${TCHAT_PORT}
ENV TCHAT_DB_HOST=${TCHAT_DB_HOST}
ENV TCHAT_DB_NAME=${TCHAT_DB_NAME}
ENV TCHAT_DB_CHARSET=${TCHAT_DB_CHARSET}
ENV TCHAT_DB_USER=${TCHAT_DB_USER}
ENV TCHAT_DB_PASSWORD=${TCHAT_DB_PASSWORD}

RUN apt update && apt install -y \
    wget \
    php \
    unzip \
    php-pdo \
    php-pdo-mysql \
    && rm -rf /var/lib/apt/lists/*

COPY app/ /var/www/html/

COPY docker-php.conf /etc/apache2/conf-available/

RUN a2dismod mpm_event && a2enmod mpm_prefork
RUN a2enconf docker-php

COPY entrypoint.sh /entrypoints