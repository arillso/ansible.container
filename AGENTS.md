# arillso.container

Ansible collection with roles for Docker, Docker Compose, K3s, Helm, Rancher
Fleet and Tailscale. User documentation lives on
<https://guide.arillso.io/collections/arillso/container/>; this file covers
changing the collection.

## Commands

`make help` lists the targets. Lint with `make lint`, run the unit tests with
`make test`. Before running or changing a Molecule scenario, read
[`docs/testing.md`](docs/testing.md): the scenarios boot qemu VMs and need KVM.

## Conventions

### Variables are documented in argument_specs

`roles/<role>/meta/argument_specs.yml` is the complete variable reference and
the input for the guide. Role READMEs carry features, a Quick Start and a link
to the guide, no variable tables. `defaults/main.yml` stays lean: a comment only
where a complex variable needs an example.

Every role variable carries the role name as prefix (`k3s_`, `fleet_`, …).

### Version pins

Pinned upstream versions live in `defaults/main.yml` with a Renovate comment on
the line above, so Renovate bumps them:

```yaml
# renovate: datasource=github-releases depName=k3s-io/k3s
k3s_version: "v1.37.2+k3s1"
```

### tasks/main.yml as dispatcher

`tasks/main.yml` dispatches, it does not implement. It holds the role-level
validation, the flow-control tasks (`include_vars`, `meta`) and one
`include_tasks` per topic file; the implementation lives in the topic files.

- Topic files carry no name prefix. Existing files are named after their topic
  (`facts.yml`, `security.yml`, `install.yml`, `configure.yml`).
- Include order equals the previous task order. `set_fact` values are
  host-scoped and only propagate forward across `include_tasks`.
- Descriptive tags belong on the individual tasks, because a tag on the include
  applies to every task in the file. Functional tags stay on the include:
  `always`, or a topic tag when the whole file should be selectable. A dynamic
  `include_tasks` is evaluated by its own tags, so an untagged include is
  skipped whole under `--tags` and the inner tasks are never reached. Where only
  part of a file must stay selectable, split that part into its own include and
  tag that (see `roles/k3s/tasks/refresh_facts.yml`).

Exception: `docker_login` consists of the role-level credential check plus a
single task (`community.docker.docker_login`). There is no second phase to split
off, so the role keeps everything in `main.yml`.

### CHANGELOG

Every user-visible change gets an entry under `## [Unreleased]` in
`CHANGELOG.md`. The release steps (CHANGELOG, `galaxy.yml` version, tag without
`v` prefix) are in [`CONTRIBUTING.md`](CONTRIBUTING.md#release-process); pushing
the tag runs `tag.yml`, which publishes to Galaxy.

## Traps

- **Static guards in `tests/unit/`.** `test_el_support.py` fails when a role
  declares `EL` in `meta/main.yml` without a matching RedHat platform in its
  Molecule scenario, when a platform lacks a `host_vars` entry or shares an SSH
  port, when a Molecule playbook installs packages with `ansible.builtin.apt`
  instead of `ansible.builtin.package`, or when the docker and
  docker_compose_v2 package pins break their apt/rpm syntax.
  `test_helm_per_host.py` fails on any `run_once` in the fleet, helm, k3s and
  tailscale tasks (every host is its own k3s cluster) and when the
  `helm_repositories` default drifts between `defaults/main.yml` and
  `argument_specs.yml`. Adding a platform, a pin or a Molecule playbook means
  running `make test`.
- **Lint differs between hook and CI.** The lefthook `ansible-lint` runs
  `--offline` so a machine without Galaxy access can still commit; CI lints
  online. `.ansible-lint` excludes the fleet, helm and tailscale
  `molecule/default/verify.yml` because the lint job does not install
  `kubernetes.core`. A new playbook calling `kubernetes.core` needs the same
  exclusion.
- **Integration tests do not run in CI.** The only targets, `fleet` and
  `tailscale`, are `disabled`, and the reusable calls `ansible-test integration`
  without `--docker-privileged`, so a new target marked `needs/privileged`
  would be skipped as well.
  Role coverage lives in the per-role Molecule jobs of `pull-request.yml`.
- **One Molecule job per role.** A new role needs its own `molecule-<role>` job
  in `pull-request.yml`; CI does not discover scenarios on its own.

## Further docs

- Before running or changing tests: [`docs/testing.md`](docs/testing.md).
- Before touching a disabled integration target:
  [`tests/integration/targets/README.md`](tests/integration/targets/README.md).
- What the review bot checks and skips: [`REVIEW.md`](REVIEW.md).
