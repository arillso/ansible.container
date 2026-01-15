# Ansible Role: tailscale

Manages Tailscale resources in Kubernetes for secure mesh networking and service exposure. Supports all three ProxyGroup types: ingress, egress, and kube-apiserver.

## Features

- **ProxyGroups**: All three types (ingress, egress, kube-apiserver)
- **Ingress Services**: Expose Kubernetes services to Tailnet (LoadBalancer/Ingress)
- **Egress Services**: Access Tailnet services from Kubernetes (FQDN/IP)
- **Kubernetes API Server Proxy**: Secure remote cluster access
- **Multi-Namespace**: Support for resources across namespaces

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/container/tailscale_role.html](https://guide.arillso.io/collections/arillso/container/tailscale_role.html)**

## Quick Start

### 1. Ingress ProxyGroup (Expose K8s services to Tailnet)

```yaml
- hosts: k8s_masters
  roles:
      - role: arillso.container.tailscale
        vars:
            tailscale_proxygroups:
                - name: ingress-proxies
                  namespace: tailscale
                  type: ingress
                  replicas: 2
                  tags:
                      - "tag:k8s-ingress"
                  hostname_prefix: prod-ingress

            tailscale_ingress_services:
                - name: my-app
                  namespace: default
                  type: loadbalancer
                  proxy_group: ingress-proxies
                  hostname: my-app
                  selector:
                      app: my-app
                  ports:
                      - name: http
                        port: 80
                        targetPort: 8080
```

### 2. Egress ProxyGroup (Access Tailnet from K8s)

```yaml
- hosts: k8s_masters
  roles:
      - role: arillso.container.tailscale
        vars:
            tailscale_proxygroups:
                - name: egress-proxies
                  namespace: tailscale
                  type: egress
                  replicas: 3
                  tags:
                      - "tag:k8s-egress"

            tailscale_egress_services:
                - name: internal-database
                  namespace: default
                  proxy_group: egress-proxies
                  fqdn: database.tailnet-abc.ts.net
                  ports:
                      - name: postgres
                        port: 5432
                        protocol: TCP
```

### 3. Kube-APIServer ProxyGroup (Secure API access)

```yaml
- hosts: k8s_masters
  roles:
      - role: arillso.container.tailscale
        vars:
            tailscale_proxygroups:
                - name: k8s-api-proxy
                  namespace: tailscale
                  type: kube-apiserver
                  replicas: 2
                  tags:
                      - "tag:k8s-api"
                  hostname_prefix: k8s-api
                  kube_apiserver:
                      mode: auth
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
