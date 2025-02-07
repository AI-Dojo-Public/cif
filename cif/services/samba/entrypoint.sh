#!/bin/bash

cat <<EOF >> /etc/samba/smb.conf
[sambashare]
    comment = Samba on Ubuntu
    path = /sambashare
    writable = yes
    browsable = yes
    public = yes
    create mask = 0644
    directory mask = 2777
EOF

service smbd restart
