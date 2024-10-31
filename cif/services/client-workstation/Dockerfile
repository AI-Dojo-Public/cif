FROM base AS workstation

RUN apt update && apt install -y \
    curl \
    wget \
    inetutils-ping \
    && rm -rf /var/lib/apt/lists/*
