#!/usr/bin/env bash
# Pass in the cycle time file and it'll find the p-95 in days

CYCLE_TIME_FILE="$1"
P95=$(wc -l < "$CYCLE_TIME_FILE")

sort "$CYCLE_TIME_FILE" | nl | grep -P "^\s+${P95}" | awk '{print $2}'
