"""Resolve filesystem locations for the toolkit tree and user data directories."""

from __future__ import annotations

import os
from pathlib import Path

_MARKERS = ("skills", "agents", "scripts")


def default_data_home() -> Path:
    """Personal career data directory (outside any repo)."""
    override = os.environ.get("AI_CAREER_TOOLKIT_HOME")
    if override:
        return Path(override).expanduser().resolve()
    return (Path.home() / ".ai-career-toolkit").resolve()


def is_toolkit_root(path: Path) -> bool:
    p = path.resolve()
    return (
        all((p / name).is_dir() for name in _MARKERS)
        and (p / "skills" / "opportunity-evaluator" / "SKILL.md").is_file()
    )


def package_dir() -> Path:
    return Path(__file__).resolve().parent


def bundled_root() -> Path | None:
    """Wheel layout: assets under ai_career_toolkit/bundle/."""
    bundle = package_dir() / "bundle"
    if is_toolkit_root(bundle):
        return bundle
    return None


def editable_repo_root() -> Path | None:
    """Development layout: repo root is parent of the ai_career_toolkit package."""
    candidate = package_dir().parent
    if is_toolkit_root(candidate):
        return candidate
    return None


def resolve_toolkit_root(*, env_only: bool = False) -> Path:
    """
    Resolution order:
    1) AI_CAREER_TOOLKIT_ROOT
    2) Walk upward from cwd looking for skills/agents/scripts
    3) Bundled wheel copy (site-packages/.../bundle)
    4) Editable checkout (repo root next to package)
    """
    env = os.environ.get("AI_CAREER_TOOLKIT_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if is_toolkit_root(p):
            return p
        raise FileNotFoundError(f"AI_CAREER_TOOLKIT_ROOT is set but does not look like a toolkit tree: {p}")

    if not env_only:
        here = Path.cwd().resolve()
        for parent in [here, *here.parents]:
            if is_toolkit_root(parent):
                return parent

    br = bundled_root()
    if br is not None:
        return br

    er = editable_repo_root()
    if er is not None:
        return er

    raise FileNotFoundError(
        "Could not find ai-career-toolkit files. Run `ai-career-toolkit init`, set "
        "AI_CAREER_TOOLKIT_ROOT to your install directory, or run from inside a checkout."
    )
