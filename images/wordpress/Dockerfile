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

ENV WORDPRESS_HOSTNAME=127.0.0.1
ENV WORDPRESS_ADMIN_NAME=wordpress
ENV WORDPRESS_ADMIN_PASSWORD=wordpress
ENV WORDPRESS_DB_USER=wordpress
ENV WORDPRESS_DB_PASSWORD=wordpress
ENV WORDPRESS_DB_HOST=127.0.0.1
ENV WORDPRESS_DEBUG=false

RUN wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
    chmod +x wp-cli.phar && \
    mv wp-cli.phar /usr/local/bin/wp

COPY wp-config.php /var/www/html/
COPY docker-php.conf /etc/apache2/conf-available/

RUN a2dismod mpm_event && a2enmod mpm_prefork
RUN a2enconf docker-php

# TODO: needs a better solution?
RUN echo "export WORDPRESS_DB_USER=$WORDPRESS_DB_USER" >> /etc/apache2/envvars
RUN echo "export WORDPRESS_DB_PASSWORD=$WORDPRESS_DB_PASSWORD" >> /etc/apache2/envvars
RUN echo "export WORDPRESS_DB_HOST=$WORDPRESS_DB_HOST" >> /etc/apache2/envvars
RUN echo "export WORDPRESS_DEBUG=$WORDPRESS_DEBUG" >> /etc/apache2/envvars

COPY entrypoint.sh /entrypoints

# https://github.com/docker-library/wordpress/blob/5bbbfa8909232af10ea3fea8b80302a6041a2d04/latest/php8.0/apache/
# https://github.com/docker-library/php/blob/master/8.3/bookworm/apache/
