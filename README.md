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
cif -r registry.gitlab.ics.muni.cz:443/ai-dojo/cif -fc /tmp/firehole-config.yml -v WORDPRESS_HOSTNAME=127.0.0.1 -v WORDPRESS_HOST=127.0.0.1 -v WORDPRESS_PORT=8000 -v WORDPRESS_TITLE=asd firehole ftp mysql ssh wordpress
```

```shell
docker run --network host -it --rm registry.gitlab.ics.muni.cz:443/ai-dojo/cif/base_firehole_ftp_mysql_ssh_wordpress bash
```

Test http vulnerability:
```shell
curl localhost -H 'X-Host: test'
```

### Using action example
```shell
cif client-workstation client-developer -v CLIENT_DEVELOPER_DATABASE_USER=asd -v CLIENT_DEVELOPER_USER_NAME=asd -a create-user:USER_NAME=asd,USER_PASSWORD=asd -a create-user:USER_NAME=test,USER_PASSWORD=test
```

## Adding an image
Create a directory with a unique name in the `cif/images/` directory. Create `Dockerfile` and `entrypoint.sh` inside it.

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
