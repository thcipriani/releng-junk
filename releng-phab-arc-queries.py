#!/usr/bin/env python3

import argparse
import json
from datetime import datetime
from dateutil import parser


def epoch(date):
    """
    Get the epoch for a date
    """
    base = date

    if not isinstance(date, datetime):
        base = parser.parse(date)

    return base.strftime('%s')


def get_relengers():
    with open('team.json') as f:
        team = json.load(f)
    return [str(t['phab']) for t in team]


def get_phids():
    with open('team-private.json') as f:
        team = json.load(f)
    return [str(t['phid']) for t in team]


def closed_tasks(users, start_date, end_date):
    return json.dumps({
        "constraints": {
            "assigned": users,
            "closedStart": start_date,
            "closedEnd": end_date
        }
    })


def filed_tasks(users, start_date, end_date):
    return json.dumps({
        "constraints": {
            "authorPHIDs": users,
            "createdStart": start_date,
            "createdEnd": end_date,
        }
    })


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--closed', action='store_true')
    ap.add_argument('--filed', action='store_true')
    ap.add_argument('--start-date', help='Start date for phab', required=True)
    ap.add_argument('--end-date', help='End date for phab', required=True)
    return ap.parse_args()

def main():
    args = parse_args()
    start_date = int(epoch(args.start_date))
    end_date = int(epoch(args.end_date))
    if args.closed:
        print(closed_tasks(get_relengers(), start_date, end_date))
    if args.filed:
        print(filed_tasks(get_phids(), start_date, end_date))


if __name__ == '__main__':
    main()
