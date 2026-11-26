# Copyright: (c) 2024-2026, Arillso
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

"""Keeps every role's argument_specs.yml in step with defaults/main.yml.

The `default:` in the spec is documentation only: the value a play gets
comes from defaults/main.yml, while antsibull-docs renders the spec on
the role page. Nothing else keeps the two copies equal, so a missing or
drifted spec default silently misdocuments the role.

Values are compared as raw YAML: a Jinja default must appear verbatim,
not resolved. `ansible-test units` runs without a
tests/unit/requirements.txt, so PyYAML is not a guaranteed import there;
the module skips instead of failing collection.
"""

import re
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

# No pytest markers here: `ansible-test units` runs pytest with
# --strict-markers against its own config, which does not know the
# markers declared in pyproject.toml, and collection would fail.

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

ROLES = sorted(p.name for p in (REPO_ROOT / "roles").iterdir() if p.is_dir())


def load(*parts):
    return yaml.safe_load(REPO_ROOT.joinpath(*parts).read_text())


def role_defaults(role):
    path = REPO_ROOT / "roles" / role / "defaults" / "main.yml"
    return (load("roles", role, "defaults", "main.yml") or {}) if path.exists() else {}


def main_spec(role):
    path = REPO_ROOT / "roles" / role / "meta" / "argument_specs.yml"
    assert path.exists(), f"{role}: meta/argument_specs.yml missing"
    return load("roles", role, "meta", "argument_specs.yml")["argument_specs"]["main"]


@pytest.mark.parametrize("role", ROLES)
def test_defaults_documented_in_argument_specs(role):
    """Every role default is declared, optional and documented with its value."""
    defaults = role_defaults(role)
    options = main_spec(role)["options"]
    for name, value in defaults.items():
        assert name in options, f"{role}: {name} not declared"
        opt = options[name] or {}
        assert not opt.get("required"), f"{role}: {name} is required but has a role default"
        assert "default" in opt, f"{role}: {name} has no default in argument_specs"
        assert opt["default"] == value, f"{role}: {name} default drifted"


@pytest.mark.parametrize("role", ROLES)
def test_examples_use_declared_options(role):
    """antsibull-docs renders `examples` on the role page; keep them valid.

    An example that sets an undeclared variable documents an option the
    role does not have. Only the top-level role `vars` keys are checked,
    not sub-options.
    """
    spec = main_spec(role)
    assert isinstance(spec.get("examples"), str) and spec["examples"].strip(), (
        f"{role}: main entry point has no examples"
    )
    plays = yaml.safe_load(spec["examples"])
    entries = [
        r
        for play in plays
        for r in play.get("roles", [])
        if isinstance(r, dict) and r.get("role") == f"arillso.container.{role}"
    ]
    assert entries, f"{role}: example does not call arillso.container.{role}"
    for entry in entries:
        unknown = set(entry.get("vars", {})) - set(spec["options"])
        assert not unknown, f"{role}: example uses undeclared {sorted(unknown)}"


def quick_start_blocks(role):
    """Return the yaml code blocks of the README `## Quick Start` section."""
    text = (REPO_ROOT / "roles" / role / "README.md").read_text()
    section = re.search(r"^## Quick Start\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert section, f"{role}: README has no '## Quick Start' section"
    blocks = re.findall(r"^```ya?ml\n(.*?)^```", section.group(1), re.M | re.S)
    assert blocks, f"{role}: README Quick Start has no yaml block"
    return blocks


@pytest.mark.parametrize("role", ROLES)
def test_readme_quick_start_uses_declared_options(role):
    """A Quick Start that sets an undeclared variable is silently ignored.

    Role argument specs do not reject unknown variables, so a copied
    Quick Start runs but drops the setting. Only the top-level role
    `vars` keys are checked, not sub-options.
    """
    options = set(main_spec(role)["options"])
    for block in quick_start_blocks(role):
        for play in yaml.safe_load(block):
            for entry in play.get("roles", []):
                if not isinstance(entry, dict) or entry.get("role") != f"arillso.container.{role}":
                    continue
                unknown = set(entry.get("vars", {})) - options
                assert not unknown, f"{role}: Quick Start uses undeclared {sorted(unknown)}"


@pytest.mark.parametrize("role", ROLES)
def test_entry_points_have_task_files(role):
    """`tasks_from: <entry point>` fails when tasks/<entry point>.yml is missing."""
    specs = load("roles", role, "meta", "argument_specs.yml")["argument_specs"]
    tasks = REPO_ROOT / "roles" / role / "tasks"
    missing = sorted(
        name for name in specs if name != "main" and not (tasks / f"{name}.yml").exists()
    )
    assert not missing, f"{role}: entry points without task file {missing}"
