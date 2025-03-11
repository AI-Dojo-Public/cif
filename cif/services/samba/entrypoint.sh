#!/bin/bash

cat <<EOF > /etc/samba/smb.conf
[global]
EOF

if [ "$SAMBA_HOST" != "" ] && [ "$SAMBA_HOST" != "0.0.0.0" ]; then
cat <<EOF >> /etc/samba/smb.conf
interfaces = $SAMBA_HOST
bind interfaces only = yes
EOF
fi

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
