# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added LICENSE (MIT)
- Added .editorconfig for editor consistency
- Added .gitignore for repository cleanliness
- Added .github/CODEOWNERS
- Added .github/renovate.json for automated dependency updates
- Added AGENTS.md for AI agent documentation
- Added CLAUDE.md for Claude integration
- Added CHANGELOG.md for version tracking
- Added comprehensive README with all 8 roles
- Added CONTRIBUTING.md for development guidelines
- Added integration tests for Docker and K3s roles
- Added Molecule tests for Docker and K3s roles
- Added unit tests for filter plugins (15 test cases)
- Added DOCUMENTATION.yml for filter plugins
- Added pytest configuration (pytest.ini)
- Added support for all three Tailscale ProxyGroup types (ingress, egress, kube-apiserver)
- Added tailscale_ingress_services for LoadBalancer and Ingress resources
- Added IP-based access support for Tailscale egress services

### Changed

- Updated main README to include all roles (docker, docker_compose, docker_compose_v2, docker_login, k3s, fleet, helm, tailscale)
- Updated requirements.txt with comprehensive development dependencies
- Updated filter plugin README with YAML documentation reference
- Updated copyright years to 2023-2026 across all files
- Updated example dates in K3s autonomous deployment documentation to 2026
- Improved inline documentation consistency
- Consolidated all tests (unit, molecule, integration) into single CI workflow
- Enabled integration tests in CI workflow
- Reduced comments in all roles defaults/main.yml files for better readability
- Added Renovate version management for Docker (27.5.1), Docker Compose (2.32.4), and K3s (v1.33.3+k3s1)
- Refactored Tailscale role to support unified ProxyGroup management (all three types)
- Renamed tailscale_egress_proxygroup and tailscale_ingress_proxygroup to tailscale_proxygroups (unified list)
- Updated Tailscale role README with examples for all three ProxyGroup types
- Updated AGENTS.md to match organization standards with complete structure documentation

### Added

- Re-enabled k3s private registry configuration support
- Re-enabled k3s security hardening (SELinux/AppArmor) with auto-detection
- Added logrotate configuration template for k3s logs

### Removed

- Removed IMPROVEMENTS.md (redundant with CHANGELOG)
- Removed AUTONOMOUS_DEPLOYMENT.md from k3s role (belongs on guide.arillso.io)
- Removed commented-out token storage code (not needed)

### Fixed

- Fixed license header consistency (MIT throughout)
- Cleaned up commented code sections in k3s role

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
