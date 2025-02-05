#!/bin/bash

for file in /entrypoints/*; do
    if [ -f "$file" ]; then
        echo "$file"
        chmod +x $file
        $file
    fi
done

echo "All entrypoints executed!"

exec "$@"
