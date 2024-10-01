FROM base AS mysql

ARG MYSQL_PORT=3306
ARG MYSQL_HOST=0.0.0.0

ENV MYSQL_PORT=${MYSQL_PORT}
ENV MYSQL_HOST=${MYSQL_HOST}

RUN apt update && apt install -y \
    mysql-server \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoints
