echo "ListenAddress $SSH_HOST:$SSH_PORT" >> /etc/ssh/sshd_config

service ssh restart
