"""Port of setup.sh: local config + personal data directories."""

from __future__ import annotations

import shutil
from pathlib import Path

from ai_career_toolkit.paths import default_data_home, is_toolkit_root


def scaffold(material_root: Path, *, data_home: Path | None = None) -> None:
    """
    Create ./config from config.example and ~/.ai-career-toolkit hierarchy.
    material_root is the directory containing skills/, config.example/, etc.
    """
    if not is_toolkit_root(material_root):
        raise ValueError(f"Invalid toolkit root: {material_root}")

    data = data_home if data_home is not None else default_data_home()
    cfg = material_root / "config"
    example = material_root / "config.example"

    cfg.mkdir(parents=True, exist_ok=True)

    if example.is_dir():
        for item in example.iterdir():
            dest = cfg / item.name
            if dest.exists():
                continue
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

    for sub, _desc in (
        (data, "personal career data"),
        (data / "voice-pack", "voice pack"),
        (data / "source-lists", "per-domain company list drafts"),
        (data / "opportunities", "opportunity tracking"),
        (data / "interview-notes", "interview notes"),
        (data / "weekly-reviews", "weekly reviews"),
    ):
        sub.mkdir(parents=True, exist_ok=True)

    role_src = cfg / "role-thesis.md"
    role_dst = data / "role-thesis.md"
    if role_src.is_file() and not role_dst.exists():
        shutil.copy2(role_src, role_dst)

    tsv_src = cfg / "target-companies.tsv"
    tsv_dst = data / "target-companies.tsv"
    if tsv_src.is_file() and not tsv_dst.exists():
        shutil.copy2(tsv_src, tsv_dst)
