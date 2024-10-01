cat <<EOF >> /etc/vsftpd.conf
listen_port=$FTP_PORT
listen_address=$FTP_HOST
EOF

nohup vsftpd > /tmp/vsftpd_std_out 2>&1 &
