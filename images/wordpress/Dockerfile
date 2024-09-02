FROM base AS wordpress

RUN apt update && apt install -y wget php unzip

RUN wget https://wordpress.org/latest.zip

ENV WP_HOSTNAME=wordpress_node
ENV WP_ADMIN_NAME=wordpress
ENV WP_ADMIN_PASSWORD=wordpress

#apt install php-mysql

#export DB_NAME=wordpress
#root@d3fbc8d7d6c5:/# export DB_USER=wordpress
#root@d3fbc8d7d6c5:/# export DB_PASSWORD=wordpress
#root@d3fbc8d7d6c5:/# export DB_HOST=127.0.0.1

# TODO: add database setup

RUN wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
    chmod +x wp-cli.phar && \
    mv wp-cli.phar /usr/local/bin/wp

#COPY --chown=www-data:www-data --chmod=700 docker/entrypoint.sh /tmp/entrypoint.sh
#COPY docker/index.php /usr/src/wordpress/index.php
COPY wp-config.php /wordpress/wp-config.php

# wp core install --path=/wordpress/ --url=http://$WP_HOSTNAME --title=CDRI --admin_name=$WP_ADMIN_NAME --admin_password=$WP_ADMIN_PASSWORD --admin_email=admin@mail.cdri --allow-root

# service apache2 restart
