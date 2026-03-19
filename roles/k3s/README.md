# Ansible Role: k3s

Installs and configures K3s, a lightweight Kubernetes distribution optimized for edge, IoT, and resource-constrained environments.

## Features

- **K3s Installation**: Install K3s server and agent nodes
- **High Availability**: Support for HA control plane with embedded etcd
- **Cluster Configuration**: Configure cluster networking, storage, and ingress
- **Token Management**: Secure cluster join tokens
- **Systemd Integration**: Manage K3s as systemd service
- **Upgrade Management**: Controlled upgrades with upgrade path validation

## Upgrading K3s

To upgrade k3s, update the `k3s_version` variable and re-run the role. The role will automatically detect the version change and replace the binary.

```yaml
k3s_version: "v1.30.2+k3s1"
```

### Upgrade Path Rules

The role enforces the following constraints:

- **One minor version at a time**: Upgrading from `v1.28.x` to `v1.30.x` is not allowed. Upgrade to `v1.29.x` first.
- **No downgrades**: K3s does not support downgrades. Attempting to set a lower version will fail with an error.
- **Patch upgrades**: Upgrading within the same minor version (e.g., `v1.29.2` → `v1.29.5`) is always allowed.

If the upgrade path validation cannot determine the installed version (e.g., on a fresh install), the check is skipped and the specified version is installed directly.

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
