# Ansible Role: docker_login

Manages Docker registry authentication for pulling from private registries.

## Features

- **Registry Authentication**: Login to Docker registries (Docker Hub, GHCR, private registries)
- **Multiple Registries**: Support for multiple registry authentications
- **Secure Credentials**: Handle credentials securely via Ansible Vault
- **User-Scoped**: Per-user Docker configuration
- **Validation**: Verify authentication after login

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/container/docker_login_role.html](https://guide.arillso.io/collections/arillso/container/docker_login_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.container.docker_login
        vars:
            docker_login_registries:
                - registry: ghcr.io
                  username: myuser
                  password: "{{ vault_ghcr_token }}"
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
