"""Copy bundled toolkit files into a user-chosen directory (pip install workflow)."""

from __future__ import annotations

import shutil
from pathlib import Path

from ai_career_toolkit.paths import is_toolkit_root

_COPY_NAMES = (
    "skills",
    "agents",
    "rules",
    "config.example",
    "templates",
    "workflow-docs",
    "docs",
    "scripts",
)


def materialize(target: Path, source: Path) -> None:
    """Populate target with toolkit directories/files from source (bundle or repo)."""
    if not is_toolkit_root(source):
        raise ValueError(f"Source is not a toolkit tree: {source}")

    target.mkdir(parents=True, exist_ok=True)

    for name in _COPY_NAMES:
        src = source / name
        dst = target / name
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            raise FileNotFoundError(f"Missing required path in toolkit source: {src}")

    setup_sh = source / "setup.sh"
    if setup_sh.is_file():
        shutil.copy2(setup_sh, target / "setup.sh")

    lic = source / "LICENSE"
    if lic.is_file():
        shutil.copy2(lic, target / "LICENSE")
