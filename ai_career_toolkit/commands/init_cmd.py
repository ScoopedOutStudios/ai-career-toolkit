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
from ai_career_toolkit.ui import (
    blank,
    bold,
    detail,
    dim,
    header,
    info,
    pick_one,
    step,
    success,
    warn,
)

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


def _run_install(material_root: Path, platform: str, scope: str = "local") -> int:
    script = material_root / "scripts" / "install.sh"
    if not script.is_file():
        print(f"Missing {script}", file=sys.stderr)
        return 1
    env = os.environ.copy()
    env.setdefault("AI_CAREER_TOOLKIT_ROOT", str(material_root))
    proc = subprocess.run(
        ["bash", str(script), "--platform", platform, "--scope", scope],
        cwd=str(material_root),
        env=env,
    )
    return int(proc.returncode)


def _is_platform_installed(platform: str, scope: str = "local", workspace: Path | None = None) -> bool:
    marker = "opportunity-evaluator/SKILL.md"
    base = workspace or Path.cwd()
    if platform == "cursor":
        if scope == "global":
            return (Path.home() / ".cursor" / "skills" / marker).is_file()
        return (base / ".cursor" / "skills" / marker).is_file()
    if platform == "claude-code":
        return (base / ".claude" / "skills" / marker).is_file()
    return False


def _pick_platform() -> str | None:
    choice = pick_one(
        "Which AI platform do you use?",
        ["Cursor", "Claude Code", "Skip for now"],
        default="Cursor",
    )
    if choice == "Cursor":
        return "cursor"
    if choice == "Claude Code":
        return "claude-code"
    return None


def _pick_scope() -> str:
    choice = pick_one(
        "Install scope for Cursor",
        [
            "This workspace only (.cursor/ in current directory)",
            "Global (~/.cursor/ — available in all workspaces)",
        ],
        default="This workspace only (.cursor/ in current directory)",
    )
    return "global" if "Global" in choice else "local"


# ---------------------------------------------------------------------------
# handle_init — the unified golden-path command
# ---------------------------------------------------------------------------

TOTAL_STEPS = 5


def handle_init(args) -> int:
    yes: bool = args.yes
    data_home = Path(args.data_home).expanduser().resolve() if args.data_home else default_data_home()
    platform_arg: str | None = getattr(args, "platform", None)

    header("ai-career-toolkit init")

    # ------------------------------------------------------------------
    # Step 1: Scaffold
    # ------------------------------------------------------------------
    step(1, TOTAL_STEPS, "Scaffold")

    if args.workspace:
        workspace = Path(str(args.workspace)).expanduser().resolve()
    else:
        er = editable_repo_root()
        workspace = er if er else (Path.home() / "ai-career-toolkit").resolve()

    source = _source_root()

    if not is_toolkit_root(workspace):
        workspace.mkdir(parents=True, exist_ok=True)
        materialize(workspace, source)
        success("Toolkit files created")
    else:
        success("Existing toolkit found")

    scaffold(workspace, data_home=data_home)
    detail("Toolkit root", str(workspace))
    detail("Config", str(workspace / "config"))
    detail("Personal data", str(data_home))
    blank()

    # ------------------------------------------------------------------
    # Step 2: Personalize
    # ------------------------------------------------------------------
    step(2, TOTAL_STEPS, "Personalize")

    from ai_career_toolkit.commands.personalize_cmd import handle_personalize

    rc = handle_personalize(workspace=workspace, data_home=data_home, yes=yes, show_header=False)
    if rc != 0:
        return rc
    blank()

    # ------------------------------------------------------------------
    # Step 3: Platform Install
    # ------------------------------------------------------------------
    step(3, TOTAL_STEPS, "Platform Install")

    if platform_arg:
        chosen_platform = platform_arg
    elif yes:
        chosen_platform = "cursor" if (Path.home() / ".cursor").is_dir() else None
    else:
        chosen_platform = _pick_platform()

    chosen_scope = "local"
    if chosen_platform:
        if chosen_platform == "cursor" and not yes:
            blank()
            chosen_scope = _pick_scope()

        if _is_platform_installed(chosen_platform, chosen_scope, workspace):
            success(f"Platform install ({chosen_platform}): already up to date")
        else:
            info(f"Installing into {chosen_platform} ({chosen_scope})...")
            rc = _run_install(workspace, chosen_platform, chosen_scope)
            if rc != 0:
                warn(f"Platform install returned exit code {rc}.")
                return rc
            if chosen_platform == "cursor":
                dest = "~/.cursor/" if chosen_scope == "global" else ".cursor/"
            else:
                dest = ".claude/"
            success(f"Installed to {dest}")
    else:
        info("Skipping platform install")
        print(f"        {dim('Run `ai-career-toolkit install --platform <name>` later.')}")
    blank()

    # ------------------------------------------------------------------
    # Step 4: Verify
    # ------------------------------------------------------------------
    step(4, TOTAL_STEPS, "Verify")

    from ai_career_toolkit.commands.verify_cmd import run_verify

    run_verify(
        platform=chosen_platform or "none",
        workspace=workspace,
        output_format="text",
    )
    blank()

    # ------------------------------------------------------------------
    # Step 5: Ready!
    # ------------------------------------------------------------------
    step(5, TOTAL_STEPS, "Ready!")

    _print_first_prompt(workspace, data_home)

    default_location = (Path.home() / "ai-career-toolkit").resolve()
    if args.workspace and workspace != default_location:
        blank()
        info(dim("Custom workspace — add to your shell profile if needed:"))
        print(f"        {dim(f'export AI_CAREER_TOOLKIT_ROOT={workspace!s}')}")

    blank()
    return 0


def _print_first_prompt(workspace: Path, data_home: Path) -> None:
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

    print(f"        {bold('Open your AI agent and try:')}")
    blank()
    if domains and role and level:
        domain_str = " and ".join(domains[:2])
        if len(domains) > 2:
            domain_str += f" (+{len(domains) - 2} more)"
        print(f'        {dim("1.")} "Build me a target company list for {domain_str} {level} {role} roles"')
    else:
        print(f'        {dim("1.")} "Build me a target company list for my target domains"')
    print(f'        {dim("2.")} "Evaluate this opportunity at [Company] — here\'s the JD: [paste]"')
    blank()
    print(f"        For more prompts, see {bold('docs/playbook.md')}")


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
            print(
                "Pass --workspace /path/to/toolkit or run init first.",
                file=sys.stderr,
            )
            return 1
    if not is_toolkit_root(workspace):
        print(
            f"Toolkit files not found at {workspace}. Run `ai-career-toolkit init` first.",
            file=sys.stderr,
        )
        return 1
    scope = getattr(args, "scope", "local")
    return _run_install(workspace, args.platform, scope)
