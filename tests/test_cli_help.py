"""Smoke tests: every CLI subcommand responds to --help with exit code 0."""

from __future__ import annotations

import subprocess
import sys

import pytest

_SUBCOMMANDS = ["init", "verify"]


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


def test_init_reinstall_flag_in_help():
    result = subprocess.run(
        [sys.executable, "-m", "ai_career_toolkit.cli", "init", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "--reinstall" in result.stdout


def test_init_personalize_flag_in_help():
    result = subprocess.run(
        [sys.executable, "-m", "ai_career_toolkit.cli", "init", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "--personalize" in result.stdout


def test_removed_install_subcommand():
    """Ensure 'install' is no longer a valid subcommand."""
    result = subprocess.run(
        [sys.executable, "-m", "ai_career_toolkit.cli", "install", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_removed_personalize_subcommand():
    """Ensure 'personalize' is no longer a valid subcommand."""
    result = subprocess.run(
        [sys.executable, "-m", "ai_career_toolkit.cli", "personalize", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
