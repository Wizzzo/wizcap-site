#!/usr/bin/env bash
# Auto-format after every edit. Silent on success so it costs no tokens;
# on lint failure it prints only the last 20 lines and exits 2, which
# feeds the error back to Claude so it fixes it right away.
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
[ -f Makefile ] || exit 0

make -s format >/dev/null 2>&1 || true
if ! out=$(make -s lint 2>&1); then
  echo "$out" | tail -n 20 >&2
  exit 2
fi
exit 0
