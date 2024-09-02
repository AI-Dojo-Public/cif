mysqld -D --port=$MYSQL_PORT --host=$MYSQL_HOST

# WordPress setup
mysql --execute "CREATE DATABASE wordpress; CREATE USER 'wordpress'@'localhost' IDENTIFIED BY 'wordpress'; GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpress'@'localhost'; FLUSH PRIVILEGES;"
