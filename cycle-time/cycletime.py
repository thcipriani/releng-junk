"""
Cycle Time
==========

> The time from deciding that you need to make a change to having it in
> production is known as the _cycle time_.
>
> -- _Continuous Delivery_ by Jez Humble and David Farley

This is an attempt to approximate cycle time for MediaWiki core at the point
in time of each train. It uses the same mechanism as our deploy-notes to
approximate cycle time for each patch on a particular train.

WMF.14
------
<https://tools.wmflabs.org/sal/log/AWiBncXMzCcrHSwq4yOt>
python3 cycletime.py \
    'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.33.0-wmf.13..75b61dd?format=JSON' \
    '2019-01-24T20:47:00+00:00'

TOTAL CHANGES: 79
MIN: 2 days, 0:54:02
MAX: 32 days, 15:01:10
AVG: 6 days, 5:48:02

WMF.13
------
<https://tools.wmflabs.org/sal/log/AWhdbE5XA1BDhGjCNMSn>
python3 cycletime.py \
    'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.33.0-wmf.12..baa5168?no-merges&format=JSON' \
    '2019-01-17T20:06:00+00:00'


TOTAL CHANGES: 32
MIN: 2 days, 18:47:24
MAX: 31 days, 2:32:21
AVG: 6 days, 5:23:55


WMF.12
------
<https://tools.wmflabs.org/sal/log/AWg5ZF8LA1BDhGjCFOx5>
python3 cycletime.py \
    'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.33.0-wmf.9..1bc0e29?no-merges&format=JSON' \
    '2019-01-10T20:11:00+00:00'

TOTAL CHANGES: 87
MIN: 2 days, 2:23:58
MAX: 22 days, 23:25:24
AVG: 10 days, 7:37:39
"""

import datetime
import json
import re
import sys

from dateutil.parser import parse as dateutil_parse
import requests

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

def valid_change(change):
    """
    validates a change based on a commit
    """
    for skip_message in SKIP_MESSAGES:
        if re.search(skip_message, change['message']):
            return False

    return True


def git_log(url):
    """
    Fetches and loads the json git log from gitiles
    """
    req = requests.get(url)

    if req.status_code != 200:
        if req.status_code == 404:
            return {'log': []}
        raise requests.exceptions.HTTPError(req)

    log_json = req.text
    # remove )]}' since because gerrit.
    return json.loads(log_json[4:])


def main(args):
    train_url = args[0]
    train_time = dateutil_parse(args[1])

    changes = git_log(train_url)
    total_seconds = 0
    max_diff = datetime.timedelta(seconds=0)
    min_diff = datetime.timedelta.max
    valid_changes = 0

    for change in changes['log']:
        if not valid_change(change):
            continue

        valid_changes += 1
        commit_datetime = dateutil_parse(change['committer']['time'])
        diff = train_time - commit_datetime

        if diff > max_diff:
            max_diff = diff
        if diff < min_diff:
            min_diff = diff

        print(diff.total_seconds())
        total_seconds += diff.total_seconds()

    # average_cycle = datetime.timedelta(seconds=(total_seconds // len(changes['log'])))
    # print('TOTAL CHANGES: {}'.format(valid_changes))
    # print('MIN: {}'.format(min_diff))
    # print('MAX: {}'.format(max_diff))
    # print('AVG: {}'.format(average_cycle))

if __name__ == '__main__':
    main(sys.argv[1:])
