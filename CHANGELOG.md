# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
