#!/bin/bash

# Set environment variables
cat <<EOF >> /etc/apache2/envvars
export TCHAT_DB_HOST=$TCHAT_DB_HOST
export TCHAT_DB_NAME=$TCHAT_DB_NAME
export TCHAT_DB_CHARSET=$TCHAT_DB_CHARSET
export TCHAT_DB_USER=$TCHAT_DB_USER
export TCHAT_DB_PASSWORD=$TCHAT_DB_PASSWORD
EOF

# Create site config
cat <<EOF > /etc/apache2/sites-available/000-default.conf
Listen $TCHAT_HOST:$TCHAT_PORT http
<VirtualHost *:$TCHAT_PORT>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html
    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined
    # ServerName www.example.com
</VirtualHost>

EOF

# Override Apache defined ports
cat <<EOF > /etc/apache2/ports.conf

EOF

# Restart apache server
service apache2 restart
