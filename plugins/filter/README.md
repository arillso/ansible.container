# Arillso Container Collection - Filter Plugins

This directory contains custom Ansible filter plugins for the
`arillso.container` collection.

## Available Filters

### fleet_transform_targets

Transforms Fleet target configurations from Ansible's snake_case convention to
Fleet API's camelCase format.

**Purpose:** Fleet's Kubernetes API expects field names in camelCase (e.g.,
`clusterSelector`, `matchLabels`), while Ansible best practices recommend using
snake_case for variable names (e.g., `cluster_selector`, `match_labels`). This
filter automatically handles the transformation.

**Usage:**

```yaml
- name: Deploy GitRepo with transformed targets
  kubernetes.core.k8s:
      definition:
          apiVersion: fleet.cattle.io/v1alpha1
          kind: GitRepo
          spec:
              targets: "{{ my_targets | arillso.container.fleet_transform_targets }}"
  vars:
      my_targets:
          - cluster_selector:
                match_labels:
                    environment: production
                    region: us-west
```

**Input (snake_case):**

```yaml
- cluster_selector:
      match_labels:
          environment: production
      match_expressions:
          - key: region
            operator: In
            values: [us-west, us-east]
- cluster_name: my-cluster
- cluster_group: staging
```

**Output (camelCase):**

```yaml
- clusterSelector:
      matchLabels:
          environment: production
      matchExpressions:
          - key: region
            operator: In
            values: [us-west, us-east]
- clusterName: my-cluster
- clusterGroup: staging
```

**Features:**

- Recursive transformation of nested dictionaries
- Handles lists of dictionaries
- Preserves all values and structure
- Only transforms dictionary keys

**Common Transformations:**

| Input (snake_case)       | Output (camelCase)     |
| ------------------------ | ---------------------- |
| `cluster_selector`       | `clusterSelector`      |
| `cluster_name`           | `clusterName`          |
| `cluster_group`          | `clusterGroup`         |
| `cluster_group_selector` | `clusterGroupSelector` |
| `match_labels`           | `matchLabels`          |
| `match_expressions`      | `matchExpressions`     |

### to_camel_case

Converts a single snake_case string to camelCase format.

**Usage:**

```yaml
- name: Transform field name
  debug:
      msg: "{{ 'cluster_selector' | arillso.container.to_camel_case }}"
  # Output: clusterSelector

- name: Build API payload dynamically
  set_fact:
      api_field_name: "{{ input_field | arillso.container.to_camel_case }}"
  vars:
      input_field: "match_labels"
  # Results in: matchLabels
```

**Examples:**

| Input              | Output            |
| ------------------ | ----------------- |
| `cluster_selector` | `clusterSelector` |
| `match_labels`     | `matchLabels`     |
| `my_variable_name` | `myVariableName`  |
| `api_version`      | `apiVersion`      |

### apt_version_pin

Resolves the full apt version string for a marketing version out of
`apt-cache madison` output.

**Purpose:** apt matches an `=` pin against the _full_ version string, which
carries an optional epoch and a distro release suffix (e.g.
`5:29.7.2-1~ubuntu.24.04~noble`), and it does not expand globs in that pin. A
bare `docker-ce=29.7.2` therefore never resolves, and neither does
`docker-ce=*29.7.2-*` — only the string madison prints does. The filter picks
that string, so roles can pin an exact version without hand-rolling a regex in
Jinja.

The match anchors on `(^|:)<version>-`: the version either opens the string or
follows the epoch colon, and the trailing hyphen keeps `29.7.1` from taking
`29.7.10` and rejects a bare prefix like `29.7`. Dots are matched literally, so
`5.4.0` does not also match a `5X4X0` build.

**Usage:**

```yaml
- name: Resolve the apt version string for the pin
  ansible.builtin.command:
      cmd: apt-cache madison docker-compose-plugin
  register: compose_madison
  changed_when: false

- name: Set the resolved apt version string
  ansible.builtin.set_fact:
      docker_compose_v2_apt_version: >-
          {{ compose_madison.stdout_lines
             | arillso.container.apt_version_pin(docker_compose_v2_version) }}
```

The filter returns `none` when the repository no longer carries the version —
Docker drops old packages — instead of raising, so the calling role can fail
with a readable message rather than a Python traceback:

```yaml
- name: Fail when the pinned version is not in the repository
  ansible.builtin.fail:
      msg: "docker_compose_v2_version {{ docker_compose_v2_version }} is not available"
  when: docker_compose_v2_apt_version | length == 0
```

**Examples:**

| madison version            | Requested | Result                        |
| -------------------------- | --------- | ----------------------------- |
| `5.4.0-1~ubuntu.24.04~no…` | `5.4.0`   | `5.4.0-1~ubuntu.24.04~noble`  |
| `5:29.7.2-1~ubuntu.24.04…` | `29.7.2`  | `5:29.7.2-1~ubuntu.24.04~no…` |
| `5:29.7.10-1~ubuntu.24.0…` | `29.7.1`  | no match on this line         |
| any                        | `29.7`    | `none` (bare prefix)          |

## Integration with Fleet Role

These filters are automatically used by the `arillso.container.fleet` role when
managing GitRepos and Bundles. You can define your targets using snake_case
notation in your variables:

```yaml
# host_vars/my_host/fleet.yml
fleet_gitrepos:
    - name: my-gitrepo
      repository: git@github.com:org/repo.git
      targets:
          - cluster_selector:
                match_labels:
                    environment: production
```

The role automatically applies the transformation when creating Kubernetes
resources.

## Development

### Testing Filters

You can test these filters using ansible-playbook:

```yaml
- hosts: localhost
  gather_facts: false
  tasks:
      - name: Test fleet_transform_targets filter
        debug:
            msg: "{{ test_data | arillso.container.fleet_transform_targets }}"
        vars:
            test_data:
                - cluster_selector:
                      match_labels:
                          test: value
```

### Filter Implementation

The filters are implemented in Python and follow Ansible's filter plugin
conventions:

- **Location:** `plugins/filter/fleet_filters.py` (`fleet_transform_targets`, `to_camel_case`) and `plugins/filter/apt_filters.py` (`apt_version_pin`)
- **Documentation:** DOCUMENTATION, EXAMPLES, and RETURN sections in the Python module, plus `DOCUMENTATION.yml` for collection integration
- **Python Version:** Compatible with Python 3.6+
- **Dependencies:** No external dependencies required
- **Unit Tests:** `tests/unit/plugins/filter/test_fleet_filters.py` and `tests/unit/plugins/filter/test_apt_filters.py`

## Documentation

Detailed filter documentation is available in multiple formats:

- **YAML Documentation:** [DOCUMENTATION.yml](DOCUMENTATION.yml) - Structured documentation for the collection
- **Python Docstrings:** Inline documentation in [fleet_filters.py](fleet_filters.py) and [apt_filters.py](apt_filters.py)
- **README:** This file provides usage examples and integration guidance

## References

- [Ansible Filter Plugins Documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#filter-plugins)
- [Fleet API Documentation](https://fleet.rancher.io/)
- [arillso.container.fleet Role](../../roles/fleet/README.md)

## License

MIT License

See [LICENSE](../../LICENSE) for the full license text.
