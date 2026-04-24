"""Unit tests for ai_career_toolkit.scaffold."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_career_toolkit.scaffold import scaffold


def _make_toolkit(root: Path) -> Path:
    """Create a minimal toolkit tree so scaffold recognises *root*."""
    (root / "skills" / "opportunity-evaluator").mkdir(parents=True)
    (root / "skills" / "opportunity-evaluator" / "SKILL.md").write_text("test")
    (root / "agents").mkdir()
    (root / "scripts").mkdir()
    example = root / "config.example"
    example.mkdir()
    (example / "settings.yaml").write_text("platform: cursor\n")
    (example / "role-thesis.md").write_text("# Role Thesis\n")
    return root


def test_scaffold_creates_directories(tmp_path: Path):
    root = _make_toolkit(tmp_path / "toolkit")
    data = tmp_path / "data"
    scaffold(root, data_home=data)

    assert (root / "config" / "settings.yaml").is_file()
    assert data.is_dir()
    assert (data / "voice-pack").is_dir()
    assert (data / "source-lists").is_dir()
    assert (data / "opportunities").is_dir()
    assert (data / "interview-notes").is_dir()
    assert (data / "weekly-reviews").is_dir()


def test_scaffold_copies_role_thesis(tmp_path: Path):
    root = _make_toolkit(tmp_path / "toolkit")
    data = tmp_path / "data"
    scaffold(root, data_home=data)

    assert (data / "role-thesis.md").is_file()
    assert "Role Thesis" in (data / "role-thesis.md").read_text()


def test_scaffold_idempotent(tmp_path: Path):
    root = _make_toolkit(tmp_path / "toolkit")
    data = tmp_path / "data"
    scaffold(root, data_home=data)
    (data / "role-thesis.md").write_text("# Customized\n")

    scaffold(root, data_home=data)
    assert (data / "role-thesis.md").read_text() == "# Customized\n"


def test_scaffold_rejects_invalid_root(tmp_path: Path):
    with pytest.raises(ValueError, match="Invalid toolkit root"):
        scaffold(tmp_path, data_home=tmp_path / "data")
