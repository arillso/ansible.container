# arillso.container.docker

This Ansible role is designed for configuring and managing Docker environments using Ansible. It defines parameters for
setting up Docker on various distributions, allowing for a customized Docker experience.

## Requirements

- Ansible 2.915 or higher.
- Suitable access to target systems for Docker installation and configuration.

## Role Variables

The role uses various variables to customize Docker setup and behavior. These variables are defined in the `defaults/main.yml` file.
Users can override these default values in their playbook.

### Docker Configuration

- `docker_version`: Specifies the Docker version to install (default: latest).
- `docker_daemon`: A dictionary to define Docker daemon configurations, including options like `log-driver` (default: "journald"),
  `log-opts` (with options like `max-size`), `live-restore` (default: true), and `registry-mirrors`.

### Systemd Units for Docker

- `docker_systemd_units`: A list of systemd units for Docker pruning tasks, with options to specify the unit's name, type, and various systemd options.

## Dependencies

No other Ansible roles are required as dependencies.

## Example Playbook

An example playbook demonstrating the use of `arillso.container.docker` to set up Docker:

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
