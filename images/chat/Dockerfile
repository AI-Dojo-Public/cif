FROM base as production

ARG CHAT_HOST=0.0.0.0
ARG CHAT_PORT=80

ENV CHAT_HOST=${CHAT_HOST}
ENV CHAT_PORT=${CHAT_PORT}

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