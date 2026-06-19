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

## Troubleshooting

- **Docker service does not start after a config change**: an invalid
  `docker_daemon` value writes a malformed `/etc/docker/daemon.json`. Validate
  the daemon config (`dockerd --validate` or `docker info`) and check
  `journalctl -u docker` for the parse error.
- **Logs grow without bound or rotation is ignored**: confirm the log driver
  and its `log-opts` are set under `docker_daemon` and that the chosen driver
  actually supports the options you provided.
- **Repository or GPG key errors during install**: ensure the host distribution
  is one of the supported platforms (see `meta/main.yml`) and that the official
  Docker apt/yum repository is reachable from the host.

For detailed guidance see <https://guide.arillso.io>.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
