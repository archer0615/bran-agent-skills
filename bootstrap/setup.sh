#!/usr/bin/env sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd); codex_home=${CODEX_HOME:-"$HOME/.codex"}; target="$codex_home/skills"
for category in "$@"; do case "$category" in core|coding|research|knowledge|composite) ;; *) echo "Unknown category: $category" >&2; exit 1;; esac; for skill in "$root/skills/$category"/*; do [ -d "$skill" ] || continue; name=$(basename "$skill"); dest="$target/$name"; mkdir -p "$target"; if [ -e "$dest" ] || [ -L "$dest" ]; then [ -L "$dest" ] || continue; rm "$dest"; fi; ln -s "$skill" "$dest"; done; done
echo "Installed categories: $*"
