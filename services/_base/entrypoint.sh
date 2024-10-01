#!/bin/bash

for file in /entrypoints/*; do
    if [ -f "$file" ]; then
        echo "$file"
        /bin/bash $file
    fi
done

echo "All entrypoints executed!"

exec "$@"
