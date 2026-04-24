"""Shared terminal UI helpers: ANSI colors, menus, formatted output."""

from __future__ import annotations

import os
import sys
import time

# ---------------------------------------------------------------------------
# Color support
# ---------------------------------------------------------------------------


def _use_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


def _wrap(code: str, text: str) -> str:
    if not _use_color():
        return text
    return f"\033[{code}m{text}\033[0m"


def bold(text: str) -> str:
    return _wrap("1", text)


def dim(text: str) -> str:
    return _wrap("2", text)


def green(text: str) -> str:
    return _wrap("32", text)


def yellow(text: str) -> str:
    return _wrap("33", text)


def cyan(text: str) -> str:
    return _wrap("36", text)


def red(text: str) -> str:
    return _wrap("31", text)


# ---------------------------------------------------------------------------
# Structured output
# ---------------------------------------------------------------------------


def header(title: str) -> None:
    print("")
    print(f"  {bold(title)}")
    print(f"  {'=' * len(title)}")
    print("")


def step(n: int, total: int, label: str) -> None:
    pause(0.3)
    print(f"  {bold(cyan(f'[{n}/{total}]'))} {bold(label)}")


def success(msg: str) -> None:
    print(f"        {green('✓')} {msg}")


def warn(msg: str) -> None:
    print(f"        {yellow('!')} {msg}")


def info(msg: str) -> None:
    print(f"        {cyan('→')} {msg}")


def detail(label: str, value: str) -> None:
    print(f"        {dim(label + ':')}  {value}")


def blank() -> None:
    print("")


def pause(seconds: float, message: str = "") -> None:
    if message:
        print(f"        {dim(message)}", end="", flush=True)
    if sys.stdout.isatty():
        time.sleep(seconds)
    if message:
        print("")


# ---------------------------------------------------------------------------
# Interactive menus
# ---------------------------------------------------------------------------


def _is_interactive() -> bool:
    return sys.stdin.isatty()


def pick_one(prompt: str, options: list[str], default: str | None = None) -> str:
    """Numbered single-select menu. Returns the chosen string."""
    if not _is_interactive():
        return default or options[0]

    print(f"  {bold(prompt)}")
    default_idx = None
    for i, opt in enumerate(options, 1):
        marker = ""
        if default and opt == default:
            default_idx = i
            marker = dim("  [current]")
        print(f"    {dim(f'{i:>2})')} {opt}{marker}")

    hint = f" [{default_idx}]" if default_idx else ""
    try:
        raw = input(f"  Choice{hint}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("")
        return default or options[0]

    if not raw:
        return default or options[0]

    # Handle "Other" — last option is always the custom entry
    try:
        idx = int(raw)
        if 1 <= idx <= len(options):
            chosen = options[idx - 1]
            if chosen.lower().startswith("other"):
                return _ask_custom("Type your own")
            return chosen
    except ValueError:
        pass

    return raw if raw else (default or options[0])


def pick_many(prompt: str, options: list[str], current: list[str] | None = None) -> list[str]:
    """Numbered multi-select menu. Enter numbers to toggle, empty Enter to confirm."""
    if not _is_interactive():
        return current or []

    selected: set[int] = set()
    if current:
        for i, opt in enumerate(options):
            if opt in current:
                selected.add(i)

    while True:
        print(f"  {bold(prompt)}  {dim('(enter numbers to toggle, Enter when done)')}")
        for i, opt in enumerate(options, 1):
            check = green("●") if (i - 1) in selected else dim("○")
            print(f"    {check} {dim(f'{i:>2})')} {opt}")

        sel_names = [options[i] for i in sorted(selected) if not options[i].lower().startswith("other")]
        if sel_names:
            print(f"  {dim('Selected:')} {', '.join(sel_names)}")

        try:
            raw = input("  Toggle: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            break

        if not raw:
            break

        for token in raw.replace(",", " ").split():
            try:
                idx = int(token) - 1
                if 0 <= idx < len(options):
                    if options[idx].lower().startswith("other"):
                        custom = _ask_custom("Type your own (comma-separated for multiple)")
                        if custom:
                            for item in custom.split(","):
                                item = item.strip()
                                if item and item not in options:
                                    options.append(item)
                                    selected.add(len(options) - 1)
                    elif options[idx].lower() == "none":
                        selected.clear()
                    elif idx in selected:
                        selected.discard(idx)
                    else:
                        selected.add(idx)
            except ValueError:
                pass

    result = [options[i] for i in sorted(selected) if not options[i].lower().startswith(("other", "none"))]
    return result


def _ask_custom(prompt: str) -> str:
    try:
        return input(f"    {cyan('→')} {prompt}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("")
        return ""


def ask(prompt: str, default: str = "") -> str:
    """Styled single-line input with default."""
    if not _is_interactive():
        return default
    suffix = f" {dim(f'[{default}]')}" if default else ""
    try:
        raw = input(f"  {prompt}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("")
        return default
    return raw if raw else default


def ask_freetext(prompt: str, hint: str = "", examples: list[str] | None = None, default: str = "") -> str:
    """Styled input with example hints shown in dim text."""
    if not _is_interactive():
        return default
    print(f"  {bold(prompt)}")
    if hint:
        print(f"  {dim(hint)}")
    if examples:
        print(f"  {dim('Examples:')}")
        for ex in examples:
            print(f"    {dim(ex)}")
    print("")
    try:
        raw = input(f"  {dim('>')} ").strip()
    except (EOFError, KeyboardInterrupt):
        print("")
        return default
    return raw if raw else default
