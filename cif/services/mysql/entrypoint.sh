#!/bin/bash

mysqld -D --port=$MYSQL_PORT --bind-address=$MYSQL_HOST

for file in /tmp/mysql/*.sql; do
    if [ -f "$file" ]; then
        echo "importing $file"
        mysql < $file
    fi
done

echo "All files imported!"
