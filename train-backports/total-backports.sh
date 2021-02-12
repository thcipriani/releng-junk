#!/usr/bin/env bash

CHANGES=$(jq -r '.[].change_id' <  backports-to-1.36.json | wc -l)
printf 'Total backports: %d\n' "$CHANGES"
