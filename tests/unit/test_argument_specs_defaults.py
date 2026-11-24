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
