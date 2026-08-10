# Ansible Collection: arillso.container

## Context

This is an Ansible collection that provides roles for container and orchestration management. The collection includes roles for Docker, Docker Compose, Kubernetes (K3s), Helm, Fleet, and Tailscale.

## Structure

### Collection Structure

```text
ansible.container/
├── .github/workflows/
│   ├── pull-request.yml    # Lint, tests, per-role molecule, secret scan, Claude review
│   ├── merge.yml           # CI + secret scan on push to main
│   ├── nightly-security.yml # Scheduled daily secret scan
│   └── tag.yml             # Galaxy publishing (triggered by tag)
├── roles/
│   ├── docker/
│   ├── docker_compose_v2/
│   ├── docker_login/
│   ├── fleet/
│   ├── helm/
│   ├── k3s/
│   └── tailscale/
├── plugins/filter/         # Filter plugins
├── tests/
│   ├── integration/        # Integration tests (ansible-test)
│   └── unit/              # Unit tests (pytest)
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── galaxy.yml
├── pyproject.toml
└── requirements.txt
```

### Role Structure

Each role follows standard Ansible role structure:

- `tasks/` - Main task files
- `defaults/` - Default variables (minimal comments, examples in comments)
- `vars/` - Role variables
- `handlers/` - Handlers for service restarts
- `templates/` - Jinja2 templates
- `meta/` - Role metadata with `argument_specs.yml` (required)
- `molecule/` - Molecule tests (role-level testing)

### tasks/main.yml as Dispatcher

`tasks/main.yml` dispatches, it does not implement. It holds the role-level
validation, the flow-control tasks (`include_vars`, `meta`) and one
`include_tasks` per topic file; the implementation lives in the topic files.

- Topic files carry no name prefix. Existing files are named after their topic
  (`facts.yml`, `security.yml`, `install.yml`, `configure.yml`).
- Include order equals the previous task order. `set_fact` values are
  host-scoped and only propagate forward across `include_tasks`.
- Do not tag an include merely to label its contents — descriptive tags belong
  on the individual tasks, because a tag on the include applies to every task in
  the file. Functional tags stay on the include: `always`, or a topic tag when
  the whole file should be selectable. A dynamic `include_tasks` is evaluated by
  its own tags, so an untagged include is skipped whole under `--tags` and the
  inner tasks are never reached. Where only part of a file must stay selectable,
  split that part into its own include and tag that (see `refresh_facts.yml`).

Exception: `docker_login` consists of a single task
(`community.docker.docker_login`). There is no second phase to split off, so a
`main.yml` including one file with one task would be indirection without
structural gain. The role stays as it is.

### Roles

#### Docker Ecosystem

- **docker** - Docker Engine installation (28.5.2)
- **docker_compose_v2** - Docker Compose v2 (5.1.0)
- **docker_login** - Docker registry authentication

#### Kubernetes Ecosystem

- **k3s** - Lightweight Kubernetes (v1.35.2+k3s1) with security hardening
- **fleet** - Rancher Fleet GitOps management
- **helm** - Helm package manager for Kubernetes
- **tailscale** - Tailscale VPN mesh network (ingress, egress, kube-apiserver)

## Conventions

### Code Style

- Use 4 spaces for indentation in YAML files
- Follow Ansible best practices and naming conventions
- Use descriptive variable names with role prefixes
- Minimal comments in defaults/main.yml (keep it clean)
- Examples in comments for complex variables
- Use handlers for service management

### Testing

Three-level testing strategy:

1. **Unit Tests** (pytest) - For plugins
    - Location: `tests/unit/plugins/`
    - Run: `pytest tests/unit/`

2. **Molecule Tests** - For individual roles
    - Location: `roles/*/molecule/default/`
    - Run: `molecule test -s default`
    - CI: one `molecule-<role>` job per role in `pull-request.yml` (one per role)

3. **Integration Tests** (ansible-test) - For role integration
    - Location: `tests/integration/targets/`
    - Run: `ansible-test integration`
    - Not wired into CI: the reusable workflow calls `ansible-test integration`
      without `--docker-privileged`, so every target marked `needs/privileged`
      is skipped. The remaining targets (`fleet`, `tailscale`) are `disabled`.
      Role coverage lives in the Molecule scenarios above, which use the
      qemu/KVM driver and can run dockerd and k3s for real.

Tests run via the reusable CI (`arillso/.github`) on pull requests and merges.

### Documentation

**Keep documentation DRY:**

1. **Collection README** - Overview + all roles listed
2. **Role README** - Features + Quick Start + link to guide
3. **argument_specs.yml** - Complete variable documentation
4. **guide.arillso.io** - Comprehensive documentation with examples

### Version Management

All versions managed by Renovate:

- Docker: `docker_version` with renovate comment
- Docker Compose: `docker_compose_v2_version`
- K3s: `k3s_version`

Format:

```yaml
# renovate: datasource=github-releases depName=k3s-io/k3s
k3s_version: "v1.35.2+k3s1"
```

## Workflows

### CI/CD

Event-focused workflows calling reusables from `arillso/.github`:

- `pull-request.yml` - Lint, unit/integration tests, per-role molecule, secret scan, and Claude review on PRs
- `merge.yml` - Same CI plus secret scan on push to `main`
- `nightly-security.yml` - Scheduled daily secret scan
- `tag.yml` - Publishes to Ansible Galaxy on tag push (e.g. `0.0.8`)

### Release Process

**IMPORTANT: Always update CHANGELOG.md before releasing!**

1. **Update CHANGELOG.md** (REQUIRED)
    - Move items from `## [Unreleased]` to new version section
    - Document all changes under appropriate sections (Added, Changed, Fixed, etc.)

2. **Update galaxy.yml version**
    - Use semantic versioning (MAJOR.MINOR.PATCH)
    - Example: `version: "0.0.8"`

3. **Create and push git tag**
    - Use version **without 'v' prefix** (e.g., `0.0.8` not `v0.0.8`)
    - Command: `git tag 0.0.8 && git push origin 0.0.8`

4. **Automated workflow triggers**
    - `tag.yml` publishes to Ansible Galaxy
    - Creates GitHub Release with CHANGELOG notes

## Do

- ✅ Always use argument_specs.yml for all roles
- ✅ Keep defaults/main.yml clean (minimal comments)
- ✅ Add renovate comments for version variables
- ✅ Test with ansible-lint before committing
- ✅ Update CHANGELOG.md before releasing
- ✅ Link to guide.arillso.io in role READMEs
- ✅ Use MIT license with copyright years 2023-2026

## Do Not

- ❌ Do not commit secrets or sensitive data
- ❌ Do not create roles without argument_specs.yml
- ❌ Do not use deprecated Ansible syntax
- ❌ Do not hardcode values that should be variables
- ❌ Do not add excessive comments to defaults/main.yml
- ❌ Do not create separate test workflows (CI runs via the reusable in `pull-request.yml`/`merge.yml`)
- ❌ Do not skip CHANGELOG.md updates before releases
- ❌ Do not use 'v' prefix in Ansible Collection tags
