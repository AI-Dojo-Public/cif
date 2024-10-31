mysqld -D --port=$MYSQL_PORT --bind-address=$MYSQL_HOST

# WordPress setup
mysql --execute "CREATE DATABASE wordpress; CREATE USER 'wordpress'@'%' IDENTIFIED BY 'wordpress'; GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpress'@'%'; FLUSH PRIVILEGES;"
