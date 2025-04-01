# CIF

Custom Image Forge.

Its purpose is to build Docker images with the services and packages you define. You can also customize the final image with actions.  
The latest ubuntu image is used as a base. To make sure the final image is as specified, we remove the default configuration (e.g. the ubuntu user).

**Services**: A service is a service (as you would expect). It is a predefined Dockerfile with default settings. It can also be configured with environment variables. Each service can be specified once a build and the variables are shared.

**Actions**: An action can be anything. For example creation of a user account. It works on the same principles as a service, but you can run it multiple times with different variables (if not stated otherwise).

**Packages**: You can also specify additional packages to install. This is done with `apt`.

CIF can also deploy firehole alongside with the other services. You only need to specify its configuration file. Doing so will allow you to make the services vulnerable.

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
Firehole config:
```yaml
applications:
  - type: http
    host: 0.0.0.0
    port: 80
    origin_host: 127.0.0.1
    origin_port: 8000
    vulnerabilities:
      - CVE-2016-10073

```

```shell
cif \
  --service mysql \
  --service wordpress \
  --service firehole \
  --file /tmp/firehole-config.yml:/firehole-config.yml \
  --variable WORDPRESS_HOSTNAME=127.0.0.1 \
  --variable WORDPRESS_HOST=127.0.0.1 \
  --variable WORDPRESS_PORT=8000 \
  --variable WORDPRESS_TITLE=asd \
  my-image-tag

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
