#!/usr/bin/env bash
# Installs the gtm-outbound skill set into ~/.claude/skills/
#
# Usage:
#   ./install.sh              install
#   ./install.sh --dry-run    show what would happen, change nothing
#   ./install.sh --dest DIR   install somewhere other than ~/.claude/skills
#
# Existing directories are backed up rather than overwritten, so re-running never
# silently discards local edits.
#
# Backups go to ~/.claude/.skill-backups/<timestamp>/, NOT alongside the skills. A
# backup left inside ~/.claude/skills/ still contains a SKILL.md, so the harness
# registers it as a real skill -- a stale duplicate of every skill, competing with
# the live one for activation.

set -euo pipefail

SKILLS=(
  gtm-outbound
  gtm-outbound-offer
  gtm-outbound-list
  gtm-outbound-clay
  gtm-outbound-copy
  gtm-outbound-math
  gtm-outbound-score
  gtm-outbound-diagnose
  gtm-outbound-reply
)

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HOME}/.claude/skills"
AGENT_DEST="${HOME}/.claude/agents"
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --dest)    DEST="$2"; shift 2 ;;
    -h|--help) sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_ROOT="${HOME}/.claude/.skill-backups/${STAMP}"  # outside $DEST on purpose
say() { [[ $DRY_RUN -eq 1 ]] && echo "  [dry-run] $*" || echo "  $*"; }

back_up() {
  # back_up <path>  -- relocate out of the skills tree, preserving the leaf name
  [[ $DRY_RUN -eq 1 ]] && return 0
  mkdir -p "$BACKUP_ROOT"
  mv "$1" "$BACKUP_ROOT/$(basename "$1")"
}

echo "Installing gtm-outbound"
echo "  from: $SOURCE_ROOT"
echo "  to:   $DEST"
echo

# --- preflight ---------------------------------------------------------------
PY=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then PY="$candidate"; break; fi
done

if [[ -z "$PY" ]]; then
  echo "  WARNING: no python found on PATH." >&2
  echo "  The skill instructions install fine, but the five scripts will not run." >&2
  echo "  Install Python 3.10 or newer, then re-run preflight.py to verify." >&2
  echo
else
  if ! "$PY" "$SOURCE_ROOT/preflight.py" --quiet; then
    echo >&2
    echo "  Preflight failed. Fix the above before installing, or pass --dry-run" >&2
    echo "  to inspect. Skill files would install correctly; the scripts would not run." >&2
    exit 1
  fi
fi

# --- install -----------------------------------------------------------------
[[ $DRY_RUN -eq 0 ]] && mkdir -p "$DEST"

installed=0
for skill in "${SKILLS[@]}"; do
  src="$SOURCE_ROOT/$skill"
  dst="$DEST/$skill"

  if [[ ! -d "$src" ]]; then
    echo "  WARNING: missing source for '$skill' -- skipped" >&2
    continue
  fi

  if [[ -e "$dst" ]]; then
    say "backing up existing $skill -> .claude/.skill-backups/$STAMP/"
    back_up "$dst"
  fi

  say "installing $skill"
  [[ $DRY_RUN -eq 0 ]] && cp -R "$src" "$dst"
  installed=$((installed + 1))
done

# --- agents -------------------------------------------------------------------
AGENTS_SRC="$SOURCE_ROOT/gtm-outbound/agents"
if [[ -d "$AGENTS_SRC" ]]; then
  [[ $DRY_RUN -eq 0 ]] && mkdir -p "$AGENT_DEST"
  for agent in "$AGENTS_SRC"/*.md; do
    [[ -e "$agent" ]] || continue
    name="$(basename "$agent")"
    if [[ -e "$AGENT_DEST/$name" ]]; then
      say "backing up existing agent $name"
      back_up "$AGENT_DEST/$name"
    fi
    say "installing agent $name"
    [[ $DRY_RUN -eq 0 ]] && cp "$agent" "$AGENT_DEST/$name"
  done
fi

echo
if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry run complete. $installed skill(s) would be installed."
  echo "Re-run without --dry-run to apply."
else
  echo "Done. $installed skill(s) installed to $DEST"
  echo
  echo "Restart Claude Code (or start a new session) to pick them up."
  echo "Then try:  /gtm-outbound math"
fi
