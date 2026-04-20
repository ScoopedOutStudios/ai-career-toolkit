"""Guided first-run setup: materialize toolkit files, scaffold config and data home."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from ai_career_toolkit.materialize import materialize
from ai_career_toolkit.paths import (
    default_data_home,
    editable_repo_root,
    is_toolkit_root,
)
from ai_career_toolkit.scaffold import scaffold


def _prompt(default: str) -> str:
    if not sys.stdin.isatty():
        return default
    try:
        line = input(f"Toolkit install directory [{default}]: ").strip()
    except EOFError:
        return default
    return line if line else default


def _yes_no(prompt: str, default_no: bool = True) -> bool:
    if not sys.stdin.isatty():
        return not default_no
    suffix = " [y/N]: " if default_no else " [Y/n]: "
    try:
        ans = input(prompt + suffix).strip().lower()
    except EOFError:
        return not default_no
    if not ans:
        return not default_no
    return ans in ("y", "yes")


def _source_root() -> Path:
    src = bundled_root() or editable_repo_root()
    if src is None:
        raise RuntimeError(
            "Cannot locate embedded toolkit files. Reinstall with: pip install -U ai-career-toolkit"
        )
    return src


def handle_init(args) -> int:
    yes: bool = args.yes
    data_home = Path(args.data_home).expanduser().resolve() if args.data_home else default_data_home()

    er = editable_repo_root()
    default_ws = str(er) if er else str(Path.home() / "ai-career-toolkit")
    workspace_s = str(args.workspace) if args.workspace else (default_ws if yes else _prompt(default_ws))
    workspace = Path(workspace_s).expanduser().resolve()

    source = _source_root()

    if not is_toolkit_root(workspace):
        if not yes and sys.stdin.isatty():
            print(f"Will copy toolkit files from package into:\n  {workspace}")
            if not _yes_no("Continue?", default_no=False):
                print("Aborted.")
                return 1
        workspace.mkdir(parents=True, exist_ok=True)
        materialize(workspace, source)
    else:
        if not yes and sys.stdin.isatty():
            print(f"Using existing toolkit at:\n  {workspace}")

    scaffold(workspace, data_home=data_home)

    if not yes and sys.stdin.isatty():
        print("")
        print("Setup complete.")
        print(f"  Toolkit root:     {workspace}")
        print(f"  Local config:     {workspace / 'config'}")
        print(f"  Personal data:    {data_home}")
        print("")
        print("Next: edit config/settings.yaml and your role-thesis under the data home path above.")
        print("")
        print("Tip: persist toolkit location:")
        print(f"  export AI_CAREER_TOOLKIT_ROOT={workspace!s}")
        if _yes_no("Run Cursor install now (scripts/install.sh --platform cursor)?", default_no=True):
            return _run_install(workspace, "cursor")
        return 0

    print(f"ai-career-toolkit init: done. Toolkit root={workspace} data_home={data_home}")
    print("")
    print("Tip: point tools and docs at your install (e.g. in ~/.zshrc):")
    print(f"  export AI_CAREER_TOOLKIT_ROOT={workspace!s}")
    return 0


def _run_install(material_root: Path, platform: str) -> int:
    script = material_root / "scripts" / "install.sh"
    if not script.is_file():
        print(f"Missing {script}", file=sys.stderr)
        return 1
    env = os.environ.copy()
    env.setdefault("AI_CAREER_TOOLKIT_ROOT", str(material_root))
    proc = subprocess.run(
        ["bash", str(script), "--platform", platform],
        cwd=str(material_root),
        env=env,
    )
    return int(proc.returncode)


def handle_install(args) -> int:
    workspace = Path(args.workspace).expanduser().resolve() if args.workspace else None
    if workspace is None:
        try:
            from ai_career_toolkit.paths import resolve_toolkit_root

            workspace = resolve_toolkit_root()
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            print("Pass --workspace /path/to/toolkit or run init first.", file=sys.stderr)
            return 1
    if not is_toolkit_root(workspace):
        print(f"Not a toolkit directory: {workspace}", file=sys.stderr)
        return 1
    return _run_install(workspace, args.platform)
