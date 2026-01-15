# Ansible Role: k3s

Installs and configures K3s, a lightweight Kubernetes distribution optimized for edge, IoT, and resource-constrained environments.

## Features

- **K3s Installation**: Install K3s server and agent nodes
- **High Availability**: Support for HA control plane with embedded etcd
- **Cluster Configuration**: Configure cluster networking, storage, and ingress
- **Token Management**: Secure cluster join tokens
- **Systemd Integration**: Manage K3s as systemd service

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/container/k3s_role.html](https://guide.arillso.io/collections/arillso/container/k3s_role.html)**

## Quick Start

```yaml
- hosts: k3s_servers
  roles:
      - role: arillso.container.k3s
        vars:
            k3s_role: server
            k3s_server_config:
                cluster-init: true
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
