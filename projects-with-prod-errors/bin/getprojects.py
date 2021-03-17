#!/usr/bin/env python3
"""
getprojects.py
--------------

USAGE:
    python3 getprojects.py > ../README.txt

WHAT
    1. Query phabricator for all projects with "group" icon (this should
       be all "teams", roughly)
    2. Query phabriactor for all tasks in any state on the Production Errors
       workboard: https://phabricator.wikimedia.org/tag/wikimedia-production-error/
       This uses PHID `PHID-PROJ-4uc7r7pdosfsk55qg7f6`
    3. For each of the many tags associated with each task increment the count
       of tasks associated with the PHID by 1 for each task on which a PHID is
       tagged.
    4. Bitwise & the set of "teams" with the tags PHID counter keys
    5. The remaining PHIDs are teams with tasks on the workboard
    6. Sort the team tag PHIDs counter by task count
    7. Print the team tag name followed by the task count
"""
import os
import sys

import json
import requests
import subprocess

from collections import Counter


def flatten_for_post(h, result=None, kk=None):
    """
    Since phab expects x-url-encoded form post data (meaning each
    individual list element is named). AND because, evidently, requests
    can't do this for me, I found a solution via stackoverflow.

    See also:
    <https://secure.phabricator.com/T12447>
    <https://stackoverflow.com/questions/26266664/requests-form-urlencoded-data/36411923>
    """
    if result is None:
        result = {}

    if isinstance(h, str) or isinstance(h, bool):
        result[kk] = h
    elif isinstance(h, list) or isinstance(h, tuple):
        for i, v1 in enumerate(h):
            flatten_for_post(v1, result, '%s[%d]' % (kk, i))
    elif isinstance(h, dict):
        for (k, v) in h.items():
            key = k if kk is None else "%s[%s]" % (kk, k)
            if isinstance(v, dict):
                for i, v1 in v.items():
                    flatten_for_post(v1, result, '%s[%s]' % (key, i))
            else:
                flatten_for_post(v, result, key)
    return result


class Phab(object):
    def __init__(self):
        self.phab_url = 'https://phabricator.wikimedia.org/api/'

        self.conduit_token = self._get_token()

    def _get_token(self):
        """
        Use the $CONDUIT_TOKEN envvar, fallback to whatever is in ~/.arcrc
        """
        token = None
        token_path = os.path.expanduser('~/.arcrc')
        if os.path.exists(token_path):
            with open(token_path) as f:
                arcrc = json.load(f)
                token = arcrc['hosts'][self.phab_url]['token']

        return os.environ.get('CONDUIT_TOKEN', token)

    def query(self, method, data):
        """
        Helper method to query phab via requests and return json
        """
        data['api.token'] = self.conduit_token
        data = flatten_for_post(data)
        r = requests.post(
            os.path.join(self.phab_url, method),
            data=data)
        r.raise_for_status()
        return r.json()

    def query_all(self, method, data):
        ret = []
        after = 0
        while after is not None:
            data['after'] = after
            print('Querying "{}:{}"'.format(method, after), file=sys.stderr)
            results = self.query(method, data)
            ret += results['result']['data']
            after = results['result']['cursor']['after']
        return ret

    def groups(self):
        groups = {}
        results = self.query_all('project.search', {
            "constraints": {
                "icons": [
                  "group"
                ]
            }
        })
        for result in results:
            has_parent = result['fields']['parent']
            if has_parent:
                groups[has_parent['phid']] = has_parent['name']
                continue
            groups[result['phid']] = result['fields']['name']
        return groups

    def tasks(self):
        return p.query_all('maniphest.search', {
            "constraints": {
                "modifiedStart": int(subprocess.check_output(['date', '+%s', '--date', '1 Year Ago', '--utc']).strip()),
                "projects": [
                  "PHID-PROJ-4uc7r7pdosfsk55qg7f6"  # Production errors
                ]
              },
              "attachments": {
                "projects": True
              }
        })


if __name__ == '__main__':
    p = Phab()
    groups = p.groups()
    tasks = p.tasks()
    PHIDs = Counter()

    for task in tasks:
        for phid in task['attachments']['projects']['projectPHIDs']:
            PHIDs[phid] += 1

    group_phids = Counter()
    groups_with_tasks = set(PHIDs.keys()) & set(groups)
    for group in groups_with_tasks:
        group_phids[group] = PHIDs[group]

    print('Team\tProduction Errors Past Year')
    for group in sorted(group_phids, key=group_phids.get, reverse=True):
        print('{}:\t{}'.format(groups[group], group_phids[group]))
