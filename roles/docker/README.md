# Ansible Role: docker

Installs and configures Docker Engine with support for custom daemon configuration, systemd integration, and automated cleanup tasks.

## Features

- **Docker Installation**: Install Docker Engine from official repositories
- **Daemon Configuration**: Customize Docker daemon settings (logging, registry mirrors, etc.)
- **Systemd Integration**: Manage Docker service and custom systemd units
- **Automated Cleanup**: Configure scheduled prune tasks for containers, images, and volumes
- **Multi-Distribution**: Support for Debian, Ubuntu, RHEL, and derivatives

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/container/docker_role.html](https://guide.arillso.io/collections/arillso/container/docker_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.container.docker
        vars:
            docker_daemon:
                log-driver: journald
                live-restore: true
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
