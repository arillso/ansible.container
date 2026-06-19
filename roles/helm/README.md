# Ansible Role: helm

Installs and manages Helm, the package manager for Kubernetes.

## Features

- **Chart Deployment**: Deploy Helm charts via the K3s-embedded Helm controller
  (`helm.cattle.io/v1` HelmChart CRDs) — no separate Helm binary required
- **Repository Management**: Add and manage Helm chart repositories
- **Chart Operations**: Install, upgrade, and remove Helm charts
- **Per-Chart Versioning**: Pin a chart `version` per entry in `helm_charts`
- **Validation**: Optional cluster reachability and deployment-wait checks

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/container/helm_role.html](https://guide.arillso.io/collections/arillso/container/helm_role.html)**

## Quick Start

```yaml
- hosts: k8s_masters
  roles:
      - role: arillso.container.helm
        vars:
            helm_enable_charts: true
            helm_charts:
                - name: "cert-manager"
                  chart: "cert-manager"
                  repository: "jetstack"
                  version: "v1.13.2"
                  namespace: "cert-manager"
                  create_namespace: true
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
