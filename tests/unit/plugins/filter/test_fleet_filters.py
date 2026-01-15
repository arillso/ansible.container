# -*- coding: utf-8 -*-

# Copyright: (c) 2024-2026, Arillso
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

"""Unit tests for fleet_filters plugin."""

import pytest
import sys
from pathlib import Path

# Add the plugins directory to the path
plugins_path = Path(__file__).parent.parent.parent.parent.parent / "plugins" / "filter"
sys.path.insert(0, str(plugins_path))

from fleet_filters import to_camel_case, transform_fleet_targets


class TestToCamelCase:
    """Test cases for to_camel_case function."""

    def test_simple_snake_case(self):
        """Test simple snake_case conversion."""
        assert to_camel_case("hello_world") == "helloWorld"

    def test_multiple_underscores(self):
        """Test snake_case with multiple underscores."""
        assert to_camel_case("cluster_selector_name") == "clusterSelectorName"

    def test_single_word(self):
        """Test single word without underscores."""
        assert to_camel_case("cluster") == "cluster"

    def test_common_fleet_fields(self):
        """Test common Fleet API field names."""
        assert to_camel_case("cluster_selector") == "clusterSelector"
        assert to_camel_case("match_labels") == "matchLabels"
        assert to_camel_case("match_expressions") == "matchExpressions"
        assert to_camel_case("cluster_name") == "clusterName"
        assert to_camel_case("cluster_group") == "clusterGroup"
        assert to_camel_case("target_namespace") == "targetNamespace"


class TestTransformFleetTargets:
    """Test cases for transform_fleet_targets function."""

    def test_empty_list(self):
        """Test with empty list."""
        result = transform_fleet_targets([])
        assert result == []

    def test_none_input(self):
        """Test with None input."""
        result = transform_fleet_targets(None)
        assert result is None

    def test_simple_target(self):
        """Test simple target transformation."""
        targets = [
            {
                "cluster_name": "production"
            }
        ]
        expected = [
            {
                "clusterName": "production"
            }
        ]
        result = transform_fleet_targets(targets)
        assert result == expected

    def test_cluster_selector_with_labels(self):
        """Test cluster_selector with match_labels."""
        targets = [
            {
                "cluster_selector": {
                    "match_labels": {
                        "environment": "production",
                        "region": "us-west"
                    }
                }
            }
        ]
        expected = [
            {
                "clusterSelector": {
                    "matchLabels": {
                        "environment": "production",
                        "region": "us-west"
                    }
                }
            }
        ]
        result = transform_fleet_targets(targets)
        assert result == expected

    def test_cluster_selector_with_expressions(self):
        """Test cluster_selector with match_expressions."""
        targets = [
            {
                "cluster_selector": {
                    "match_expressions": [
                        {
                            "key": "provider",
                            "operator": "In",
                            "values": ["k3s", "eks"]
                        }
                    ]
                }
            }
        ]
        expected = [
            {
                "clusterSelector": {
                    "matchExpressions": [
                        {
                            "key": "provider",
                            "operator": "In",
                            "values": ["k3s", "eks"]
                        }
                    ]
                }
            }
        ]
        result = transform_fleet_targets(targets)
        assert result == expected

    def test_multiple_targets(self):
        """Test multiple targets with different types."""
        targets = [
            {
                "cluster_selector": {
                    "match_labels": {
                        "tier": "frontend"
                    }
                }
            },
            {
                "cluster_name": "production-cluster"
            },
            {
                "cluster_group": "staging-group"
            }
        ]
        expected = [
            {
                "clusterSelector": {
                    "matchLabels": {
                        "tier": "frontend"
                    }
                }
            },
            {
                "clusterName": "production-cluster"
            },
            {
                "clusterGroup": "staging-group"
            }
        ]
        result = transform_fleet_targets(targets)
        assert result == expected

    def test_nested_structure(self):
        """Test deeply nested structure transformation."""
        targets = [
            {
                "cluster_selector": {
                    "match_labels": {
                        "env": "prod"
                    },
                    "match_expressions": [
                        {
                            "key": "type",
                            "operator": "NotIn",
                            "values": ["test"]
                        }
                    ]
                },
                "target_namespace": "default"
            }
        ]
        expected = [
            {
                "clusterSelector": {
                    "matchLabels": {
                        "env": "prod"
                    },
                    "matchExpressions": [
                        {
                            "key": "type",
                            "operator": "NotIn",
                            "values": ["test"]
                        }
                    ]
                },
                "targetNamespace": "default"
            }
        ]
        result = transform_fleet_targets(targets)
        assert result == expected

    def test_preserves_values(self):
        """Test that values are preserved unchanged."""
        targets = [
            {
                "cluster_name": "test_cluster_with_underscores"
            }
        ]
        result = transform_fleet_targets(targets)
        # Key should be transformed, but value should remain unchanged
        assert result[0]["clusterName"] == "test_cluster_with_underscores"

    def test_list_of_strings_preserved(self):
        """Test that lists of strings are preserved."""
        targets = [
            {
                "match_expressions": [
                    {
                        "values": ["value_one", "value_two"]
                    }
                ]
            }
        ]
        result = transform_fleet_targets(targets)
        # String values in lists should not be transformed
        assert result[0]["matchExpressions"][0]["values"] == ["value_one", "value_two"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
