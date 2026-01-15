# Ansible Collection: arillso.container

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=popout-square)](licence) [![Ansible Galaxy](http://img.shields.io/badge/ansible--galaxy-arillso.container-blue.svg?style=popout-square)](https://galaxy.ansible.com/arillso/container)

## Description

This is an Ansible collection that provides comprehensive roles for container and orchestration management. It includes tools for Docker, Docker Compose, Kubernetes (K3s), Helm, Rancher Fleet GitOps, and Tailscale VPN mesh networking.

## Roles

### Docker Ecosystem

- **[docker](roles/docker/README.md)** - Docker Engine installation and configuration with comprehensive daemon settings
- **[docker_compose](roles/docker_compose/README.md)** - Docker Compose v1 (legacy) installation and management
- **[docker_compose_v2](roles/docker_compose_v2/README.md)** - Docker Compose v2 (modern) installation as Docker CLI plugin
- **[docker_login](roles/docker_login/README.md)** - Docker registry authentication management for multiple registries

### Kubernetes Ecosystem

- **[k3s](roles/k3s/README.md)** - Lightweight Kubernetes distribution with autonomous deployment and HA support
- **[fleet](roles/fleet/README.md)** - Rancher Fleet GitOps management for Kubernetes with GitRepo and Bundle support
- **[helm](roles/helm/README.md)** - Helm package manager for Kubernetes with chart and repository management
- **[tailscale](roles/tailscale/README.md)** - Tailscale VPN mesh networking with Kubernetes ProxyGroup configuration

## Installation

Install this collection from Ansible Galaxy:

```bash
ansible-galaxy collection install arillso.container
```

Or add it to your `requirements.yml`:

```yaml
---
collections:
    - name: arillso.container
      version: ">=0.0.5"
```

## Quick Start

See the [examples](examples/) directory for sample playbooks and inventory configurations.

For detailed documentation, visit [guide.arillso.io](https://guide.arillso.io).

## License

<!-- markdownlint-disable -->

This project is under the MIT License. See the [LICENSE](licence) file for the full license text.

<!-- markdownlint-enable -->

## Copyright

(c) 2023-2026, Arillso
