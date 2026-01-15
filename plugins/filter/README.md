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

- **Location:** `plugins/filter/fleet_filters.py`
- **Documentation:**
    - Python module: DOCUMENTATION, EXAMPLES, and RETURN sections
    - YAML format: `DOCUMENTATION.yml` for collection integration
- **Python Version:** Compatible with Python 3.6+
- **Dependencies:** No external dependencies required
- **Unit Tests:** `tests/unit/plugins/filter/test_fleet_filters.py`

## Documentation

Detailed filter documentation is available in multiple formats:

- **YAML Documentation:** [DOCUMENTATION.yml](DOCUMENTATION.yml) - Structured documentation for the collection
- **Python Docstrings:** Inline documentation in [fleet_filters.py](fleet_filters.py)
- **README:** This file provides usage examples and integration guidance

## References

- [Ansible Filter Plugins Documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#filter-plugins)
- [Fleet API Documentation](https://fleet.rancher.io/)
- [arillso.container.fleet Role](../../roles/fleet/README.md)

## License

MIT License

See [LICENSE](../../LICENSE) for the full license text.
