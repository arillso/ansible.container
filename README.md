# Ansible Collection: arillso.container

[![CI](https://github.com/arillso/ansible.container/actions/workflows/merge.yml/badge.svg?branch=main)](https://github.com/arillso/ansible.container/actions/workflows/merge.yml)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-arillso.container-blue.svg)](https://galaxy.ansible.com/ui/repo/published/arillso/container/)
[![License: MIT](https://img.shields.io/github/license/arillso/ansible.container)](LICENSE)

Roles to install and run container and Kubernetes infrastructure on Debian,
Ubuntu and EL 9 hosts.

## Roles

| Role                                                   | Purpose                                                                |
| ------------------------------------------------------ | ---------------------------------------------------------------------- |
| [docker](roles/docker/README.md)                       | Docker Engine installation and daemon configuration                    |
| [docker_compose_v2](roles/docker_compose_v2/README.md) | Docker Compose v2 as Docker CLI plugin                                 |
| [docker_login](roles/docker_login/README.md)           | Login to and logout from a container registry                          |
| [k3s](roles/k3s/README.md)                             | K3s server and agent nodes, including HA with embedded etcd            |
| [helm](roles/helm/README.md)                           | Helm repositories and charts on a K3s cluster                          |
| [fleet](roles/fleet/README.md)                         | Rancher Fleet GitRepos, Bundles and cluster registration               |
| [tailscale](roles/tailscale/README.md)                 | Tailscale Kubernetes operator resources (ProxyGroups, ingress, egress) |

## Quickstart

```bash
ansible-galaxy collection install arillso.container
```

```yaml
---
- name: Install Docker
  hosts: docker_hosts
  become: true
  roles:
      - arillso.container.docker
```

The collection depends on `arillso.system`, `community.docker` and
`kubernetes.core`; `ansible-galaxy` installs them with it.

## Configuration

Each role documents its variables in `roles/<role>/meta/argument_specs.yml`,
and Ansible validates them at runtime. Examples per role are in the guide:
<https://guide.arillso.io/collections/arillso/container/>

## Requirements

- Ansible >= 2.18
- Python >= 3.11 on the control node (ansible-core 2.18 minimum)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Test setup and Molecule usage:
[docs/testing.md](docs/testing.md).

## License

MIT, see [LICENSE](LICENSE). (c) 2023-2026, Arillso
