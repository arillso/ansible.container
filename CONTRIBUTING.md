# Contributing to arillso.container

Thank you for your interest in contributing to the arillso.container Ansible collection! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Ansible 2.16 or higher
- Git
- Docker (for testing)

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/ansible.container.git
cd ansible.container
```

3. Install development dependencies:

```bash
pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml
```

4. Create a new branch for your feature or fix:

```bash
git checkout -b feature/your-feature-name
```

## Project Structure

```
ansible.container/
├── roles/               # Ansible roles
│   ├── docker/
│   ├── k3s/
│   └── ...
├── plugins/
│   └── filter/         # Custom filter plugins
├── tests/
│   ├── integration/    # Integration tests
│   └── unit/           # Unit tests
├── examples/           # Example playbooks
├── .github/
│   └── workflows/      # CI/CD workflows
└── docs/               # Additional documentation
```

## Development Guidelines

### Code Style

#### YAML Files

- Use 2 spaces for indentation
- Use lowercase with underscores for variable names
- Prefix role variables with the role name (e.g., `docker_daemon_config`)
- Use descriptive variable names
- Add comments for complex logic
- Keep lines under 160 characters when possible

#### Python Files

- Follow PEP 8 style guidelines
- Use 4 spaces for indentation
- Add docstrings for all functions and classes
- Use type hints where applicable
- Keep functions focused and single-purpose

### Ansible Best Practices

1. **Idempotency**: All tasks must be idempotent
2. **Handlers**: Use handlers for service restarts and reloads
3. **Variables**: Document all variables in `defaults/main.yml`
4. **Argument Specs**: Always provide `meta/argument_specs.yml` for roles
5. **Tags**: Use meaningful tags for task organization
6. **Privilege Escalation**: Use `become: true` only when necessary
7. **OS Support**: Test on multiple distributions when possible

### Creating a New Role

1. Create the role structure:

```bash
ansible-galaxy role init roles/your_role_name
```

2. Required files:
    - `README.md` - Role documentation with Features, Quick Start
    - `defaults/main.yml` - Default variables with comments
    - `meta/argument_specs.yml` - Argument specifications
    - `meta/main.yml` - Role metadata and dependencies
    - `tasks/main.yml` - Main task file

3. Update collection metadata:
    - Add role to main `README.md`
    - Add role to `CHANGELOG.md` under [Unreleased]
    - Create example playbook in `examples/`

### Writing Tests

#### Unit Tests

For filter plugins and Python code:

```python
# tests/unit/plugins/filter/test_fleet_filters.py
import pytest
from ansible_collections.arillso.container.plugins.filter.fleet_filters import to_camel_case

def test_to_camel_case():
    assert to_camel_case("hello_world") == "helloWorld"
    assert to_camel_case("test_case_example") == "testCaseExample"
```

Run unit tests:

```bash
pytest tests/unit/
```

#### Integration Tests

Create test playbooks in `tests/integration/targets/`:

```yaml
# tests/integration/targets/docker/tasks/main.yml
---
- name: Install Docker
  include_role:
      name: arillso.container.docker

- name: Verify Docker is installed
  command: docker --version
  register: docker_version
  changed_when: false

- name: Check Docker service is running
  service:
      name: docker
      state: started
  check_mode: true
  register: docker_service
  failed_when: docker_service.changed
```

Run integration tests:

```bash
ansible-test integration docker --docker
```

#### Molecule Tests

For role testing with Molecule:

```bash
cd roles/docker
molecule test
```

### Linting

Before submitting, run all linters:

```bash
# Ansible linting
ansible-lint

# YAML linting
yamllint .

# Python linting
ruff check .
black --check .
pylint plugins/

# Markdown linting
markdownlint-cli2 "**/*.md"
```

Fix issues automatically where possible:

```bash
black .
ruff check --fix .
```

## Submitting Changes

### Commit Messages

Follow the Conventional Commits specification:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:

```
feat(docker): add support for Docker daemon metrics

Add configuration options for enabling Prometheus metrics
endpoint on Docker daemon.

Closes #123
```

```
fix(k3s): correct token retrieval in HA mode

The token was not being correctly retrieved when using
external datastore. This fix ensures the token is fetched
from the correct location.
```

### Pull Request Process

1. **Update Documentation**:
    - Update role README if behavior changes
    - Update CHANGELOG.md under [Unreleased]
    - Add or update example playbooks

2. **Add Tests**:
    - Add unit tests for Python code
    - Add integration tests for new roles or features
    - Ensure all tests pass locally

3. **Run Linters**:
    - Fix all linting errors
    - Ensure CI checks will pass

4. **Create Pull Request**:
    - Use a descriptive title following conventional commits
    - Reference related issues
    - Describe changes and motivation
    - Include testing information
    - Add screenshots for UI changes (if applicable)

5. **Pull Request Template**:

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Tested on: [list distributions/versions]

## Checklist

- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] All tests pass
- [ ] Linting passes
```

## Release Process

**Note**: Only maintainers can create releases.

1. Update `CHANGELOG.md`:
    - Move items from [Unreleased] to new version section
    - Add release date

2. Update `galaxy.yml`:
    - Bump version number (follow semver)

3. Create and push tag:

```bash
git tag 0.1.0
git push origin 0.1.0
```

4. GitHub Actions will automatically:
    - Build the collection
    - Publish to Ansible Galaxy
    - Create GitHub Release

## Getting Help

- **Issues**: Open an issue on GitHub for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check [guide.arillso.io](https://guide.arillso.io)

## Recognition

Contributors will be:

- Listed in release notes
- Credited in the CHANGELOG
- Added to the contributors list

Thank you for contributing to arillso.container!
