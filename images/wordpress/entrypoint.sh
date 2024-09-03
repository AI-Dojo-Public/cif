wp core install --path=/var/www/html/ --url=http://$WORDPRESS_HOSTNAME --title=CDRI --admin_name=$WORDPRESS_ADMIN_NAME --admin_password=$WORDPRESS_ADMIN_PASSWORD --admin_email=admin@example.com --allow-root

service apache2 restart
# TODO add port /etc/apache2/ports.conf
