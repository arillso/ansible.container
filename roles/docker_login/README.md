# Ansible Role: docker_login

Manages Docker registry authentication for pulling from private registries.

## Features

- **Registry Authentication**: Login to one Docker registry per role call (Docker Hub, GHCR, private registries)
- **Logout**: `docker_login_state: absent` removes the stored credentials
- **Credential Check**: Fails early when username or password is empty
- **Custom Config Path**: `docker_login_config_path` selects the Docker client config file

The role does not escalate privileges itself. The credentials land in the
config of the user the task runs as, so set `become` / `become_user` on the
play or role as needed.

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/container/docker_login_role.html](https://guide.arillso.io/collections/arillso/container/docker_login_role.html)**

## Quick Start

```yaml
- hosts: servers
  become: true
  roles:
      - role: arillso.container.docker_login
        vars:
            docker_login_registry_url: ghcr.io
            docker_login_username: myuser
            docker_login_password: "{{ vault_ghcr_token }}"
```

For several registries, include the role once per registry.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
