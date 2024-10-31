FROM base AS wordpress

RUN apt update && apt install -y \
    wget \
    php \
    unzip \
    php-mysql \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://wordpress.org/latest.zip
RUN unzip latest.zip
RUN mv /wordpress/* /var/www/html/

ARG WORDPRESS_HOSTNAME=0.0.0.0
ARG WORDPRESS_ADMIN_NAME=wordpress
ARG WORDPRESS_ADMIN_PASSWORD=wordpress
ARG WORDPRESS_DB_USER=wordpress
ARG WORDPRESS_DB_PASSWORD=wordpress
ARG WORDPRESS_DB_HOST=127.0.0.1
ARG WORDPRESS_DEBUG=false
ARG WORDPRESS_CERTIFICATE="/"
ARG WORDPRESS_PRIVATE_KEY="/"
ARG WORDPRESS_HOST=0.0.0.0
ARG WORDPRESS_PORT=80
ARG WORDPRESS_TITLE=Placeholder

ENV WORDPRESS_HOSTNAME=${WORDPRESS_HOSTNAME}
ENV WORDPRESS_ADMIN_NAME=${WORDPRESS_ADMIN_NAME}
ENV WORDPRESS_ADMIN_PASSWORD=${WORDPRESS_ADMIN_PASSWORD}
ENV WORDPRESS_DB_USER=${WORDPRESS_DB_USER}
ENV WORDPRESS_DB_PASSWORD=${WORDPRESS_DB_PASSWORD}
ENV WORDPRESS_DB_HOST=${WORDPRESS_DB_HOST}
ENV WORDPRESS_DEBUG=${WORDPRESS_DEBUG}
ENV WORDPRESS_CERTIFICATE=${WORDPRESS_CERTIFICATE}
ENV WORDPRESS_PRIVATE_KEY=${WORDPRESS_PRIVATE_KEY}
ENV WORDPRESS_HOST=${WORDPRESS_HOST}
ENV WORDPRESS_PORT=${WORDPRESS_PORT}
ENV WORDPRESS_TITLE=${WORDPRESS_TITLE}

RUN wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
    chmod +x wp-cli.phar && \
    mv wp-cli.phar /usr/local/bin/wp

COPY wp-config.php /var/www/html/
COPY docker-php.conf /etc/apache2/conf-available/

RUN a2dismod mpm_event && a2enmod mpm_prefork
RUN a2enconf docker-php

COPY entrypoint.sh /entrypoints

# https://github.com/docker-library/wordpress/blob/5bbbfa8909232af10ea3fea8b80302a6041a2d04/latest/php8.0/apache/
# https://github.com/docker-library/php/blob/master/8.3/bookworm/apache/
