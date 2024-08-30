#!/bin/bash

for file in *; do
    if [ -f "$file" ]; then
        echo "$file"
        /bin/bash $file
    fi
done

# todo add sleep and checks...
