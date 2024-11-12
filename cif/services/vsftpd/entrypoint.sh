cat <<EOF >> /etc/vsftpd.conf
listen_port=$VSFTPD_PORT
listen_address=$VSFTPD_HOST
EOF

nohup vsftpd > /tmp/vsftpd_std_out 2>&1 &
