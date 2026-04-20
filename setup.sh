#!/usr/bin/env bash
# First-run setup for ai-career-toolkit.
# Scaffolds local config directory and personal data directory.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${AI_CAREER_TOOLKIT_HOME:-${HOME}/.ai-career-toolkit}"
CONFIG_DIR="${SCRIPT_DIR}/config"

usage() {
  echo "Usage: $(basename "$0") [--dry-run]"
  echo ""
  echo "Sets up local directories for ai-career-toolkit:"
  echo "  1. ./config/          — toolkit settings (gitignored)"
  echo "  2. ~/.ai-career-toolkit/  — personal career data"
  echo ""
  echo "Options:"
  echo "  --dry-run    Print what would be created without writing"
  echo "  --help       Show this help"
}

DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
  shift
done

ensure_dir() {
  local dir="$1"
  local desc="$2"
  if [[ -d "$dir" ]]; then
    echo "  exists: $dir ($desc)"
  elif [[ $DRY_RUN -eq 1 ]]; then
    echo "  would create: $dir ($desc)"
  else
    mkdir -p "$dir"
    echo "  created: $dir ($desc)"
  fi
}

copy_if_missing() {
  local src="$1"
  local dest="$2"
  if [[ -e "$dest" ]]; then
    echo "  exists: $dest"
  elif [[ $DRY_RUN -eq 1 ]]; then
    echo "  would copy: $src → $dest"
  else
    cp -R "$src" "$dest"
    echo "  copied: $src → $dest"
  fi
}

echo ""
echo "ai-career-toolkit setup"
echo "======================="
echo ""

echo "1. Local config (${CONFIG_DIR}):"
ensure_dir "$CONFIG_DIR" "toolkit settings"

if [[ -d "${SCRIPT_DIR}/config.example" ]]; then
  for item in "${SCRIPT_DIR}/config.example"/*; do
    [[ -e "$item" ]] || continue
    name="$(basename "$item")"
    copy_if_missing "$item" "${CONFIG_DIR}/${name}"
  done
fi

echo ""
echo "2. Personal data directory (${DATA_DIR}):"
ensure_dir "$DATA_DIR" "personal career data"
ensure_dir "${DATA_DIR}/voice-pack" "voice pack"
ensure_dir "${DATA_DIR}/source-lists" "per-domain company list drafts"
ensure_dir "${DATA_DIR}/opportunities" "opportunity tracking"
ensure_dir "${DATA_DIR}/interview-notes" "interview notes"
ensure_dir "${DATA_DIR}/weekly-reviews" "weekly reviews"

if [[ -f "${CONFIG_DIR}/role-thesis.md" ]] && [[ ! -f "${DATA_DIR}/role-thesis.md" ]]; then
  copy_if_missing "${CONFIG_DIR}/role-thesis.md" "${DATA_DIR}/role-thesis.md"
fi

if [[ -f "${CONFIG_DIR}/target-companies.tsv" ]] && [[ ! -f "${DATA_DIR}/target-companies.tsv" ]]; then
  copy_if_missing "${CONFIG_DIR}/target-companies.tsv" "${DATA_DIR}/target-companies.tsv"
fi

echo ""
if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry run complete — no files were written."
else
  echo "Setup complete."
  echo ""
  echo "Next steps:"
  echo "  1. Edit config/settings.yaml with your preferences"
  echo "  2. Customize config/voice-pack/ with your writing style"
  echo "  3. Fill out ~/.ai-career-toolkit/role-thesis.md with your target role"
  echo "  4. Run scripts/install.sh to install skills, agents, and rules into your AI agent platform"
fi
