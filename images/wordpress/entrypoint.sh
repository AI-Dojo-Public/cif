# TODO: needs a better solution?
echo "export WORDPRESS_DB_USER=$WORDPRESS_DB_USER" >> /etc/apache2/envvars
echo "export WORDPRESS_DB_PASSWORD=$WORDPRESS_DB_PASSWORD" >> /etc/apache2/envvars
echo "export WORDPRESS_DB_HOST=$WORDPRESS_DB_HOST" >> /etc/apache2/envvars
echo "export WORDPRESS_DEBUG=$WORDPRESS_DEBUG" >> /etc/apache2/envvars

wp core install --path=/var/www/html/ --url=http://$WORDPRESS_HOSTNAME --title=CDRI --admin_name=$WORDPRESS_ADMIN_NAME --admin_password=$WORDPRESS_ADMIN_PASSWORD --admin_email=admin@example.com --allow-root

service apache2 restart
# TODO add port /etc/apache2/ports.conf
# TODO https://httpd.apache.org/docs/2.4/bind.html - change ports; must be done in entrypoint/on startup due to firehole