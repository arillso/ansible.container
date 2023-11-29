# arillso.container.docker_login

This Ansible role facilitates Docker registry logins, offering a streamlined authentication process with customizable settings for various environments.

## Requirements

- **Ansible Version**: 2.15 or higher
- **Permissions**: Adequate rights to manage Docker configurations on target machines

## Role Variables

Defined in `defaults/main.yml`, these variables can be customized in your playbook. Key variables include:

- `docker_login_api_version`: Docker API version
- `docker_login_ca_cert`: CA certificate path for server verification
- `docker_login_client_cert`: Client's TLS certificate path
- `docker_login_client_key`: Client's TLS key path
- `docker_login_config_path`: Custom path for Docker CLI configuration
- `docker_login_debug`: Debug mode toggle
- `docker_login_docker_host`: Docker API connection URL or Unix socket
- `docker_login_password`: Registry account password (plaintext)
- `docker_login_reauthorize`: Refresh existing authentication token
- `docker_login_registry_url`: Docker registry URL
- `docker_login_ssl_version`: SSL version for secure communication
- `docker_login_state`: User state ('present' or 'absent')
- `docker_login_timeout`: API response timeout (seconds)
- `docker_login_tls`: Toggle for TLS in API connection
- `docker_login_tls_hostname`: Expected Docker Host server name for TLS
- `docker_login_username`: Registry account username
- `docker_login_validate_certs`: Docker host server authenticity verification

## Documentation

For detailed information and advanced usage, refer to our comprehensive guide, covering topics like advanced configurations, best practices, and troubleshooting.

[Arillso Docker Login Guide](https://guide.arillso.io/collections/arillso/container/docker_login.html#ansible-collections-arillso-container-ocker-login-role)

## Dependencies

This role is self-contained with no external dependencies.

## Example Playbook

An example of using this role:

```yaml
- hosts: docker
  become: true
  roles:
    - arillso.container.docker_login
  vars:
    docker_login_username: "user123"
    docker_login_registry_url: "https://myregistry.com"
```
