# -*- coding: utf-8 -*-

# Copyright: (c) 2024-2026, Arillso
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

"""Guards the EL (RedHat family) support declared in meta/main.yml.

Every role advertises EL 9, so every role must also test it and the docker
role must resolve real RedHat package vars. These checks are static: they
read the repo, not a live host, so they run without qemu or a cluster.

Parsing is deliberately line-based instead of using PyYAML, because
`ansible-test units` runs without a tests/unit/requirements.txt and PyYAML
is therefore not a guaranteed import in that environment.
"""

import re
from pathlib import Path

import pytest

# No pytest markers here: `ansible-test units` runs pytest with
# --strict-markers against its own config, which does not know the
# markers declared in pyproject.toml, and collection would fail.

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ROLES = sorted(p.name for p in (REPO_ROOT / "roles").iterdir() if p.is_dir())

# Facts a Rocky 9 GenericCloud host reports, used to replay the
# with_first_found lookups in roles/docker/tasks/main.yml.
ROCKY_FACTS = {
    "distribution": "Rocky",
    "distribution_version": "9.6",
    "distribution_major_version": "9",
    "os_family": "RedHat",
    "system": "Linux",
}


def read(*parts):
    return (REPO_ROOT.joinpath(*parts)).read_text()


def molecule_text(role):
    return read("roles", role, "molecule", "default", "molecule.yml")


def platform_names(role):
    """Platform entries are `- name: <x>` inside the platforms: block."""
    text = molecule_text(role)
    block = text.split("platforms:", 1)[1].split("\nprovisioner:", 1)[0]
    return re.findall(r"^\s+- name:\s*(\S+)", block, re.MULTILINE)


def host_var_names(role):
    """host_vars keys are `<name>:` inside the host_vars: block."""
    text = molecule_text(role)
    block = text.split("host_vars:", 1)[1].split("playbooks:", 1)[0]
    return re.findall(r"^\s+(\S+):\s*$", block, re.MULTILINE)


def ssh_ports(role):
    text = molecule_text(role)
    block = text.split("platforms:", 1)[1].split("\nprovisioner:", 1)[0]
    return re.findall(r"network_ssh_port:\s*(\d+)", block)


def el_versions(role):
    """Versions listed under the `- name: EL` platform in meta/main.yml.

    Returns None when the role does not declare EL at all.
    """
    text = read("roles", role, "meta", "main.yml")
    match = re.search(r"- name: EL\n\s+versions:\n((?:\s+- .*\n)+)", text)
    if not match:
        return None
    return re.findall(r'-\s*"?([^"\s]+)"?', match.group(1))


def first_found(directory, candidates):
    """Mirror ansible.builtin.first_found: first existing file wins."""
    for name in candidates:
        if (REPO_ROOT / directory / name).exists():
            return name
    return None


@pytest.mark.parametrize("role", ROLES)
def test_el_declaration_is_backed_by_a_redhat_platform(role):
    """A role may only advertise EL if its molecule matrix runs one."""
    if el_versions(role) is None:
        pytest.skip(f"{role} does not declare EL")

    names = platform_names(role)
    assert any("rocky" in n for n in names), (
        f"{role} declares EL in meta/main.yml but tests no RedHat-family platform: {names}"
    )


@pytest.mark.parametrize("role", ROLES)
def test_declared_el_versions_are_tested(role):
    """Only EL 9 is in the matrix, so only EL 9 may be advertised."""
    versions = el_versions(role)
    if versions is None:
        pytest.skip(f"{role} does not declare EL")
    assert versions == ["9"], f"{role} advertises untested EL versions: {versions}"


@pytest.mark.parametrize("role", ROLES)
def test_every_platform_has_host_vars_and_a_unique_port(role):
    """A platform without host_vars or with a clashing port never boots."""
    names = sorted(platform_names(role))
    host_vars = sorted(host_var_names(role))
    assert names == host_vars, f"{role}: platforms {names} != host_vars {host_vars}"

    ports = ssh_ports(role)
    assert len(ports) == len(names), f"{role}: {len(names)} platforms but {len(ports)} ports"
    assert len(ports) == len(set(ports)), f"{role}: duplicate ssh ports {ports}"


@pytest.mark.parametrize("role", ROLES)
def test_molecule_playbooks_install_packages_portably(role):
    """`apt` installs silently skip or hard-fail on the RedHat family.

    A bare `update_cache` refresh stays allowed — `package` cannot refresh
    apt metadata — but it must be guarded to the Debian family, and it must
    not install anything.
    """
    scenario = REPO_ROOT / "roles" / role / "molecule"
    offenders = []
    for path in sorted(scenario.rglob("*.yml")):
        text = path.read_text()
        for task in re.findall(
            r"ansible\.builtin\.apt:\n((?:\s+\S.*\n)+?)(?=\s*(?:-\s|\w)|\Z)", text
        ):
            installs = "name:" in task
            guarded = 'os_family\'] == "Debian"' in text or 'os_family == "Debian"' in text
            if installs or not guarded:
                offenders.append(path.relative_to(REPO_ROOT).as_posix())
    assert not offenders, (
        f"{role}: install via ansible.builtin.package; apt only for a "
        f"Debian-guarded cache refresh — offenders: {offenders}"
    )


def test_rocky_resolves_to_the_redhat_vars_and_tasks():
    """Without vars/RedHat.yml, first_found falls through to the empty
    defaults.yml, docker_package stays undefined and the install task dies."""
    facts = ROCKY_FACTS
    vars_hit = first_found(
        "roles/docker/vars",
        [
            f"{facts['distribution']}-{facts['distribution_version']}.yml",
            f"{facts['distribution']}-{facts['distribution_major_version']}.yml",
            f"{facts['distribution']}.yml",
            f"{facts['os_family']}.yml",
            f"{facts['system']}.yml",
            "defaults.yml",
        ],
    )
    assert vars_hit == "RedHat.yml", f"Rocky resolved vars to {vars_hit}"

    tasks_hit = first_found(
        "roles/docker/tasks",
        [
            f"install_docker_{facts['distribution'].lower()}_{facts['distribution_version']}.yml",
            f"install_docker_{facts['distribution'].lower()}"
            f"_{facts['distribution_major_version']}.yml",
            f"install_docker_{facts['distribution'].lower()}.yml",
            f"install_docker_{facts['os_family'].lower()}.yml",
            f"install_docker_{facts['system'].lower()}.yml",
            "defaults.yml",
        ],
    )
    assert tasks_hit == "install_docker_redhat.yml", f"Rocky resolved tasks to {tasks_hit}"


def test_redhat_vars_pin_uses_rpm_compatible_wildcard():
    """RPM version strings carry epoch and release parts, so an exact
    `docker-ce-<version>` pin never matches; the wildcard suffix does."""
    text = read("roles", "docker", "vars", "RedHat.yml")
    # compare package entries only; comments mention names they must not install
    entries = [
        line.strip().lstrip("-").strip()
        for line in text.splitlines()
        if line.strip().startswith("-")
    ]
    assert any("docker-ce-' + docker_version + '*" in e for e in entries), entries
    # apt syntax in a RedHat vars file would break dnf
    assert not any("docker-ce=" in e for e in entries), entries
    # the EL repos ship no python3-docker, and pip is not the SDK, so the
    # role installs neither; scenarios that need the SDK install it
    assert "python3-docker" not in entries, entries
    assert "python3-pip" not in entries, entries
