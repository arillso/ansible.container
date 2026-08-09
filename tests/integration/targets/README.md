# Integration test targets

Each directory here is an `ansible-test` integration target. Run the whole
suite with:

```bash
ansible-test integration
```

Targets whose `aliases` file contains `disabled` are excluded from that run and
from CI. They are not broken — they need infrastructure a CI runner does not
have. Run them manually with `--allow-disabled` once the prerequisites below are
in place.

## Disabled targets

### `fleet`

- **Why disabled:** exercising the role end-to-end requires a running K3s
  cluster with the Rancher Fleet CRDs and controller installed. The `Bundle`
  resource is applied with `wait_condition type=Ready`, which only reconciles
  once the Fleet controller is present. Plain CI runners and the default
  `ansible-test` containers do not ship Fleet.
- **Prerequisites:** a K3s cluster with Rancher Fleet deployed, reachable via
  the kubeconfig at `/etc/rancher/k3s/k3s.yaml` (override with
  `fleet_kubeconfig_path`).
- **Run manually:**

    ```bash
    ansible-test integration fleet --allow-disabled
    ```

### `tailscale`

- **Why disabled:** the role does not install Tailscale on a host with an auth
  key — it manages Tailscale Kubernetes resources (ProxyGroups, Ingress/Egress
  Services) via the `tailscale.com/v1alpha1` CRDs. End-to-end testing therefore
  needs a K3s cluster _and_ the Tailscale Kubernetes operator installed in it,
  which in turn needs a Tailscale OAuth client to register with the tailnet.
  CI runners have neither the operator nor a tailnet credential.
- **Prerequisites:** a K3s cluster with the Tailscale Kubernetes operator
  installed, plus a Tailscale OAuth client. The client id and secret are read
  from the environment and are never hardcoded; they only bootstrap the
  operator, the role itself takes no credentials.
- **Run manually:**

    ```bash
    TS_OAUTH_CLIENT_ID=... TS_OAUTH_CLIENT_SECRET=... \
      ansible-test integration tailscale --allow-disabled
    ```

Both targets depend on the `k3s` target to provide the cluster. The
per-target `tasks/main.yml` files carry the same reasoning inline; keep the two
in sync when the prerequisites change.
