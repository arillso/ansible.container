# Ansible Role: docker

Installs and configures Docker Engine with support for custom daemon configuration, systemd integration, and automated cleanup tasks.

## Features

- **Docker Installation**: Install Docker Engine from official repositories
- **Daemon Configuration**: Customize Docker daemon settings (logging, registry mirrors, etc.), merged onto secure role defaults
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
            # Merged on top of the role defaults, not a replacement.
            docker_daemon:
                log-driver: json-file
                log-opts:
                    max-size: "10m"
                    max-file: "3"
```

### Daemon configuration merge

`/etc/docker/daemon.json` is rendered from `docker_daemon_base` recursively
merged with `docker_daemon`:

- `docker_daemon_base` holds the role defaults (`log-driver: journald`,
  `live-restore: true`, `no-new-privileges: true`).
- `docker_daemon` is the user hook and defaults to `{}`. Keys set here win;
  keys left unset are inherited from the base.

The merge is recursive, so a nested dict such as `log-opts` merges per sub-key
instead of being replaced wholesale. To drop a base key rather than override
it, replace `docker_daemon_base` itself.

## Hardening

- **`no-new-privileges: true` is enabled by default.** Containers can no longer
  gain privileges through setuid/setgid binaries. This breaks images that rely
  on them (for example `sudo` or `ping` in some base images). Opt out with:

    ```yaml
    docker_daemon:
        no-new-privileges: false
    ```

- **`userns-remap` is opt-in.** The role sets no default because enabling user
  namespace remapping has real costs: bind mounts need host UIDs matching the
  remapped range, `--privileged` containers and namespace sharing
  (`--userns=host` aside) stop working, and existing images and volumes may
  need re-chowning. Enable it deliberately:

    ```yaml
    docker_daemon:
        userns-remap: "default"
    ```

## Troubleshooting

- **Docker service does not start after a config change**: an invalid
  `docker_daemon` value writes a malformed `/etc/docker/daemon.json`. Validate
  the daemon config (`dockerd --validate` or `docker info`) and check
  `journalctl -u docker` for the parse error.
- **Logs grow without bound or rotation is ignored**: the default log driver is
  `journald`, which does **not** support `max-size`/`max-file` — those are
  `json-file` options and are silently ignored under `journald`. Journald
  enforces its own limits via `SystemMaxUse` in `journald.conf`, which this role
  does not manage. For per-container rotation owned by Docker, switch drivers:

    ```yaml
    docker_daemon:
        log-driver: json-file
        log-opts:
            max-size: "10m"
            max-file: "3"
    ```

- **Repository or GPG key errors during install**: ensure the host distribution
  is one of the supported platforms (see `meta/main.yml`) and that the official
  Docker apt/yum repository is reachable from the host.

For detailed guidance see <https://guide.arillso.io>.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
