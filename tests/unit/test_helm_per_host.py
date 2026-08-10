# Copyright: (c) 2024-2026, Arillso
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

"""Guards the per-host semantics of the helm role.

Every host the role runs against is its own k3s cluster: the role's own
default is `helm_target_host: "{{ inventory_hostname }}"`, the molecule
scenario installs k3s on every VM, and the sister roles fleet, k3s and
tailscale all run per host. A `run_once` anywhere in the role would apply
the HelmChart CRs to exactly one host and leave the other clusters empty.

The molecule scenario catches this too, but only in CI and only with two
booted VMs. These checks are static: they read the repo, not a live host,
so they run without qemu or a cluster.

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

HELM_TASKS = ["charts.yml", "main.yml", "prerequisites.yml", "repositories.yml"]

# Roles that manage a cluster and therefore share the per-host contract.
CLUSTER_ROLES = ["fleet", "helm", "k3s", "tailscale"]

# A directive, not a mention: `run_once:` as a task key, so the prose in a
# comment that explains why it is gone does not trip the assertion.
RUN_ONCE = re.compile(r"^\s+run_once:", re.MULTILINE)


def read(*parts):
    return (REPO_ROOT.joinpath(*parts)).read_text()


def run_once_lines(path):
    """1-based line numbers carrying a run_once directive."""
    text = path.read_text()
    return [i for i, line in enumerate(text.splitlines(), 1) if RUN_ONCE.match(line + "\n")]


@pytest.mark.parametrize("task_file", HELM_TASKS)
def test_helm_tasks_run_on_every_host(task_file):
    """One host per cluster: a skipped host never gets its HelmChart CR."""
    path = REPO_ROOT / "roles" / "helm" / "tasks" / task_file
    hits = run_once_lines(path)
    assert not hits, f"roles/helm/tasks/{task_file} carries run_once at lines {hits}"


def test_helm_verify_asserts_on_every_host():
    """Verify must cover both VMs, otherwise the scenario is not a gate.

    With run_once the verify simply followed the role onto whichever host
    ansible picked, so a role that skipped a cluster still passed.
    """
    path = REPO_ROOT / "roles" / "helm" / "molecule" / "default" / "verify.yml"
    hits = run_once_lines(path)
    assert not hits, f"verify.yml carries run_once at lines {hits}"
    assert re.search(
        r"^\s*hosts:\s*all\s*$", path.read_text(), re.MULTILINE
    ), "verify.yml must assert against hosts: all"


@pytest.mark.parametrize("role", CLUSTER_ROLES)
def test_cluster_roles_agree_on_per_host_execution(role):
    """helm must not be the odd one out among the cluster-facing roles."""
    tasks_dir = REPO_ROOT / "roles" / role / "tasks"
    offenders = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in tasks_dir.rglob("*.yml")
        if run_once_lines(path)
    )
    assert not offenders, f"{role} deviates from per-host execution: {offenders}"


def test_kubeconfig_autodetection_takes_the_first_match():
    """The task is named "first existing file" and must deliver that.

    A `set_fact` in a loop has no break: every matching candidate
    overwrites the previous one, so the *last* existing path wins. On a
    k3s server both /etc/rancher/k3s/k3s.yaml and /root/.kube/config
    exist, and the loop picks the wrong one. run_once used to mask this,
    because only one host ever ran the detection.
    """
    text = read("roles", "helm", "tasks", "prerequisites.yml")
    block = text.split('- name: "Set detected kubeconfig path', 1)[1].split("\n- name:", 1)[0]
    assert (
        "loop:" not in block
    ), "kubeconfig detection still loops over all candidates; the last match wins"
    assert "| first" in block, "detection must select the first existing candidate"


def test_kubeconfig_selection_survives_a_skipped_stat():
    """The stat task is conditional, so its items may carry no stat dict.

    Jinja resolves a dotted path left to right before the `defined` test
    runs, so `selectattr('stat.exists', 'defined')` alone raises
    UndefinedError on a skipped stat. The `stat`-level guard must come
    first.
    """
    text = read("roles", "helm", "tasks", "prerequisites.yml")
    assert (
        "selectattr('stat', 'defined')" in text
    ), "guard the stat dict itself before testing stat.exists"
