# CIF

Custom Image Forge

## Installation
Requires Python >=3.11, [pipx](https://pipx.pypa.io/latest/installation/), and [Docker](https://docs.docker.com/engine/install/).

Install the project using:
```shell
pipx install cif --index-url https://gitlab.ics.muni.cz/api/v4/projects/7197/packages/pypi/simple
```

## Usage
```shell
cif -h
```

### Example
FireHole config:
```yaml
applications:
  - type: http_s
    host: 0.0.0.0
    port: 80
    origin_host: 127.0.0.1
    origin_port: 8000
    vulnerabilities:
      - CVE-2016-10073

```

```shell
cif \
  --firehole-config /tmp/firehole-config.yml \
  --tag my-image-tag \
  --variable WORDPRESS_HOSTNAME=127.0.0.1 \
  --variable WORDPRESS_HOST=127.0.0.1 \
  --variable WORDPRESS_PORT=8000 \
  --variable WORDPRESS_TITLE=asd \
  mysql wordpress

```

```shell
docker run --network host -it --rm my-image-tag bash
```

Test http vulnerability:
```shell
curl localhost -H 'X-Host: test'
```

## Adding a service
Create a directory with a unique name in the `cif/services/` directory. Create `Dockerfile` and `entrypoint.sh` inside it.

Entrypoint must contain a non-blocking script and will be executed at the startup.

The Dockerfile must contain the following:
```dockerfile
FROM base AS <service>

ARG <SERVICE>_PORT=22
ARG <SERVICE>_HOST=0.0.0.0

ENV <SERVICE>_PORT=${<SERVICE>_PORT}
ENV <SERVICE>_HOST=${<SERVICE>_HOST}

COPY entrypoint.sh /entrypoints

```

## Adding an action
Same as an image. The only difference is that you need to create it in the `cif/actions/` directory.
