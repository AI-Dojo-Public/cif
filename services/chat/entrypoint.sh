# Create site config
cat <<EOF > /etc/apache2/sites-available/000-default.conf
Listen $CHAT_HOST:$CHAT_PORT http
<VirtualHost *:CHAT_PORT>
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
