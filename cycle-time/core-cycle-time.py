#!/usr/bin/env python

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta

from dateutil.parser import parse as dateutil_parse


GITILES_CORE = 'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/'


# Messages we don't want to see in the git log
SKIP_MESSAGES = [
    'Localisation updates from',
    # Fix for escaping fail leaving a commit summary of $COMMITMSG
    'COMMITMSG',
    r'Add (\.gitreview( and )?)?\.gitignore',
    # Branching commit; set $wgVersion, defaultbranch, add submodules
    'Creating new WMF',
    'Updating development dependencies',
    # git submodule autobumps
    r'Updated mediawiki\/core',
]


def valid_change(log_message):
    """
    validates a change based on a commit
    """
    for skip_message in SKIP_MESSAGES:
        if re.search(skip_message, log_message):
            return False

    return True


def parse_args(args=None):
    """
    Parse args
    """
    ap = argparse.ArgumentParser()
    ap.add_argument('-C', '--core-path', required=True, help='Path to core checkout')
    ap.add_argument(
        '-w',
        '--wmf-version',
        dest='wmf_versions',
        action='append',
        required=True,
        help='wmf version'
    )
    return ap.parse_args()


def p95_time(git_logs, train_time):
    times = []
    for log in git_logs:
        log = log.split()
        log_message = log[:-1]
        log_epoch = log[-1]
        if not valid_change(' '.join(log_message)):
            continue
        times.append(train_time - int(log_epoch))

    times = sorted(times)
    return times[int(len(times) * 0.95)]

def format_seconds(seconds):
    """
    Human readable seconds

	<https://stackoverflow.com/a/4048773>
    """
    sec = timedelta(seconds=seconds)
    d = datetime(1, 1, 1) + sec

    return '%d:%d:%d:%d' % (d.day-1, d.hour, d.minute, d.second)


def previous_version(version, path):
    """
    Get the previous version for version numbers like 1.35.0-wmf.10
    """
    version = version.split('.')
    last_digit = int(version[-1]) - 1

    if last_digit <= 0:
        raise RuntimeError('I\'m too stupid for this shit')

    last_version = os.path.join('wmf', '.'.join(version[:-1] + [str(last_digit)]))
    if subprocess.check_output(['git', '-C', path, 'for-each-ref', os.path.join('refs', 'remotes', 'origin', last_version)]):
        return os.path.join('origin', last_version)
    else:
        raise RuntimeError('Last version "%s" not found', last_version)


def git_log(git_range, path='.'):
    """
    git log of changes between old version and the train branch point
    """
    return subprocess.check_output([
        'git',
        '-C',
        path,
        'log',
        '--no-merges',
        "--format=%s %ct",
        git_range], text=True).splitlines()


def main(args=None):
    args = parse_args(args)
    path = args.core_path
    versions = args.wmf_versions
    total_p95 = 0
    for version in versions:
        if ',' in version:
            old_version, version = version.split(',')
            old_version = os.path.join('origin', 'wmf', old_version)
        else:
            old_version = previous_version(version, path)
        train_sha, train_time = subprocess.check_output(
            ['git', '-C', path, 'log', '--format=%H %ct', '--reverse', 'origin/master..origin/wmf/{}'.format(version)],
            text=True
        ).splitlines()[0].split()
        train_time = int(train_time)
        git_range = '{}..{}'.format(str(old_version), str(train_sha))
        p95 = p95_time(git_log(git_range, path), train_time)
        total_p95 += p95
        print('{} - {}'.format(version, format_seconds(p95)))

    print('Average p95: {}'.format(format_seconds(int(total_p95/len(versions)))))


if __name__ == '__main__':
    main(sys.argv[1:])
