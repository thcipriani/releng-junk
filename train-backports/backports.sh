#!/bin/bash

# Get a list of backports (with file names) of changes backported to 1.36
curl -s 'https://gerrit.wikimedia.org/r/changes/?q=branch:^wmf/1\.36.*+is:merged+-owner:TrainBranchBot&o=CURRENT_REVISION&o=CURRENT_FILES' \
    | tail -c +6 > backports-to-1.36.json
