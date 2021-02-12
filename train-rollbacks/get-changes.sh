#!/usr/bin/env bash

set -eu

# Get the oldest change that mentions $VERSION
OLDEST=$(git -C "$REPO" log --grep="\b$VERSION\b" --reverse --format='%H' -- wikiversions.json | head -1)

# Get every change to wikiversions.json between that change and HEAD
CHANGES=$(git -C "$REPO" log --format='%H' "$OLDEST"..HEAD -- wikiversions.json)

# Check whether that change was a revert
for change in $CHANGES; do
    printf "%s" "$change"
    IS_REVERT=$(echo "$change" | REPO="$REPO" ./diff-is-revert.py)
    printf '\t%s\n' "$IS_REVERT"
done
