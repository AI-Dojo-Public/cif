FROM base AS mysql

RUN apt update && apt install -y mysql-server

# Use -D for running it in the background
CMD ["mysqld"]
