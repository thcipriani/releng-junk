#!/usr/bin/env python
# Quick script to parse json output of gerrit. Output is a list of files
# that are in the latest revision of a merged change list and the amount of
# times that file has been seen in the json input.
import collections
import json
import os

BACKPORT_CNT = collections.Counter()


def map_project(name):
    if name == 'mediawiki/core':
        return 'mediawiki'
    return name


def make_path(project, fn):
    return os.path.join(map_project(project), fn)


if __name__ == '__main__':
    with open('backports-to-1.36.json') as f:
        backports = json.load(f)

    for backport in backports:
        subject = backport['subject']

        # Skip all the search satisfaction A/B tests
        if 'a/b test' in subject.lower():
            continue

        project = backport['project']
        revisions = backport['revisions']
        latest_revision = revisions[sorted(revisions, reverse=True)[0]]
        for fn in latest_revision['files'].keys():
            BACKPORT_CNT[make_path(project, fn)] += 1

    for path, cnt in BACKPORT_CNT.most_common():
        print('{}\t{}'.format(cnt, path))
