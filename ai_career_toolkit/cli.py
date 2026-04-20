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

    p_init = sub.add_parser("init", help="Materialize toolkit files (if needed), create config and data directories")
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

    p_verify = sub.add_parser("verify", help="Check toolkit layout, config, data home, and optional IDE install")
    p_verify.add_argument(
        "--ide",
        choices=("none", "cursor", "claude-code", "both"),
        default="none",
        help="Also verify IDE file installs (default: none)",
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

    p_inst = sub.add_parser(
        "install",
        help="Run scripts/install.sh for Cursor or Claude Code (bash required)",
    )
    p_inst.add_argument(
        "--platform",
        choices=("cursor", "claude-code"),
        required=True,
    )
    p_inst.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Toolkit root containing scripts/install.sh",
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
                ide=args.ide,
                workspace=args.workspace,
                output_format=args.format,
            )
        if args.command == "install":
            from ai_career_toolkit.commands.init_cmd import handle_install

            return handle_install(args)
    except KeyboardInterrupt:
        return 130
    except (RuntimeError, FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
