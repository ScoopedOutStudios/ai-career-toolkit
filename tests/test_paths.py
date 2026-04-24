"""Unit tests for ai_career_toolkit.paths."""

from __future__ import annotations

from pathlib import Path

from ai_career_toolkit.paths import (
    default_data_home,
    is_toolkit_root,
    package_dir,
)


def test_package_dir_exists():
    d = package_dir()
    assert d.is_dir()
    assert (d / "__init__.py").is_file()


def test_is_toolkit_root_true(tmp_path: Path):
    (tmp_path / "skills" / "opportunity-evaluator").mkdir(parents=True)
    (tmp_path / "skills" / "opportunity-evaluator" / "SKILL.md").write_text("test")
    (tmp_path / "agents").mkdir()
    (tmp_path / "scripts").mkdir()
    assert is_toolkit_root(tmp_path)


def test_is_toolkit_root_false_missing_marker(tmp_path: Path):
    (tmp_path / "skills").mkdir()
    (tmp_path / "agents").mkdir()
    assert not is_toolkit_root(tmp_path)


def test_is_toolkit_root_false_empty(tmp_path: Path):
    assert not is_toolkit_root(tmp_path)


def test_default_data_home(monkeypatch):
    monkeypatch.delenv("AI_CAREER_TOOLKIT_HOME", raising=False)
    result = default_data_home()
    assert result == (Path.home() / ".ai-career-toolkit").resolve()


def test_default_data_home_override(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("AI_CAREER_TOOLKIT_HOME", str(tmp_path / "custom"))
    result = default_data_home()
    assert result == (tmp_path / "custom").resolve()
