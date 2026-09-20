#!/bin/bash
# Push the site to GitHub (Netlify auto-deploys from main). Run from the Mac VM: bash tools/deploy.sh "message"
set -e
cd "$(dirname "$0")/.."
TOKEN_FILE="$HOME/mnt/Projects/.polycrafted-deploy-token"
[ -f "$TOKEN_FILE" ] || { echo "token file missing: $TOKEN_FILE"; exit 1; }
python3 tools/assemble.py
git add -A
git -c commit.gpgsign=false commit -q -m "${1:-Site update}" || echo "nothing to commit"
git -c credential.helper='!f(){ echo username=x-access-token; echo password='"$(cat "$TOKEN_FILE")"'; }; f' push origin main
echo "pushed; Netlify deploys in ~30s: https://thepolycrafted.com"
