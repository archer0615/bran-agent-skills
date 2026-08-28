#!/usr/bin/env sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd); codex_home=${CODEX_HOME:-"$HOME/.codex"}; target="$codex_home/skills"; dry_run=false; repair=false
while [ "$#" -gt 0 ]; do case "$1" in --dry-run) dry_run=true; shift;; --repair) repair=true; shift;; *) break;; esac; done
if [ "$#" -eq 0 ]; then set -- core coding research knowledge composite; fi
for category in "$@"; do
  case "$category" in core|coding|research|knowledge|composite) ;; *) echo "Unknown category: $category" >&2; exit 1;; esac
  for skill in "$root/skills/$category"/*; do
    [ -d "$skill" ] || continue
    name=$(basename "$skill"); dest="$target/$name"
    if "$dry_run"; then echo "Would install $name -> $skill"; continue; fi
    mkdir -p "$target"
    if [ -e "$dest" ] || [ -L "$dest" ]; then
      if [ ! -L "$dest" ] && ! "$repair"; then echo "Destination exists and is not a symlink: $dest (use --repair only after reviewing it)" >&2; exit 1; fi
      rm -rf "$dest"
    fi
    ln -s "$skill" "$dest"
  done
done
if "$dry_run"; then echo "Would install categories: $*"; exit 0; fi
echo "Installed categories: $*"; echo "Codex skills path: $target"
