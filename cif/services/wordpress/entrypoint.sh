#!/bin/bash

cat <<EOF >> /etc/apache2/envvars
export WORDPRESS_DB_USER=$WORDPRESS_DB_USER
export WORDPRESS_DB_PASSWORD=$WORDPRESS_DB_PASSWORD
export WORDPRESS_DB_HOST=$WORDPRESS_DB_HOST
export WORDPRESS_DEBUG=$WORDPRESS_DEBUG
EOF

if [ -f $WORDPRESS_CERTIFICATE ] && [ -f $WORDPRESS_PRIVATE_KEY ]; then
a2enmod ssl
APACHE_PROTOCOL=https
cat <<EOF > /etc/apache2/sites-available/000-default.conf
LoadModule ssl_module modules/mod_ssl.so

Listen $WORDPRESS_HOST:$WORDPRESS_PORT $APACHE_PROTOCOL
<VirtualHost *:$WORDPRESS_PORT>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html
    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined
    # ServerName www.example.com
    SSLEngine on
    SSLCertificateFile "$WORDPRESS_CERTIFICATE"
    SSLCertificateKeyFile "$WORDPRESS_PRIVATE_KEY"
</VirtualHost>

EOF

else
APACHE_PROTOCOL=http
cat <<EOF > /etc/apache2/sites-available/000-default.conf
Listen $WORDPRESS_HOST:$WORDPRESS_PORT $APACHE_PROTOCOL
<VirtualHost *:$WORDPRESS_PORT>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html
    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined
    # ServerName www.example.com
</VirtualHost>

EOF

fi

# Override Apache defined ports
cat <<EOF > /etc/apache2/ports.conf

EOF

#Wordpress
if [[ "$WORDPRESS_PORT" == 80 && "$APACHE_PROTOCOL" == "http" || "$WORDPRESS_PORT" == 443 && "$APACHE_PROTOCOL" == "https" ]]; then
  WORDPRESS_URL=$APACHE_PROTOCOL://$WORDPRESS_HOSTNAME
else
  WORDPRESS_URL=$APACHE_PROTOCOL://$WORDPRESS_HOSTNAME:$WORDPRESS_PORT
fi

wp core install --path=/var/www/html/ --url=$WORDPRESS_URL --title=$WORDPRESS_TITLE --admin_name=$WORDPRESS_ADMIN_NAME --admin_password=$WORDPRESS_ADMIN_PASSWORD --admin_email=admin@example.com --allow-root

service apache2 restart
# https://httpd.apache.org/docs/2.4/bind.html
# https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html
