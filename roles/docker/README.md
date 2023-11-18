# arillso.container.docker

This Ansible role is designed for the configuration and management of Docker environments.
It offers tailored parameters for setting up Docker across various distributions, enabling a customized Docker experience.

## Requirements

- **Ansible Version**: 2.15 or higher
- **Access**: Adequate permissions for Docker installation and configuration on target systems

## Role Variables

Variables for customizing Docker setup are defined in `defaults/main.yml`. Users can override these in their playbook. Key variables include:

### Docker Configuration

- `docker_version`: Docker version to install (default: latest)
- `docker_daemon`: Configuration dictionary for Docker daemon, including:
  - `log-driver` (default: "journald")
  - `log-opts` with options like `max-size`
  - `live-restore` (default: true)
  - `registry-mirrors`

### Systemd Units for Docker

- `docker_systemd_units`: List of systemd units for Docker pruning tasks. Includes options for unit's name, type, and various systemd settings.

## Documentation

For detailed information and advanced usage, refer to our guide:

[Arillso Docker Guide](https://guide.arillso.io/collections/arillso/container/docker.html#ansible-collections-arillso-container-docker-role)

## Dependencies

This role is standalone and does not require other Ansible roles as dependencies.

## Example Playbook

Example playbook for using `arillso.container.docker`:

```yaml
- hosts: all
  become: yes
  roles:
    - arillso.container.docker
  vars:
    docker_version: "20.10.5"
    docker_daemon:
      log-driver: "json-file"
      log-opts:
        max-size: "500m"
```
