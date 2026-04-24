"""Unified first-run setup: scaffold -> personalize -> install -> verify -> first prompt."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from ai_career_toolkit.materialize import materialize
from ai_career_toolkit.paths import (
    bundled_root,
    default_data_home,
    editable_repo_root,
    is_toolkit_root,
)
from ai_career_toolkit.scaffold import scaffold

# ---------------------------------------------------------------------------
# Interactive helpers
# ---------------------------------------------------------------------------


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


def _pick_platform() -> str | None:
    """Auto-detect or interactively choose the target platform."""
    if not sys.stdin.isatty():
        if (Path.home() / ".cursor").is_dir():
            return "cursor"
        return None
    print("")
    print("Which AI platform do you use?")
    print("  1) Cursor")
    print("  2) Claude Code")
    print("  3) Skip for now")
    try:
        choice = input("Choice [1]: ").strip()
    except EOFError:
        choice = "1"
    if choice in ("", "1"):
        return "cursor"
    if choice == "2":
        return "claude-code"
    return None


# ---------------------------------------------------------------------------
# Source root resolution
# ---------------------------------------------------------------------------


def _source_root() -> Path:
    src = bundled_root() or editable_repo_root()
    if src is None:
        raise RuntimeError("Cannot locate embedded toolkit files. Reinstall with: pip install -U ai-career-toolkit")
    return src


# ---------------------------------------------------------------------------
# Step 3: platform install
# ---------------------------------------------------------------------------


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


def _is_platform_installed(platform: str) -> bool:
    if platform == "cursor":
        return (Path.home() / ".cursor" / "skills" / "opportunity-evaluator" / "SKILL.md").is_file()
    if platform == "claude-code":
        return (Path.cwd() / ".claude" / "skills" / "opportunity-evaluator" / "SKILL.md").is_file()
    return False


# ---------------------------------------------------------------------------
# handle_init — the unified golden-path command
# ---------------------------------------------------------------------------


def handle_init(args) -> int:
    yes: bool = args.yes
    data_home = Path(args.data_home).expanduser().resolve() if args.data_home else default_data_home()
    platform_arg: str | None = getattr(args, "platform", None)

    # --- Step 1: Scaffold ---
    er = editable_repo_root()
    default_ws = str(er) if er else str(Path.home() / "ai-career-toolkit")
    workspace_s = str(args.workspace) if args.workspace else (default_ws if yes else _prompt(default_ws))
    workspace = Path(workspace_s).expanduser().resolve()

    source = _source_root()

    if not is_toolkit_root(workspace):
        if not yes and sys.stdin.isatty():
            print(f"\nWill copy toolkit files from package into:\n  {workspace}")
            if not _yes_no("Continue?", default_no=False):
                print("Aborted.")
                return 1
        workspace.mkdir(parents=True, exist_ok=True)
        materialize(workspace, source)
        print(f"  Toolkit files materialized to {workspace}")
    else:
        print(f"  Using existing toolkit at {workspace}")

    scaffold(workspace, data_home=data_home)
    print(f"  Config:       {workspace / 'config'}")
    print(f"  Personal data: {data_home}")

    # --- Step 2: Personalize ---
    from ai_career_toolkit.commands.personalize_cmd import handle_personalize

    print("")
    rc = handle_personalize(workspace=workspace, data_home=data_home, yes=yes)
    if rc != 0:
        return rc

    # --- Step 3: Platform install ---
    if platform_arg:
        chosen_platform = platform_arg
    elif yes:
        chosen_platform = "cursor" if (Path.home() / ".cursor").is_dir() else None
    else:
        chosen_platform = _pick_platform()

    if chosen_platform:
        if _is_platform_installed(chosen_platform):
            print(f"\n  Platform install ({chosen_platform}): already up to date.")
        else:
            print(f"\n  Installing into {chosen_platform}...")
            rc = _run_install(workspace, chosen_platform)
            if rc != 0:
                print(f"  Platform install returned exit code {rc}.", file=sys.stderr)
                return rc
    else:
        print("\n  Skipping platform install (run `ai-career-toolkit install --platform <name>` later).")

    # --- Step 4: Verify ---
    from ai_career_toolkit.commands.verify_cmd import run_verify

    print("")
    run_verify(
        platform=chosen_platform or "none",
        workspace=workspace,
        output_format="text",
    )

    # --- Step 5: First prompt ---
    _print_first_prompt(workspace, data_home)

    print("")
    print("Tip: persist toolkit location in your shell profile:")
    print(f"  export AI_CAREER_TOOLKIT_ROOT={workspace!s}")
    return 0


def _print_first_prompt(workspace: Path, data_home: Path) -> None:
    """Print a ready-to-paste first prompt based on the user's personalized config."""
    from ai_career_toolkit.commands.personalize_cmd import (
        _read_scalar,
        _read_settings,
        _read_yaml_list_values,
    )

    settings_path = workspace / "config" / "settings.yaml"
    lines = _read_settings(settings_path)
    role = _read_scalar(lines, "role")
    level = _read_scalar(lines, "level")
    domains = _read_yaml_list_values(lines, "domains")

    print("")
    print("Setup complete! Open your AI agent and try:")
    if domains and role and level:
        domain_str = " and ".join(domains[:2])
        if len(domains) > 2:
            domain_str += f" (+{len(domains) - 2} more)"
        print(f'  "Build me a target company list for {domain_str} {level} {role} roles"')
    else:
        print('  "Build me a target company list for my target domains"')
    print("")
    print("For more prompts, see docs/playbook.md or docs/GETTING_STARTED.md.")


# ---------------------------------------------------------------------------
# handle_install — standalone re-install (after git pull, etc.)
# ---------------------------------------------------------------------------


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
