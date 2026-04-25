"""Tests for verify_cmd platform checks with workspace-aware paths."""

from __future__ import annotations

from pathlib import Path

from ai_career_toolkit.commands.verify_cmd import (
    _check_claude_install,
    _check_cursor_install,
)


def _make_toolkit(root: Path) -> Path:
    """Create a minimal toolkit tree."""
    (root / "skills" / "opportunity-evaluator").mkdir(parents=True)
    (root / "skills" / "opportunity-evaluator" / "SKILL.md").write_text("test")
    (root / "agents").mkdir()
    (root / "scripts").mkdir()
    return root


def _install_cursor_local(root: Path) -> None:
    """Simulate a local Cursor install under root/.cursor/."""
    base = root / ".cursor"
    (base / "skills" / "opportunity-evaluator").mkdir(parents=True)
    (base / "skills" / "opportunity-evaluator" / "SKILL.md").write_text("test")
    (base / "agents").mkdir(parents=True)
    (base / "agents" / "research-guru.md").write_text("test")
    (base / "rules").mkdir(parents=True)
    (base / "rules" / "job-artifact-privacy.mdc").write_text("test")


def _install_claude_local(root: Path) -> None:
    """Simulate a local Claude Code install under root/.claude/."""
    base = root / ".claude"
    (base / "skills" / "opportunity-evaluator").mkdir(parents=True)
    (base / "skills" / "opportunity-evaluator" / "SKILL.md").write_text("test")


# ---------------------------------------------------------------------------
# Cursor local install
# ---------------------------------------------------------------------------


def test_cursor_local_install_found(tmp_path: Path):
    root = _make_toolkit(tmp_path / "toolkit")
    _install_cursor_local(root)
    result = _check_cursor_install(root)
    assert result.ok
    assert "local" in result.detail


def test_cursor_local_install_missing(tmp_path: Path, monkeypatch):
    fake_home = tmp_path / "fakehome"
    fake_home.mkdir()
    monkeypatch.setattr(Path, "home", staticmethod(lambda: fake_home))

    root = _make_toolkit(tmp_path / "toolkit")
    result = _check_cursor_install(root)
    assert not result.ok
    assert "not found" in result.detail


def test_cursor_global_install_found(tmp_path: Path, monkeypatch):
    """Simulate global install by patching Path.home()."""
    fake_home = tmp_path / "fakehome"
    fake_home.mkdir()
    monkeypatch.setattr(Path, "home", staticmethod(lambda: fake_home))

    cursor_dir = fake_home / ".cursor"
    (cursor_dir / "skills" / "opportunity-evaluator").mkdir(parents=True)
    (cursor_dir / "skills" / "opportunity-evaluator" / "SKILL.md").write_text("test")

    root = _make_toolkit(tmp_path / "toolkit")
    result = _check_cursor_install(root)
    assert result.ok
    assert "global" in result.detail


# ---------------------------------------------------------------------------
# Claude Code workspace-local install
# ---------------------------------------------------------------------------


def test_claude_install_found(tmp_path: Path):
    root = _make_toolkit(tmp_path / "toolkit")
    _install_claude_local(root)
    result = _check_claude_install(root)
    assert result.ok
    assert ".claude" in result.detail


def test_claude_install_missing(tmp_path: Path):
    root = _make_toolkit(tmp_path / "toolkit")
    result = _check_claude_install(root)
    assert not result.ok
    assert "No .claude/skills" in result.detail


def test_claude_install_uses_workspace_not_cwd(tmp_path: Path, monkeypatch):
    """Verify check uses workspace root, not process cwd."""
    workspace = _make_toolkit(tmp_path / "workspace")
    _install_claude_local(workspace)

    other_dir = tmp_path / "unrelated"
    other_dir.mkdir()
    monkeypatch.chdir(other_dir)

    result = _check_claude_install(workspace)
    assert result.ok, "Should find .claude under workspace, not cwd"


# ---------------------------------------------------------------------------
# init_cmd._is_platform_installed with workspace arg
# ---------------------------------------------------------------------------


def test_is_platform_installed_cursor_local(tmp_path: Path):
    from ai_career_toolkit.commands.init_cmd import _is_platform_installed

    root = _make_toolkit(tmp_path / "toolkit")
    assert not _is_platform_installed("cursor", "local", root)

    _install_cursor_local(root)
    assert _is_platform_installed("cursor", "local", root)


def test_is_platform_installed_claude(tmp_path: Path):
    from ai_career_toolkit.commands.init_cmd import _is_platform_installed

    root = _make_toolkit(tmp_path / "toolkit")
    assert not _is_platform_installed("claude-code", "local", root)

    _install_claude_local(root)
    assert _is_platform_installed("claude-code", "local", root)
