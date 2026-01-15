# Ansible Role: docker_compose_v2

Installs and manages Docker Compose v2 (docker compose) as a Docker CLI plugin.

## Features

- **Docker Compose v2 Installation**: Install as Docker CLI plugin
- **Version Management**: Install specific versions or latest
- **Native Integration**: Integrated with Docker CLI (docker compose)
- **Performance**: Improved performance over v1
- **Modern Features**: Support for profiles, GPU, and other v2 features

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/container/docker_compose_v2_role.html](https://guide.arillso.io/collections/arillso/container/docker_compose_v2_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.container.docker_compose_v2
        vars:
            docker_compose_v2_version: "2.23.0"
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
