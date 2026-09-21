#!/usr/bin/env bash
set -euo pipefail

platform="${1:-all}"
case "$platform" in
  grok|claude|cursor|hermes|gemini|antigravity|antigravity-cli|all) ;;
  *)
    echo "usage: $0 [grok|claude|cursor|hermes|gemini|antigravity|antigravity-cli|all]" >&2
    exit 2
    ;;
esac

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
skill_src="$repo_root/SKILL.md"
readme_src="$repo_root/README.md"
refs_src="$repo_root/references"
if [[ ! -f "$skill_src" ]]; then
    echo "SKILL.md not found at $skill_src" >&2
    exit 1
fi

dest_for() {
  local name="$1"
  if [[ -n "${UPDATE_HARNESS_SKILLS:-}" ]]; then
    printf '%s\n' "$UPDATE_HARNESS_SKILLS/musk-backlog"
    return
  fi
  local home="${HOME}"
  case "$name" in
    grok)
      local root="${GROK_HOME:-$home/.grok}"
      printf '%s\n' "$root/skills/musk-backlog"
      ;;
    hermes)
      local root="${HERMES_HOME:-$home/.hermes}"
      printf '%s\n' "$root/skills/musk-backlog"
      ;;
    claude) printf '%s\n' "$home/.claude/skills/musk-backlog" ;;
    cursor) printf '%s\n' "$home/.cursor/skills/musk-backlog" ;;
    gemini) printf '%s\n' "$home/.gemini/config/skills/musk-backlog" ;;
    antigravity) printf '%s\n' "$home/.gemini/antigravity/skills/musk-backlog" ;;
    antigravity-cli) printf '%s\n' "$home/.gemini/antigravity-cli/skills/musk-backlog" ;;
    *)
      echo "Unknown platform $name" >&2
      return 1
      ;;
  esac
}

install_to() {
  local name="$1"
  local dest
  dest="$(dest_for "$name")"
  mkdir -p "$dest"
  cp "$skill_src" "$dest/SKILL.md"
  if [[ -f "$readme_src" ]]; then
    cp "$readme_src" "$dest/README.md"
  fi
  if [[ -d "$refs_src" ]]; then
    rm -rf "$dest/references"
    cp -R "$refs_src" "$dest/references"
  fi
  echo "Installed $name -> $dest"
}

if [[ "$platform" == "all" ]]; then
  for t in grok claude cursor hermes gemini antigravity antigravity-cli; do
    install_to "$t"
  done
else
  install_to "$platform"
fi
