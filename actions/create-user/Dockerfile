FROM base AS create_user

ARG USER_NAME=user
ARG USER_PASSWORD=user
ARG USER_GROUPS=""

COPY check-groups.sh /tmp/actions/create-user/

RUN useradd --password $(openssl passwd -1 $USER_PASSWORD) --shell /bin/bash --user-group --create-home $USER_NAME $(/tmp/actions/create-user/check-groups.sh)

COPY entrypoint.sh /entrypoints
