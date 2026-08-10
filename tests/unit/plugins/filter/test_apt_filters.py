# -*- coding: utf-8 -*-

# Copyright: (c) 2024-2026, Arillso
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

"""Unit tests for apt_filters plugin.

The fixtures are real `apt-cache madison` output: docker-ce carries an epoch,
docker-compose-plugin does not, and both live in the same Docker repository.
"""

import sys
from pathlib import Path

# Add the plugins directory to the path
plugins_path = Path(__file__).parent.parent.parent.parent.parent / "plugins" / "filter"
sys.path.insert(0, str(plugins_path))

from apt_filters import apt_version_pin  # noqa: E402

# `apt-cache madison docker-compose-plugin` on Ubuntu 24.04 (no epoch).
COMPOSE_MADISON = [
    " docker-compose-plugin | 5.4.0-1~ubuntu.24.04~noble | "
    "https://download.docker.com/linux/ubuntu noble/stable amd64 Packages",
    " docker-compose-plugin | 5.3.0-1~ubuntu.24.04~noble | "
    "https://download.docker.com/linux/ubuntu noble/stable amd64 Packages",
]

# `apt-cache madison docker-ce` on Ubuntu 24.04 (epoch "5:").
DOCKER_MADISON = [
    " docker-ce | 5:29.7.10-1~ubuntu.24.04~noble | "
    "https://download.docker.com/linux/ubuntu noble/stable amd64 Packages",
    " docker-ce | 5:29.7.2-1~ubuntu.24.04~noble | "
    "https://download.docker.com/linux/ubuntu noble/stable amd64 Packages",
    " docker-ce | 5:29.7.1-1~ubuntu.24.04~noble | "
    "https://download.docker.com/linux/ubuntu noble/stable amd64 Packages",
]


def test_version_without_epoch_resolves_to_the_full_string():
    """docker-compose-plugin carries no epoch, so the version opens the string."""
    assert apt_version_pin(COMPOSE_MADISON, "5.4.0") == "5.4.0-1~ubuntu.24.04~noble"


def test_version_with_epoch_keeps_the_epoch():
    """apt matches the pin against the full string, epoch included."""
    assert apt_version_pin(DOCKER_MADISON, "29.7.2") == "5:29.7.2-1~ubuntu.24.04~noble"


def test_shorter_version_does_not_take_the_longer_one():
    """The trailing hyphen keeps 29.7.1 from resolving to 29.7.10."""
    assert apt_version_pin(DOCKER_MADISON, "29.7.1") == "5:29.7.1-1~ubuntu.24.04~noble"


def test_bare_prefix_does_not_resolve():
    """"29.7" is not a release; without the hyphen guard it would take one."""
    assert apt_version_pin(DOCKER_MADISON, "29.7") is None


def test_dots_are_literal():
    """Without regex escaping "5.4.0" would also match a "5X4X0" build."""
    weird = [
        " docker-compose-plugin | 5X4X0-1~ubuntu.24.04~noble | "
        "https://download.docker.com/linux/ubuntu noble/stable amd64 Packages",
    ]
    assert apt_version_pin(weird, "5.4.0") is None


def test_version_missing_from_the_repository_returns_none():
    """Docker drops old packages, so a pin stops resolving at some point."""
    assert apt_version_pin(COMPOSE_MADISON, "5.0.0") is None


def test_empty_line_list_returns_none():
    """A madison call that printed nothing must not raise."""
    assert apt_version_pin([], "5.4.0") is None


def test_empty_version_returns_none():
    """The unpinned branch never calls the filter, but it must not match all."""
    assert apt_version_pin(COMPOSE_MADISON, "") is None
