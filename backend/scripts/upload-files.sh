#!/usr/bin/env bash
# Upload every template in ../files (and the catalogue) to the R2 bucket.
# Usage: bash scripts/upload-files.sh --remote   (or --local for wrangler dev)
set -euo pipefail
MODE="${1:---remote}"
BUCKET="pm-toolkit-files"
cd "$(dirname "$0")/.."
for f in ../frontend/files/*; do
  name="$(basename "$f")"
  case "$name" in
    *.docx) type="application/vnd.openxmlformats-officedocument.wordprocessingml.document" ;;
    *.xlsx) type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ;;
    *.pptx) type="application/vnd.openxmlformats-officedocument.presentationml.presentation" ;;
    *) continue ;;
  esac
  echo "Uploading $name"
  npx wrangler r2 object put "$BUCKET/files/$name" --file "$f" --content-type "$type" "$MODE"
done
echo "Uploading catalog.json"
npx wrangler r2 object put "$BUCKET/catalog.json" --file src/catalog.json --content-type "application/json" "$MODE"
