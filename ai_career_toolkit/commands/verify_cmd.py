"""Validate toolkit layout, config scaffolding, and optional IDE installs."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, field
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
    level: str = field(default="error")  # "error" | "warn"


def _bash_available() -> bool:
    return shutil.which("bash") is not None


def _check_cursor_install(root: Path) -> Check:
    """Check both local (workspace) and global (~/.cursor) Cursor installs."""
    local_skills = root / ".cursor" / "skills" / "opportunity-evaluator" / "SKILL.md"
    global_skills = Path.home() / ".cursor" / "skills" / "opportunity-evaluator" / "SKILL.md"

    if local_skills.is_file():
        return Check(
            "platform_cursor",
            True,
            f"Cursor install found (local): {root / '.cursor'}",
            "",
        )
    if global_skills.is_file():
        return Check(
            "platform_cursor",
            True,
            "Cursor install found (global): ~/.cursor",
            "",
        )
    return Check(
        "platform_cursor",
        False,
        "Cursor skills not found in .cursor/ (local) or ~/.cursor/ (global)",
        "Run `ai-career-toolkit install --platform cursor` from your toolkit directory.",
    )


def _check_claude_install(root: Path) -> Check:
    """Check workspace-local .claude/ install."""
    skills = root / ".claude" / "skills" / "opportunity-evaluator" / "SKILL.md"
    if skills.is_file():
        return Check(
            "platform_claude",
            True,
            f"Claude install found: {root / '.claude'}",
            "",
        )
    return Check(
        "platform_claude",
        False,
        f"No .claude/skills found under {root}",
        "Run `ai-career-toolkit install --platform claude-code` from your project directory.",
    )


# ---------------------------------------------------------------------------
# Personalization checks (warn level — don't fail, but surface gaps)
# ---------------------------------------------------------------------------


def _check_personalization_domains(settings: Path) -> Check:
    """Warn if settings.yaml has no uncommented domains."""
    if not settings.is_file():
        return Check(
            "personalization_domains",
            False,
            "No settings.yaml found",
            "Run `ai-career-toolkit init`.",
            level="warn",
        )
    text = settings.read_text()
    in_domains = False
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^\s*domains\s*:", line):
            in_domains = True
            continue
        if in_domains:
            if stripped.startswith("- ") and not stripped.startswith("# "):
                return Check(
                    "personalization_domains",
                    True,
                    "Targeting domains configured.",
                    "",
                    level="warn",
                )
            if stripped and not stripped.startswith("#") and not stripped.startswith("- "):
                break
    return Check(
        "personalization_domains",
        False,
        "No targeting domains configured",
        "Run `ai-career-toolkit personalize` or uncomment domains in config/settings.yaml.",
        level="warn",
    )


def _check_personalization_role(settings: Path) -> Check:
    """Warn if role or level are empty / commented out."""
    if not settings.is_file():
        return Check(
            "personalization_role",
            False,
            "No settings.yaml found",
            "Run `ai-career-toolkit init`.",
            level="warn",
        )
    text = settings.read_text()
    has_role = False
    has_level = False
    for line in text.splitlines():
        m_role = re.match(r"^\s*role\s*:\s*(.+)$", line)
        if m_role and not m_role.group(1).strip().startswith("#"):
            has_role = bool(m_role.group(1).strip())
        m_level = re.match(r"^\s*level\s*:\s*(.+)$", line)
        if m_level and not m_level.group(1).strip().startswith("#"):
            has_level = bool(m_level.group(1).strip())
    if has_role and has_level:
        return Check(
            "personalization_role",
            True,
            "Role and level configured.",
            "",
            level="warn",
        )
    missing = []
    if not has_role:
        missing.append("role")
    if not has_level:
        missing.append("level")
    return Check(
        "personalization_role",
        False,
        f"Missing targeting fields: {', '.join(missing)}",
        "Run `ai-career-toolkit personalize` or edit config/settings.yaml.",
        level="warn",
    )


def _check_personalization_thesis(thesis: Path) -> Check:
    """Warn if role-thesis still contains only template placeholder markers."""
    if not thesis.is_file():
        return Check(
            "personalization_thesis",
            False,
            "role-thesis.md not found",
            "Run `ai-career-toolkit init` to create it.",
            level="warn",
        )
    text = thesis.read_text()
    if "<!-- e.g.," in text or "<!-- " in text:
        without_placeholders = re.sub(r"<!--.*?-->", "", text)
        meaningful = [
            ln.strip()
            for ln in without_placeholders.splitlines()
            if ln.strip() and not ln.strip().startswith(("#", ">", "-", "**", "Use this", "Define your", "Score:"))
        ]
        if len(meaningful) < 5:
            return Check(
                "personalization_thesis",
                False,
                "role-thesis.md still contains template placeholders",
                "Run `ai-career-toolkit personalize` or edit ~/.ai-career-toolkit/role-thesis.md.",
                level="warn",
            )
    return Check(
        "personalization_thesis",
        True,
        "role-thesis.md has content.",
        "",
        level="warn",
    )


# ---------------------------------------------------------------------------
# Main verify logic
# ---------------------------------------------------------------------------


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
                    f"Toolkit files not found at {w} (expected skills/, agents/, scripts/ inside)",
                    "Run `ai-career-toolkit init` to set up, or cd into your toolkit directory.",
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
                    "Run `ai-career-toolkit init` to set up your toolkit.",
                )
            )
            return _emit(results, output_format, critical=True)

    if root is None:
        raise RuntimeError("Toolkit root resolved to None unexpectedly.")
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
                "Run init or copy templates/role-thesis.md to ~/.ai-career-toolkit/.",
            )
        )

    # Personalization checks (warn level)
    results.append(_check_personalization_domains(settings))
    results.append(_check_personalization_role(settings))
    results.append(_check_personalization_thesis(role))

    if platform in ("cursor", "both"):
        results.append(_check_cursor_install(root))
    if platform in ("claude-code", "both"):
        results.append(_check_claude_install(root))

    return _emit(results, output_format, critical=False)


def _emit(results: list[Check], output_format: str, *, critical: bool) -> int:
    from ai_career_toolkit.ui import bold, green, red, yellow

    if output_format == "json":
        print(json.dumps([c.__dict__ for c in results], indent=2))
    else:
        for c in results:
            if c.ok:
                label = green("[  ok]")
            elif c.level == "warn":
                label = yellow("[warn]")
            else:
                label = red("[ gap]")
            print(f"        {label} {c.id}: {c.detail}")
            if not c.ok and c.fix:
                print(f"               fix: {c.fix}")
        if not critical:
            warns = sum(1 for c in results if not c.ok and c.level == "warn")
            passed = sum(1 for c in results if c.ok)
            parts = [f"{passed}/{len(results)} checks passed"]
            if warns:
                parts.append(f"{warns} warning{'s' if warns != 1 else ''}")
            print("")
            print(f"        {bold('Summary:')} {', '.join(parts)}.")
    if critical:
        return 2
    if any(not c.ok and c.level == "error" for c in results):
        return 1
    return 0
