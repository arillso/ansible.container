# arillso.container.docker_compose

This Ansible role is tailored for the configuration and management of Docker Compose environments.
It provides a customizable approach for Docker Compose setups across various systems.

## Requirements

- **Ansible Version**: 2.15 or higher
- **Permissions**: Necessary rights to access and manage target systems

## Role Variables

Variables are defined in `defaults/main.yml` and can be overridden in your playbook for specific needs. Key variables include:

### Docker Compose Configuration

#### Argument Specifications

- `docker_compose_version`: Specifies Docker Compose version to install (defaults to latest)
- `docker_compose_package`: List of Docker Compose packages for installation
- `docker_compose_directory_path`: Base directory path for Docker Compose configuration files
- `docker_compose_directory`: Full path for the Docker Compose project directory
- `docker_compose_use_file`: Boolean to choose between file-based or inline configuration
- `docker_compose_config`: Inline Docker Compose configuration as YAML string
- `docker_compose_project`: Name of the Docker Compose project
- `docker_compose_api_version`: Docker API version ('auto' for automatic)
- `docker_compose_build`: Option to build images before starting services
- `docker_compose_ca_cert`: CA certificate path for server verification
- `docker_compose_client_cert`: Client's TLS certificate path
- `docker_compose_client_key`: Client's TLS key path
- `docker_compose_debug`: Toggle for debug mode
- `docker_compose_dependencies`: Include/exclude linked services
- `docker_compose_docker_host`: Docker host URL or Unix socket path
- `docker_compose_env_file`: Custom environment file path
- `docker_compose_files`: Override default `docker-compose.yml` with a list of filenames
- `docker_compose_hostname_check`: Check Docker daemon's hostname against client certificate
- `docker_compose_nocache`: Control cache use during image build
- `docker_compose_profiles`: Profiles to activate when starting services
- `docker_compose_project_name`: Custom name for the Docker Compose project
- `docker_compose_pull`: Always pull images before starting
- `docker_compose_recreate`: Container recreation strategy ('always', 'never', 'smart')
- `docker_compose_remove_images`: Remove images when state is 'absent'
- `docker_compose_remove_orphans`: Remove containers not defined in Compose file
- `docker_compose_remove_volumes`: Remove data volumes when state is 'absent'
- `docker_compose_restarted`: Restart all containers when state is 'present'
- `docker_compose_scale`: Service scaling configuration
- `docker_compose_services`: List of specific services to operate on
- `docker_compose_ssl_version`: SSL version for secure communication
- `docker_compose_state`: Desired state of the Docker Compose project
- `docker_compose_stopped`: Stop all containers when state is 'present'
- `docker_compose_timeout`: Timeout for container shutdown operations (seconds)
- `docker_compose_tls`: Use TLS for API connection without server authenticity verification
- `docker_compose_tls_hostname`: Expected hostname for Docker Host server TLS verification
- `docker_compose_use_ssh_client`: Enable SSH client for Docker API communication
- `docker_compose_validate_certs`: Verify Docker host server authenticity with TLS

## Documentation

For detailed information and advanced usage, refer to our comprehensive guide:

[Arillso Docker Compose Guide](https://guide.arillso.io/collections/arillso/container/docker_compose.html#ansible-collections-arillso-container-docker-compose-role)

## Dependencies

This role operates independently without external dependencies.

## Example Playbook

Example demonstrating this role's usage:

```yaml
- hosts: servers
  become: true
  roles:
    - arillso.container.docker_compose
  vars:
    docker_compose_version: "1.29.2"
    docker_compose_use_file: true
    docker_compose_project: "my_project"
```
