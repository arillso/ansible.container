# Ansible Role: helm

Installs and manages Helm, the package manager for Kubernetes.

## Features

- **Helm Installation**: Install Helm binary from official releases
- **Version Management**: Install specific Helm versions or latest
- **Repository Management**: Add and manage Helm chart repositories
- **Chart Operations**: Install, upgrade, and remove Helm charts
- **Multi-Architecture**: Support for x86_64 and ARM architectures

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/container/helm_role.html](https://guide.arillso.io/collections/arillso/container/helm_role.html)**

## Quick Start

```yaml
- hosts: k8s_masters
  roles:
      - role: arillso.container.helm
        vars:
            helm_version: "3.13.0"
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
