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
```shell
cif -r registry.gitlab.ics.muni.cz:443/ai-dojo/cif -fc /home/sad/dev/csirt/ai-dojo/firehole/config.yml -v WORDPRESS_HOSTNAME=127.0.0.1 -v WORDPRESS_HOST=127.0.0.1 -v WORDPRESS_PORT=8000 -v WORDPRESS_TITLE=asd firehole ftp mysql ssh wordpress
```

```shell
docker run --network host -it --rm registry.gitlab.ics.muni.cz:443/ai-dojo/cif/base_firehole_ftp_mysql_ssh_wordpress bash
```


## Adding an image
Create a directory with a unique name in the `cif/images/` directory. Create `Dockerfile` and `entrypoint.sh` inside it.

Entrypoint must contain a non-blocking script and will be executed at the startup.

The Dockerfile must contain the following:
```dockerfile
FROM base AS <service>

ENV <SERVICE>_PORT=6996
ENV <SERVICE>_HOST=127.0.0.1

COPY entrypoint.sh /entrypoints

```
