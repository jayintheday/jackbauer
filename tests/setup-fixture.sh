#!/usr/bin/env bash
# Copy the meridian-digest fixture to a scratch directory as its own git repo,
# with the single 2026-09-08 commit the answer key relies on (planted issue #13).
# Usage: tests/setup-fixture.sh [target-dir]   (default: a new temp dir)
set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)/fixtures/meridian-digest"
dest="${1:-$(mktemp -d)/meridian-digest}"

if [ -e "$dest" ]; then
  echo "refusing to overwrite existing $dest" >&2
  exit 1
fi

mkdir -p "$dest"
cp -R "$src/." "$dest/"
cd "$dest"
git init -q
git add -A
GIT_AUTHOR_NAME="Meridian Ops" GIT_AUTHOR_EMAIL="ops@meridian.example" \
GIT_COMMITTER_NAME="Meridian Ops" GIT_COMMITTER_EMAIL="ops@meridian.example" \
GIT_AUTHOR_DATE="2026-09-08T10:12:00Z" GIT_COMMITTER_DATE="2026-09-08T10:12:00Z" \
  git commit -q -m "Weekly digest pipeline"

echo "$dest"
