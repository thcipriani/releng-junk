#!/usr/bin/env python3

import json

with open('yaks.json') as f:
    tasks = json.load(f)

for task in tasks:
    phid = 'T{}'.format(task['id'])
    row = [
        phid,
        f'https://phabricator.wikimedia.org/{phid}',
        task['fields']['name'],
    ]
    print(','.join(row))
