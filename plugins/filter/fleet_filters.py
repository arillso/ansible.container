# -*- coding: utf-8 -*-

# Copyright: (c) 2024-2026, Arillso
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
name: fleet_transform_targets
version_added: "1.0.0"
short_description: Transform Fleet targets from snake_case to camelCase
description:
    - Converts Fleet target configurations from Ansible's snake_case convention to Fleet API's camelCase format.
    - Recursively transforms all nested dictionary keys.
    - Handles complex structures including cluster_selector, match_labels, match_expressions, etc.
    - Preserves all values and structure while only changing key names.
options:
    _input:
        description:
            - List of target dictionaries with snake_case keys.
            - Typically contains cluster_selector, cluster_name, cluster_group, etc.
        type: list
        elements: dict
        required: true
author:
    - Arillso
notes:
    - This filter is specifically designed for Fleet GitOps target configurations.
    - Common transformations include cluster_selector -> clusterSelector, match_labels -> matchLabels.
'''

EXAMPLES = r'''
# Transform Fleet targets in a GitRepo configuration
- name: Apply GitRepo with transformed targets
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

# Result will transform to:
#   targets:
#       - clusterSelector:
#             matchLabels:
#                 environment: production
#                 region: us-west

# Multiple targets with different selectors
- name: Configure multi-cluster deployment
  set_fact:
      transformed_targets: "{{ fleet_targets | arillso.container.fleet_transform_targets }}"
  vars:
      fleet_targets:
          - cluster_selector:
                match_labels:
                    tier: frontend
          - cluster_name: production-cluster
          - cluster_group: staging-group
'''

RETURN = r'''
_value:
    description: List of target dictionaries with camelCase keys suitable for Fleet API.
    type: list
    elements: dict
    returned: always
'''

DOCUMENTATION_TO_CAMEL = r'''
---
name: to_camel_case
version_added: "1.0.0"
short_description: Convert snake_case string to camelCase
description:
    - Converts a snake_case string to camelCase format.
    - Useful for transforming Ansible variable names to API-compatible formats.
    - Preserves the first word in lowercase and capitalizes the first letter of subsequent words.
options:
    _input:
        description:
            - String in snake_case format to be converted.
        type: string
        required: true
author:
    - Arillso
'''

EXAMPLES_TO_CAMEL = r'''
# Convert a single string
- name: Transform variable name
  debug:
      msg: "{{ 'cluster_selector' | arillso.container.to_camel_case }}"
  # Returns: clusterSelector

# Use in variable transformation
- name: Create API payload
  set_fact:
      api_field: "{{ field_name | arillso.container.to_camel_case }}"
  vars:
      field_name: "match_labels"
  # Results in: matchLabels
'''

RETURN_TO_CAMEL = r'''
_value:
    description: String converted to camelCase format.
    type: string
    returned: always
'''


def to_camel_case(snake_str):
    """
    Convert snake_case string to camelCase.

    Args:
        snake_str: String in snake_case format

    Returns:
        String in camelCase format
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def transform_fleet_targets(targets):
    """
    Transform Fleet targets from snake_case to camelCase.
    Handles nested structures recursively.

    Args:
        targets: List of target dictionaries with snake_case keys

    Returns:
        List of target dictionaries with camelCase keys
    """
    if not targets or not isinstance(targets, list):
        return targets

    def transform_dict(d):
        """Recursively transform dictionary keys from snake_case to camelCase."""
        if not isinstance(d, dict):
            return d

        result = {}
        for key, value in d.items():
            # Transform the key to camelCase
            new_key = to_camel_case(key)

            # Recursively transform nested dictionaries
            if isinstance(value, dict):
                result[new_key] = transform_dict(value)
            elif isinstance(value, list):
                result[new_key] = [transform_dict(item) if isinstance(item, dict) else item for item in value]
            else:
                result[new_key] = value

        return result

    return [transform_dict(target) for target in targets]


class FilterModule:
    """Ansible filter module for Fleet transformations."""

    def filters(self):
        return {
            'fleet_transform_targets': transform_fleet_targets,
            'to_camel_case': to_camel_case,
        }
