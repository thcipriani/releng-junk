#!/usr/bin/env bash
printf '{\n"constraints": {"columnPHIDs": ["PHID-PCOL-2m5ef4rehupj3kxnprgy"]}\n}\n' | arc call-conduit maniphest.search | jq -r '.response.data[]' > yaks.jsons
