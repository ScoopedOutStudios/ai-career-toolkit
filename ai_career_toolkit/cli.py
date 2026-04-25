"""Entry point: `ai-career-toolkit` console script."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ai_career_toolkit import __version__


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-career-toolkit",
        description="Guided setup and verification for the ai-career-toolkit skill pack.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser(
        "init",
        help="Set up the toolkit: scaffold files, personalize, install into AI platform, and verify",
    )
    p_init.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Non-interactive: use defaults, do not prompt",
    )
    p_init.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Directory for skills/agents/scripts (default: repo root if editable, else ~/ai-career-toolkit)",
    )
    p_init.add_argument(
        "--data-home",
        type=Path,
        default=None,
        help="Override personal data directory (default: ~/.ai-career-toolkit or AI_CAREER_TOOLKIT_HOME)",
    )
    p_init.add_argument(
        "--platform",
        choices=("cursor", "claude-code"),
        default=None,
        help="Target platform to install into (default: auto-detect or ask interactively)",
    )
    p_init.add_argument(
        "--scope",
        choices=("local", "global"),
        default="local",
        help="Install scope for Cursor: local (workspace .cursor/) or global (~/.cursor/). Default: local",
    )
    p_init.add_argument(
        "--reinstall",
        action="store_true",
        help="Re-install platform files only (skip scaffold and personalize). Use after git pull.",
    )
    p_init.add_argument(
        "--personalize",
        action="store_true",
        help="Re-run personalization only (skip scaffold and install). Use to change targeting mid-search.",
    )

    p_verify = sub.add_parser(
        "verify",
        help="Check toolkit layout, config, data home, and platform installs",
    )
    p_verify.add_argument(
        "--platform",
        choices=("none", "cursor", "claude-code", "both"),
        default="none",
        metavar="TARGET",
        help="Also verify install destinations for this platform (default: none)",
    )
    p_verify.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Toolkit root to validate (default: auto-discover)",
    )
    p_verify.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        if args.command == "init":
            from ai_career_toolkit.commands.init_cmd import handle_init

            return handle_init(args)
        if args.command == "verify":
            from ai_career_toolkit.commands.verify_cmd import run_verify

            return run_verify(
                platform=args.platform,
                workspace=args.workspace,
                output_format=args.format,
            )
    except KeyboardInterrupt:
        return 130
    except (RuntimeError, FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
