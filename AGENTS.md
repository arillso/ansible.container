# Ansible Collection: arillso.container

## Context

This is an Ansible collection that provides roles for container and orchestration management. The collection includes roles for Docker, Docker Compose, Kubernetes (K3s), Helm, Fleet, and Tailscale.

## Structure

### Collection Structure

```text
ansible.container/
├── .github/workflows/
│   ├── ci.yml              # All-in-one: linting, tests, build
│   └── publish.yml         # Galaxy publishing
├── roles/
│   ├── docker/
│   ├── docker_compose/
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
├── pytest.ini
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

### Roles

#### Docker Ecosystem

- **docker** - Docker Engine installation (27.5.1)
- **docker_compose** - Docker Compose v1
- **docker_compose_v2** - Docker Compose v2 (2.32.4)
- **docker_login** - Docker registry authentication

#### Kubernetes Ecosystem

- **k3s** - Lightweight Kubernetes (v1.33.3+k3s1) with security hardening
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

3. **Integration Tests** (ansible-test) - For role integration
    - Location: `tests/integration/targets/`
    - Run: `ansible-test integration`

All tests consolidated in single `ci.yml` workflow.

### Documentation

**Keep documentation DRY:**

1. **Collection README** - Overview + all roles listed
2. **Role README** - Features + Quick Start + link to guide
3. **argument_specs.yml** - Complete variable documentation
4. **guide.arillso.io** - Comprehensive documentation with examples

### Version Management

All versions managed by Renovate:

- Docker: `docker_version` with renovate comment
- Docker Compose: `docker_compose_version` / `docker_compose_v2_version`
- K3s: `k3s_version`

Format:

```yaml
# renovate: datasource=github-releases depName=k3s-io/k3s
k3s_version: "v1.33.3+k3s1"
```

## Workflows

### CI/CD

**Standard workflows:**

- `ci.yml` - All linting, tests (unit, molecule, integration), and build
- `publish.yml` - Galaxy publishing (triggered by tag)

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
    - `publish.yml` publishes to Ansible Galaxy
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
- ❌ Do not create separate test workflows (use ci.yml)
- ❌ Do not skip CHANGELOG.md updates before releases
- ❌ Do not use 'v' prefix in Ansible Collection tags
