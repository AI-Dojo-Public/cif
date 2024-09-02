FROM base AS wordpress

RUN apt update && apt install -y wget php unzip php-mysql

RUN wget https://wordpress.org/latest.zip
RUN unzip latest.zip
RUN mv /wordpress/* /var/www/html/

ENV WP_HOSTNAME=wordpress_node
ENV WP_ADMIN_NAME=wordpress
ENV WP_ADMIN_PASSWORD=wordpress
ENV WORDPRESS_DB_USER=wordpress
ENV WORDPRESS_DB_PASSWORD=wordpress
ENV WORDPRESS_DB_HOST=127.0.0.1

RUN wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
    chmod +x wp-cli.phar && \
    mv wp-cli.phar /usr/local/bin/wp

COPY wp-config.php /wordpress/wp-config.php

RUN wp core install --path=/wordpress/ --url=http://$WP_HOSTNAME --title=CDRI --admin_name=$WP_ADMIN_NAME --admin_password=$WP_ADMIN_PASSWORD --admin_email=admin@mail.cdri --allow-root
