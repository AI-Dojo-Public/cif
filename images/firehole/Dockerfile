FROM base AS firehole

RUN apt update && apt install -y \
    python3 \
    pipx \
    && rm -rf /var/lib/apt/lists/*

RUN pipx install firehole --index-url https://gitlab.ics.muni.cz/api/v4/projects/6823/packages/pypi/simple

COPY entrypoint.sh /entrypoints
