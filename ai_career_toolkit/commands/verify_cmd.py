"""Validate toolkit layout, config scaffolding, and optional IDE installs."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from ai_career_toolkit.paths import (
    bundled_root,
    default_data_home,
    editable_repo_root,
    is_toolkit_root,
    resolve_toolkit_root,
)


@dataclass
class Check:
    id: str
    ok: bool
    detail: str
    fix: str


def _bash_available() -> bool:
    return shutil.which("bash") is not None


def _check_cursor_install() -> Check:
    skills = Path.home() / ".cursor" / "skills" / "opportunity-evaluator" / "SKILL.md"
    agents = Path.home() / ".cursor" / "agents" / "research-guru.md"
    rules = Path.home() / ".cursor" / "rules" / "job-artifact-privacy.mdc"
    if skills.is_file() and agents.is_file() and rules.is_file():
        return Check("platform_cursor", True, "Cursor skills, agents, and rules present.", "")
    missing = []
    if not skills.is_file():
        missing.append("~/.cursor/skills/…")
    if not agents.is_file():
        missing.append("~/.cursor/agents/…")
    if not rules.is_file():
        missing.append("~/.cursor/rules/…")
    return Check(
        "platform_cursor",
        False,
        "Incomplete: " + ", ".join(missing),
        "From your toolkit directory run: ./scripts/install.sh --platform cursor",
    )


def _check_claude_cwd() -> Check:
    root = Path.cwd()
    skills = root / ".claude" / "skills" / "opportunity-evaluator" / "SKILL.md"
    if skills.is_file():
        return Check("platform_claude_cwd", True, f"Claude skills found under {root / '.claude'}.", "")
    return Check(
        "platform_claude_cwd",
        False,
        f"No .claude/skills in current directory ({root}).",
        "cd your job-search project and run: /path/to/ai-career-toolkit/scripts/install.sh --platform claude-code",
    )


def run_verify(*, platform: str, workspace: Path | None, output_format: str) -> int:
    results: list[Check] = []

    root: Path | None = None
    if workspace is not None:
        w = workspace.expanduser().resolve()
        if is_toolkit_root(w):
            root = w
        else:
            results.append(
                Check(
                    "toolkit_root",
                    False,
                    f"Not a toolkit directory: {w}",
                    "Pass a path with skills/, agents/, scripts/ or run init.",
                )
            )
            return _emit(results, output_format, critical=True)
    else:
        try:
            root = resolve_toolkit_root(env_only=False)
        except FileNotFoundError as e:
            results.append(
                Check(
                    "toolkit_root",
                    False,
                    str(e),
                    "Run `ai-career-toolkit init` or set AI_CAREER_TOOLKIT_ROOT.",
                )
            )
            return _emit(results, output_format, critical=True)

    assert root is not None
    results.append(Check("toolkit_root", True, str(root), ""))

    if not (root / "scripts" / "install.sh").is_file():
        results.append(
            Check(
                "install_script",
                False,
                "scripts/install.sh missing",
                "Re-run init or reinstall the package.",
            )
        )
    else:
        results.append(Check("install_script", True, "scripts/install.sh present", ""))

    # Python packaging modes
    if bundled_root() is not None:
        results.append(Check("bundle", True, "Running from pip wheel bundle.", ""))
    elif editable_repo_root() is not None:
        results.append(Check("bundle", True, "Editable / git checkout layout detected.", ""))
    else:
        results.append(
            Check(
                "bundle",
                True,
                "Using workspace discovery / AI_CAREER_TOOLKIT_ROOT.",
                "",
            )
        )

    # Bash (for install.sh)
    if _bash_available():
        results.append(Check("bash", True, shutil.which("bash") or "bash", ""))
    else:
        results.append(
            Check(
                "bash",
                False,
                "bash not found on PATH",
                "Install bash (Windows: use WSL or Git Bash) to run scripts/install.sh.",
            )
        )

    # Config scaffold
    cfg = root / "config"
    settings = cfg / "settings.yaml"
    if settings.is_file():
        results.append(Check("config_settings", True, str(settings), ""))
    else:
        results.append(
            Check(
                "config_settings",
                False,
                f"No {settings}",
                "Run `ai-career-toolkit init` or copy config.example into config/.",
            )
        )

    # Personal data home
    data = default_data_home()
    if data.is_dir():
        results.append(Check("data_home", True, str(data), ""))
    else:
        results.append(
            Check(
                "data_home",
                False,
                f"Missing {data}",
                "Run `ai-career-toolkit init` to create ~/.ai-career-toolkit.",
            )
        )

    role = data / "role-thesis.md"
    if role.is_file():
        results.append(Check("role_thesis", True, str(role), ""))
    else:
        results.append(
            Check(
                "role_thesis",
                False,
                f"Missing {role}",
                "Run init or copy config/role-thesis.md data home (see README).",
            )
        )

    if platform in ("cursor", "both"):
        results.append(_check_cursor_install())
    if platform in ("claude-code", "both"):
        results.append(_check_claude_cwd())

    return _emit(results, output_format, critical=False)


def _emit(results: list[Check], output_format: str, *, critical: bool) -> int:
    if output_format == "json":
        print(json.dumps([c.__dict__ for c in results], indent=2))
    else:
        for c in results:
            status = "ok" if c.ok else "gap"
            print(f"[{status}] {c.id}: {c.detail}")
            if not c.ok and c.fix:
                print(f"        fix: {c.fix}")
        if not critical:
            gaps = sum(1 for c in results if not c.ok)
            print("")
            print(f"Summary: {len(results) - gaps}/{len(results)} checks passed.")
    if critical:
        return 2
    return 1 if any(not c.ok for c in results) else 0
