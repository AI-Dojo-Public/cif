cat <<EOF >> /etc/ssh/sshd_config
PasswordAuthentication yes
ChallengeResponseAuthentication yes
ListenAddress $SSH_HOST:$SSH_PORT
EOF

service ssh restart
