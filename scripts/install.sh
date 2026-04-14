#!/usr/bin/env bash
# Install ai-career-toolkit skills and agents into a supported AI platform.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
DRY_RUN=0
PLATFORM=""

usage() {
  echo "Usage: $(basename "$0") [--platform cursor|claude-code] [--dry-run]"
  echo ""
  echo "Install skills and agents into your AI agent platform."
  echo ""
  echo "Options:"
  echo "  --platform PLATFORM  Target platform: cursor, claude-code (default: auto-detect)"
  echo "  --dry-run            Print what would be copied without writing"
  echo "  --help               Show this help"
  echo ""
  echo "Platforms:"
  echo "  cursor       Copies to ~/.cursor/skills/ and ~/.cursor/agents/"
  echo "  claude-code  Copies to .claude/skills/ and .claude/agents/ in current project"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform)
      PLATFORM="$2"
      shift
      ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
  shift
done

auto_detect_platform() {
  if [[ -d "${HOME}/.cursor" ]]; then
    echo "cursor"
  elif command -v claude &>/dev/null; then
    echo "claude-code"
  else
    echo ""
  fi
}

if [[ -z "$PLATFORM" ]]; then
  PLATFORM="$(auto_detect_platform)"
  if [[ -z "$PLATFORM" ]]; then
    echo "Error: Could not auto-detect platform. Use --platform to specify." >&2
    usage >&2
    exit 1
  fi
  echo "Auto-detected platform: $PLATFORM"
fi

case "$PLATFORM" in
  cursor)
    SKILLS_DEST="${HOME}/.cursor/skills"
    AGENTS_DEST="${HOME}/.cursor/agents"
    ;;
  claude-code)
    SKILLS_DEST=".claude/skills"
    AGENTS_DEST=".claude/agents"
    ;;
  *)
    echo "Error: Unsupported platform '$PLATFORM'. Use: cursor, claude-code" >&2
    exit 1
    ;;
esac

copy_file() {
  local src="$1"
  local dest="$2"
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "  would copy: $src → $dest"
  else
    mkdir -p "$(dirname "$dest")"
    cp "$src" "$dest"
    echo "  copied: $(basename "$src") → $dest"
  fi
}

copy_dir() {
  local src="$1"
  local dest="$2"
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "  would copy: $src/ → $dest/"
  else
    mkdir -p "$dest"
    shopt -s dotglob nullglob
    for item in "$src"/*; do
      [[ -e "$item" ]] || continue
      cp -R "$item" "$dest/"
    done
    shopt -u dotglob nullglob
    echo "  copied: $(basename "$src")/ → $dest/"
  fi
}

echo ""
echo "Installing ai-career-toolkit → $PLATFORM"
echo ""

echo "Skills:"
shopt -s nullglob
for skill_dir in "${REPO_ROOT}/skills"/*/; do
  [[ -d "$skill_dir" ]] || continue
  name="$(basename "$skill_dir")"
  copy_dir "$skill_dir" "${SKILLS_DEST}/${name}"
done
shopt -u nullglob

echo ""
echo "Agents:"
shopt -s nullglob
for agent_file in "${REPO_ROOT}/agents"/*.md; do
  [[ -f "$agent_file" ]] || continue
  copy_file "$agent_file" "${AGENTS_DEST}/$(basename "$agent_file")"
done
shopt -u nullglob

echo ""
if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry run complete — no files were written."
else
  echo "Installation complete."
  echo ""
  if [[ "$PLATFORM" == "cursor" ]]; then
    echo "Restart Cursor or reload the window if skills/agents don't appear immediately."
  elif [[ "$PLATFORM" == "claude-code" ]]; then
    echo "Skills and agents are installed in the current project directory."
    echo "Start a new Claude Code session to pick them up."
  fi
fi
