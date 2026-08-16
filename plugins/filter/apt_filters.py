# -*- coding: utf-8 -*-

# Copyright: (c) 2024-2026, Arillso
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
name: apt_version_pin
version_added: "2.0.0"
short_description: Resolve an apt version pin from apt-cache madison output
description:
    - Picks the full apt version string for a marketing version out of C(apt-cache madison) output.
    - apt matches an C(=) pin against the full version string, which carries an
      optional epoch and a distro release suffix, and it does not expand globs
      in that pin.
    - A bare pin such as C(docker-ce=29.7.2) therefore never resolves, and neither does C(docker-ce=*29.7.2-*); only the string madison prints does.
    - Returns C(None) when the version is not in the repository, so the calling task can fail with a readable message instead of a Python traceback.
options:
    _input:
        description:
            - Lines of C(apt-cache madison <package>) output, typically C(stdout_lines) of the command.
            - Each line looks like C(<package> | <version> | <repository>); only the middle field is read.
        type: list
        elements: str
        required: true
    version:
        description:
            - The marketing version to resolve, for example C(29.7.2) or C(5.4.0).
            - Matched on C((^|:)<version>-) so the version either opens the
              string or follows the epoch colon, and the trailing hyphen keeps
              C(29.7.1) from taking C(29.7.10) and rejects a bare prefix like
              C(29.7).
            - Dots are matched literally, so C(5.4.0) does not also match a C(5X4X0) build.
        type: str
        required: true
author:
    - Arillso
notes:
    - The filter never raises on a missing version; the readable error belongs in an C(ansible.builtin.fail) task.
'''

EXAMPLES = r'''
# Resolve the exact apt version string before pinning it
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
  # Returns e.g. 5.4.0-1~ubuntu.24.04~noble, or None when the repository
  # no longer carries the version.
'''

RETURN = r'''
_value:
    description:
        - The full apt version string, epoch and distro suffix included.
        - C(None) when no line matches the requested version.
    type: str
'''

import re

# madison prints "<pkg> | <version> | <repo>"; take the middle field.
_MADISON_LINE = re.compile(r'^[^|]*\|\s*([^|]+?)\s*\|')


def apt_version_pin(lines, version):
    """
    Resolve the full apt version string for a marketing version.

    Args:
        lines: Lines of `apt-cache madison <package>` output
        version: The marketing version to look for, e.g. "5.4.0"

    Returns:
        The full version string, or None when the version is not offered
    """
    if not lines or not version:
        return None

    # The version either opens the string or follows the epoch colon. The
    # trailing hyphen keeps 29.7.1 from taking 29.7.10 and rejects a bare
    # prefix like "29.7"; re.escape keeps the dots literal, without it
    # "5.4.0" would also match a "5X4X0" build.
    wanted = re.compile(r'(^|:)' + re.escape(str(version)) + r'-')

    for line in lines:
        match = _MADISON_LINE.match(line)
        if not match:
            continue
        candidate = match.group(1)
        if wanted.search(candidate):
            return candidate

    return None


class FilterModule:
    """Ansible filter module for apt version pinning."""

    def filters(self):
        return {
            'apt_version_pin': apt_version_pin,
        }
