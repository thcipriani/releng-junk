#!/usr/bin/env python
# This is fucking stupid, but it seems to work.
import os
import re
import subprocess
import sys

from collections import namedtuple
from distutils.version import LooseVersion

class VersionDiff:
    def __init__(self):
        self.old_version = None
        self.new_version = None

REPO = os.environ['REPO']
WIKIS = {}
REVISION = sys.stdin.readline().strip()
IS_ROLLBACK = False

def set_version(version_diff, wikiversions_line):
    if wikiversions_line['diff'] == '-':
        version_diff.old_version = LooseVersion(wikiversions_line['version'])
    else:
        version_diff.new_version = LooseVersion(wikiversions_line['version'])

    return version_diff

diff = subprocess.check_output([
    'git', '-C', REPO, 'diff-tree', '-p', '-U0', REVISION, 'wikiversions.json'
])

# That's right. It's a regex for parsing a diff. Fight me.
for line in diff.splitlines():
    if not re.search(r'^(-|\+)\s+', line):
        continue
    regex = ''.join([
        r'(?P<diff>(-|\+))\s+',              # +/-
        r'"(?P<wiki>\w+)":\s+',              # "Wiki:"
        r'"php-(?P<version>[0-9\.wmf-]+)"', # "php-1.3x.0-wmf.x"
    ])
    line = re.search(regex, line).groupdict()
    wiki = line['wiki']
    version_diff = WIKIS.get(wiki, VersionDiff())
    WIKIS[wiki] = set_version(version_diff, line)

for wiki, version in WIKIS.items():
    # print('{} > {}'.format(version.old_version, version.new_version))
    try:
        if version.old_version > version.new_version:
            IS_ROLLBACK = True
    except AttributeError:
        # This happens when you add or remove a wiki -- there won't be an
        # old_version or a new_version, respectively
        pass


print(IS_ROLLBACK)
