# Ansible Role: fleet

Installs and configures Rancher Fleet for GitOps-based Kubernetes management.

## Features

- **Fleet Installation**: Deploy Rancher Fleet on Kubernetes clusters
- **GitOps Management**: Manage Kubernetes resources from Git repositories
- **Multi-Cluster**: Support for multi-cluster deployments
- **Helm Integration**: Deploy Helm charts via GitOps
- **Fleet Configuration**: Configure Fleet controller and agents

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/container/fleet_role.html](https://guide.arillso.io/collections/arillso/container/fleet_role.html)**

## Quick Start

```yaml
- hosts: k8s_masters
  roles:
      - role: arillso.container.fleet
        vars:
            fleet_namespace: cattle-fleet-system
```

## Troubleshooting

- **GitRepo does not sync**: inspect the GitRepo status with
  `kubectl -n <fleet-namespace> get gitrepo` and the controller logs. Missing or
  incorrect Git authentication (the `auth` entry point) is a common cause.
- **Cluster not registered / agent not connecting**: verify the
  ClusterRegistrationToken is valid and the downstream agent can reach the Fleet
  controller; check `kubectl -n <fleet-namespace> get clusters`.
- **Resources never reconcile**: confirm the Fleet controller and agents are
  running (`kubectl -n <fleet-namespace> get pods`) before re-running the role.

For detailed guidance see <https://guide.arillso.io>.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
