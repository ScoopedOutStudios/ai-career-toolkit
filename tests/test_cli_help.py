"""Smoke tests: every CLI subcommand responds to --help with exit code 0."""

from __future__ import annotations

import subprocess
import sys

import pytest

_SUBCOMMANDS = ["init", "verify", "install", "personalize"]


@pytest.mark.parametrize("cmd", [None, *_SUBCOMMANDS])
def test_help_exits_zero(cmd: str | None):
    args = [sys.executable, "-m", "ai_career_toolkit.cli", "--help"]
    if cmd is not None:
        args = [sys.executable, "-m", "ai_career_toolkit.cli", cmd, "--help"]
    result = subprocess.run(args, capture_output=True, text=True)
    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"


def test_version():
    result = subprocess.run(
        [sys.executable, "-m", "ai_career_toolkit.cli", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "ai-career-toolkit" in result.stdout
