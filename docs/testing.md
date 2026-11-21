# Testing

How to run the collection's tests locally and what CI runs. For contributors
changing a role, a plugin or a test; read it before running Molecule for the
first time.

## Levels

| Level                                      | Location                         | Runs in CI                                                   |
| ------------------------------------------ | -------------------------------- | ------------------------------------------------------------ |
| Lint (ansible-lint, yamllint, ruff, black) | repo; ruff and black `plugins/`  | yes, `ci` job                                                |
| Unit tests (pytest)                        | `tests/unit/`                    | yes, `ci` job                                                |
| Molecule, one scenario per role            | `roles/<role>/molecule/default/` | yes, one `molecule-<role>` job each                          |
| Integration (`ansible-test`)               | `tests/integration/targets/`     | no, see [its README](../tests/integration/targets/README.md) |

The unit tests are static checks over the repo, not plugin tests only. They
guard EL support, package pin syntax and helm's per-host execution, and run
without a VM.

## Setup

```bash
make install-dev
lefthook install
```

`install-dev` installs `requirements.txt`, which includes `molecule-qemu`.
`lefthook` itself is not in it; install the binary first. Its hooks also call
`npx`, `gitleaks` and `actionlint`.

## Lint and unit tests

```bash
make lint
make test
```

## Molecule

The scenarios use the `molecule-qemu` driver, not the docker driver: dockerd
and k3s need a real kernel (modprobe, cgroups). Each scenario boots an Ubuntu
and a Rocky 9 cloud image; docker and k3s add Debian 12.

Prerequisites:

- `qemu-system-x86_64`, `qemu-img`, `mkisofs` (package `genisoimage` on Debian) for the
  cloud-init seed, and access to `/dev/kvm`.
- About 2–3 GiB RAM per VM (`vm_memory` in each `molecule.yml`), three VMs for
  docker and k3s.
- Free ports 2222–2224 on localhost. Every scenario forwards SSH to the same
  ports, so run one role at a time.

The scenarios call each role by its full name (`arillso.container.<role>`).
Install the checkout as that collection first, or Molecule tests a copy from
Galaxy instead of your changes. Repeat after every change:

```bash
make build
ansible-galaxy collection install arillso-container-*.tar.gz --force
```

Then run the role's scenario from the role directory:

```bash
cd roles/<role>
molecule test
```

During development, keep the VMs between runs:

```bash
molecule converge
molecule verify
molecule destroy
```

The scenarios that need a cluster (fleet, helm, tailscale) install k3s in
`prepare.yml` first, so they take longer than the docker roles.

## Adding a role or platform

- New role: add a `molecule-<role>` job to `.github/workflows/pull-request.yml`,
  copied from an existing one with `scenarios_root` and `concurrency-suffix`
  changed.
- New platform: give it its own `network_ssh_port` and a `host_vars` entry,
  then run `make test`. `tests/unit/test_el_support.py` checks both.
