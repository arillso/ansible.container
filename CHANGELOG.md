# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.2] - 2026-03-20

### Fixed

- Fixed remaining k3s handler name case mismatches: `reload systemd` → `Reload systemd` and `restart k3s` → `Restart k3s` in systemd service task
- Added `meta: flush_handlers` before k3s server health check to ensure server restarts before agents attempt to connect

## [1.3.1] - 2026-03-20

### Fixed

- Fixed k3s role handler name case mismatch: `restart k3s` → `Restart k3s` causing deployment failures when k3s binary or config changes trigger a service restart

## [1.3.0] - 2026-03-19

### Added

- Added k3s upgrade path validation: blocks downgrades and enforces one-minor-version-at-a-time upgrades
- Added automatic k3s binary upgrade detection by comparing installed version with target `k3s_version`
- Added upgrade documentation to k3s role README

## [1.2.0] - 2026-03-18

### Added

- Added comprehensive argument specs for K3s role covering networking, storage, security, service, and facts variables (#46)
- Added K3s facts configuration variables (`k3s_facts_collect_cluster_state`, `k3s_facts_collect_service_status`, `k3s_facts_collect_inventory_info`, `k3s_facts_collect_health_metrics`) with expanded fact template (#51)
- Added K3s facts dependency wiring to `arillso.system.facts` role via configurable variables (#51)
- Added `docker_compose_v2_scale` and `docker_compose_v2_build`/`docker_compose_v2_ca_path` argument specs for Docker Compose v2 role (#45)
- Added `fleet_registration_tokens`, Fleet authentication defaults (`fleet_git_username`, `fleet_git_token`, etc.) and missing argument specs (`fleet_dry_run`, `fleet_secret_timeout`, `fleet_resource_timeout`) for Fleet role (#45)
- Added nested `options` for `helm_defaults` in Helm role argument specs (#45)
- Added Makefile with targets for lint, test, format, build, clean, and install-dev (#44)
- Added pyproject.toml with black, isort, ruff, and pytest configuration (#44)
- Added pre-commit configuration with trailing-whitespace, end-of-file-fixer, and ansible-lint hooks (#44)
- Added security scanning configurations: checkov, gitleaks, grype, trivy, secretlint (#44)
- Added markdownlint, markdown-link-check, jscpd, and kics configuration files (#44)

### Changed

- Renamed `k3s_facts_health_check_interval` to `k3s_facts_health_check_timeout` (#51)
- Changed `k3s_enable_helm_integration` default from `true` to `false` (#51)
- Changed `docker_compose_v2_recreate` default from `smart` to `auto` and added type to `docker_compose_v2_pull` (#45)
- Updated `docker_version` default in argument specs to `28.5.2`, `docker_compose_v2_version` to `5.1.0` (#45)
- Renamed Fleet auth variables to use `fleet_` prefix (`git_username` → `fleet_git_username`, etc.) (#45)
- Updated `helm_repositories` default to include `noqa: argument-specs` annotation (#45)
- Replaced `.yamllint.yml` with comprehensive `.yamllint` configuration (stricter rules, 160 char line limit) (#44)
- Modernized `.ansible-lint` configuration (removed `experimental` skip, cleaned up formatting) (#44)
- Expanded `.gitignore` with testing, build, and environment patterns (#44)
- Simplified CONTRIBUTING.md (reduced from 334 to 167 lines, modernized prerequisites to Python 3.12/Ansible 2.18) (#44)
- Migrated pytest configuration from `pytest.ini` to `pyproject.toml` (#44)
- Bumped `requires_ansible` from `>=2.15.5` to `>=2.18.0` in `meta/runtime.yml` (#44)
- Updated Renovate config to pin shared preset version and add custom regex manager for role defaults (#43)
- Updated CI workflows to `@2026-03-09` shared workflow refs (#43)
- Restricted Claude AI workflow triggers to `@claude` mentions only (#43)
- Updated Claude review to trigger only on PR open events (#43)
- Updated Python development dependencies (pytest-cov v7, molecule v26/v25, ansible-lint v26, black v26, sphinx v9, and others) (#47, #48, #49, #50, #52)

### Removed

- Removed `k3s_require_facts_role` variable from K3s defaults (#51)

## [1.1.0] - 2026-03-08

### Changed

- Migrated CI/CD workflows to shared reusable workflows from `arillso/.github`
- Updated Docker Engine default version from 27.5.1 to 28.5.2
- Updated Docker Compose v2 default version from 2.32.4 to 5.1.0
- Updated K3s default version from v1.33.3+k3s1 to v1.35.2+k3s1
- Updated Python development dependencies (pytest-cov, pylint, sphinx-rtd-theme)
- Updated documentation links with UTM tracking parameters
- Excluded `ansible-core` from Renovate updates (version controlled by CI matrix)

### Added

- Added Claude AI workflow for automated issue and PR handling
- Added Claude AI review workflow for pull requests

## [1.0.2] - 2026-01-17

### Fixed

- Fixed K3s role Galaxy validation errors by removing invalid `no_log` field from argument_specs.yml
- Fixed Fleet role Galaxy validation errors by replacing YAML anchor references with explicit descriptions
- Resolved 13 total validation errors preventing proper indexing on Ansible Galaxy
- K3s and Fleet roles now properly documented and searchable on Galaxy

## [1.0.1] - 2026-01-16

### Fixed

- Fixed K3s configuration directory permissions causing unnecessary 'changed' status on every run
- Improved K3s AppArmor profile with comprehensive permissions for container operations
- Added sys_chroot, sys_ptrace, dac_override capabilities
- Added xtables-nft-multi, nft, modprobe subprocess execution permissions
- Expanded proc/sys and sys filesystem access for full K3s functionality
- Added file locking support (k flag) to k3s data directory
- Added ptrace permissions for containerd process management
- Improved Galaxy collection description for better discoverability

### Changed

- Disabled K3s AppArmor profile by default (k3s_apparmor_profile: false)
- K3s configuration directory now created with correct 0700 permissions from the start

## [1.0.0] - 2026-01-15

### Added

- Added new K3s role with comprehensive Kubernetes support (v1.33.3+k3s1)
- Added new Helm role for Kubernetes package management
- Added new Fleet role for Rancher Fleet GitOps management
- Added new Tailscale role with support for all ProxyGroup types (ingress, egress, kube-apiserver)
- Added GitHub issue templates (bug report, documentation, feature request)
- Added GitHub pull request template
- Added comprehensive documentation (AGENTS.md, CONTRIBUTING.md, CLAUDE.md)
- Added filter plugins for Fleet management with 15 unit tests
- Added CI/CD workflow with integrated linting and testing
- Added Molecule tests for Docker and K3s roles
- Added integration tests for Docker and K3s roles
- Added argument_specs.yml for all roles with complete variable documentation
- Added K3s security hardening (SELinux, AppArmor) with auto-detection
- Added K3s auto-facts collection with caching
- Added K3s private registry configuration support
- Added logrotate configuration for K3s logs
- Added EditorConfig for consistent code style
- Added yamllint configuration
- Added pytest configuration
- Added Renovate for automated dependency management
- Added CODEOWNERS file

### Changed

- Updated README to include all 8 roles
- Updated copyright years to 2023-2026 across all files
- Updated ansible-lint configuration to use extended profile
- Updated Docker platform support to EL 8/9
- Updated all roles to use FQCN (Fully Qualified Collection Names)
- Improved role READMEs with links to guide.arillso.io
- Consolidated all tests (unit, molecule, integration) into single CI workflow
- Reduced comments in defaults/main.yml files for better readability
- Refactored Tailscale role to support unified ProxyGroup management

### Removed

- Removed deprecated docker_compose v1 role (migrate to docker_compose_v2)
- Removed dependabot configuration (replaced by Renovate)
- Removed pre-commit configuration
- Removed separate linter workflow (integrated into ci.yml)
- Removed RHEL 7 support from Docker role

### Fixed

- Fixed all YAML linting issues (document-start, comments-indentation, line-length)
- Fixed all ansible-lint violations (FQCN, schema, task-key-order)
- Fixed ansible-test sanity errors (shebangs, empty-init)
- Fixed platform schema validation for Ansible Galaxy
- Fixed Jinja2 template shebangs to avoid sanity errors
- Fixed license header consistency (MIT throughout)

## [0.0.7] - 2024-02-16

### Added

- Added meta documentation

## [0.0.6] - 2024-02-16

### Fixed

- Fixed docker-compose v2 scale functionality

### Changed

- Updated super-linter from version 5 to 6

## [0.0.5] - 2024-02-12

### Added

- Added docker_compose_v2 role for Docker Compose v2 support

## [0.0.4] - 2023-11-29

### Added

- Initial collection structure with docker role
- Added docker_compose role
- Added docker_login role
- Added k3s role
- Added fleet role
- Added helm role
- Added tailscale role

## [0.0.3] - 2023-11-29

### Changed

- Collection metadata improvements

## [0.0.2] - 2023-11-18

### Changed

- Role refinements and bug fixes

## [0.0.1] - 2023-11-12

### Added

- Initial release of arillso.container collection
- Basic collection structure
- Initial CI/CD workflows
