"""Interactive Tier-0 personalization: collect targeting criteria and seed role-thesis."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from ai_career_toolkit.paths import default_data_home, resolve_toolkit_root

# ---------------------------------------------------------------------------
# Prompt helpers
# ---------------------------------------------------------------------------


def _input(prompt: str, default: str = "") -> str:
    if not sys.stdin.isatty():
        return default
    suffix = f" [{default}]" if default else ""
    try:
        ans = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        return default
    return ans if ans else default


def _input_list(prompt: str, current: list[str]) -> list[str]:
    """Prompt for a comma-separated list, showing *current* as the default."""
    default_display = ", ".join(current) if current else ""
    raw = _input(prompt + " (comma-separated)", default_display)
    if not raw:
        return current
    return [item.strip() for item in raw.split(",") if item.strip()]


def _input_optional(prompt: str, default: str = "") -> str:
    return _input(prompt + " (optional, press Enter to skip)", default)


# ---------------------------------------------------------------------------
# settings.yaml line-level read / write (no PyYAML dependency)
# ---------------------------------------------------------------------------


def _read_settings(path: Path) -> list[str]:
    if path.is_file():
        return path.read_text().splitlines(keepends=True)
    return []


def _parse_yaml_list(lines: list[str], key_indent: str, start_idx: int) -> tuple[list[str], int]:
    """Return (items, end_idx) for a YAML list block starting after a key line."""
    items: list[str] = []
    i = start_idx
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("- ") and lines[i].startswith(key_indent + "  "):
            items.append(stripped[2:].strip())
            i += 1
        elif stripped.startswith("# ") and lines[i].startswith(key_indent + "  "):
            i += 1
        elif stripped == "":
            i += 1
        else:
            break
    return items, i


def _find_key_line(lines: list[str], key: str) -> int | None:
    """Find the line index where a YAML key appears (supports nested with indent)."""
    pattern = re.compile(rf"^(\s*){re.escape(key)}\s*:")
    for i, line in enumerate(lines):
        if pattern.match(line):
            return i
    return None


def _write_scalar(lines: list[str], key: str, value: str) -> list[str]:
    """Set a scalar YAML value. Handles `key: value` and `key: # comment` forms."""
    idx = _find_key_line(lines, key)
    if idx is None:
        return lines
    line = lines[idx]
    m = re.match(r"^(\s*" + re.escape(key) + r"\s*:)\s*(.*)$", line)
    if not m:
        return lines
    prefix = m.group(1)
    existing = m.group(2).strip()
    if existing.startswith("#"):
        lines[idx] = f"{prefix} {value}  {existing}\n"
    else:
        lines[idx] = f"{prefix} {value}\n"
    return lines


def _write_list(lines: list[str], key: str, values: list[str]) -> list[str]:
    """Replace the YAML list block under *key* with *values*."""
    idx = _find_key_line(lines, key)
    if idx is None:
        return lines
    indent = re.match(r"^(\s*)", lines[idx]).group(1)  # type: ignore[union-attr]
    item_indent = indent + "    "

    # Find extent of old list (items + comments after the key line)
    old_start = idx + 1
    old_end = old_start
    while old_end < len(lines):
        s = lines[old_end].strip()
        if s == "" or s.startswith("- ") or s.startswith("# - ") or s.startswith("#"):
            if lines[old_end].startswith(item_indent) or lines[old_end].startswith(indent + "  ") or s == "":
                old_end += 1
                continue
        break

    new_block = [f"{item_indent}- {v}\n" for v in values] if values else []
    lines[old_start:old_end] = new_block
    return lines


def _read_scalar(lines: list[str], key: str) -> str:
    idx = _find_key_line(lines, key)
    if idx is None:
        return ""
    m = re.match(r"^\s*" + re.escape(key) + r"\s*:\s*(.*)$", lines[idx])
    if not m:
        return ""
    val = m.group(1).strip()
    if val.startswith("#"):
        return ""
    return val


def _read_yaml_list_values(lines: list[str], key: str) -> list[str]:
    idx = _find_key_line(lines, key)
    if idx is None:
        return []
    indent = re.match(r"^(\s*)", lines[idx]).group(1)  # type: ignore[union-attr]
    items, _ = _parse_yaml_list(lines, indent, idx + 1)
    return items


# ---------------------------------------------------------------------------
# role-thesis.md seeding
# ---------------------------------------------------------------------------

_THESIS_PLACEHOLDER = re.compile(r"<!--\s*.*?-->")


def _thesis_is_template(path: Path) -> bool:
    """Return True if the role-thesis still looks like the unfilled template."""
    if not path.is_file():
        return True
    text = path.read_text()
    without_placeholders = _THESIS_PLACEHOLDER.sub("", text)
    meaningful = [
        ln.strip()
        for ln in without_placeholders.splitlines()
        if ln.strip()
        and not ln.strip().startswith(("#", ">", "-", "**", "- [", "- **", "Use this", "Define your", "Score:"))
    ]
    return len(meaningful) < 3


def _seed_thesis_section(text: str, heading: str, content: str) -> str:
    """Replace the placeholder content under a ## heading with real content."""
    if not content:
        return text
    pattern = re.compile(
        rf"(## {re.escape(heading)}\n\n)"
        r"(- \*\*.*?\*\*:?\s*)<!--.*?-->\n?",
        re.DOTALL,
    )
    m = pattern.search(text)
    if m:
        replacement = m.group(1) + m.group(2).rstrip() + " " + content + "\n"
        text = text[: m.start()] + replacement + text[m.end() :]
    return text


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def handle_personalize(
    *,
    workspace: Path | None = None,
    data_home: Path | None = None,
    yes: bool = False,
) -> int:
    """Run the interactive Tier-0 personalization flow.

    Returns 0 on success.
    """
    if workspace is None:
        try:
            workspace = resolve_toolkit_root()
        except FileNotFoundError:
            print("Cannot locate toolkit root. Run `ai-career-toolkit init` first.", file=sys.stderr)
            return 1

    settings_path = workspace / "config" / "settings.yaml"
    data = data_home if data_home is not None else default_data_home()
    thesis_path = data / "role-thesis.md"

    # --- Read current state ---
    lines = _read_settings(settings_path)
    cur_role = _read_scalar(lines, "role")
    cur_level = _read_scalar(lines, "level")
    cur_domains = _read_yaml_list_values(lines, "domains")
    cur_geo = _read_yaml_list_values(lines, "geo_remote")
    cur_excl = _read_yaml_list_values(lines, "exclusions")

    if yes:
        print("Personalization: non-interactive mode — using existing config values.")
        _print_summary(settings_path, thesis_path, cur_role, cur_level, cur_domains)
        return 0

    print("")
    print("Personalize your toolkit")
    print("========================")
    print("These answers feed into target-list-generator, opportunity-evaluator,")
    print("and other skills so they tailor output to your search.")
    print("")

    # --- Collect inputs ---
    new_role = _input("Target role", cur_role or "Software Engineer")
    new_level = _input("Seniority level", cur_level or "Senior")
    new_domains = _input_list("Target domains", cur_domains)
    new_geo = _input_list("Geo / remote preferences", cur_geo)
    new_excl = _input_list("Exclusions", cur_excl)

    # --- Write settings.yaml ---
    if new_role:
        lines = _write_scalar(lines, "role", new_role)
    if new_level:
        lines = _write_scalar(lines, "level", new_level)
    if new_domains:
        lines = _write_list(lines, "domains", new_domains)
    if new_geo:
        lines = _write_list(lines, "geo_remote", new_geo)
    if new_excl:
        lines = _write_list(lines, "exclusions", new_excl)

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text("".join(lines))

    # --- Seed role-thesis if still template ---
    if _thesis_is_template(thesis_path):
        print("")
        print(f"Your role thesis ({thesis_path}):")
        print("This file drives opportunity-evaluator and career-guide recommendations.")
        print("")
        must_haves = _input_optional("Must-haves (comp floor, scope, location — 1-2 sentences)")
        non_neg = _input_optional("Non-negotiables (culture or role dealbreakers)")
        if must_haves or non_neg:
            template_src = workspace / "templates" / "role-thesis.md"
            if thesis_path.is_file():
                text = thesis_path.read_text()
            elif template_src.is_file():
                text = template_src.read_text()
            else:
                text = ""
            if must_haves:
                text = _seed_thesis_section(text, "Must-Haves", must_haves)
            if non_neg:
                text = _seed_thesis_section(text, "Non-Negotiables", non_neg)
            thesis_path.parent.mkdir(parents=True, exist_ok=True)
            thesis_path.write_text(text)
    else:
        print("")
        print(f"Role thesis already has content: {thesis_path}")

    _print_summary(settings_path, thesis_path, new_role, new_level, new_domains)
    return 0


def _print_summary(
    settings_path: Path,
    thesis_path: Path,
    role: str,
    level: str,
    domains: list[str],
) -> None:
    print("")
    print("Personalization saved.")
    print(f"  settings.yaml:  {settings_path}")
    print(f"  role-thesis.md: {thesis_path}")
    print("")
    if domains and role and level:
        domain_str = " and ".join(domains[:2])
        if len(domains) > 2:
            domain_str += f" (+{len(domains) - 2} more)"
        print("Your first useful prompt (paste into your AI agent):")
        print(f'  "Build me a target company list for {domain_str} {level} {role} roles"')
        print("")
