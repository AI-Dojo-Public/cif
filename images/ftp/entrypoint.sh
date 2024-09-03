echo "listen_port=$FTP_PORT" >> /etc/vsftpd.conf
echo "listen_address=$FTP_HOST" >> /etc/vsftpd.conf

nohup vsftpd > /tmp/vsftpd_std_out 2>&1 &
