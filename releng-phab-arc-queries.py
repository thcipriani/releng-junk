import argparse
import json
from datetime import datetime
from dateutil import parser


def epoch(start_date):
    base = start_date

    if not isinstance(start_date, datetime):
        base = parser.parse(start_date)

    weekday = base.weekday()
    if weekday != 0:
        raise RuntimeError('not a monday!')
    return base.strftime('%s')


def get_relengers():
    with open('team.json') as f:
        team = json.load(f)
    return [str(t['phab']) for t in team]


def get_phids():
    with open('team.json') as f:
        team = json.load(f)
    return [str(t['phid']) for t in team]


def closed_week(users, last_monday):
    return json.dumps({
        "constraints": {
            "assigned": users,
            "closedStart": last_monday
        }
    })


def filed_week(users, last_monday):
    return json.dumps({
        "constraints": {
            "authorPHIDs": users,
            "createdStart": last_monday
        }
    })


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('date')
    ap.add_argument('--closed', action='store_true')
    ap.add_argument('--filed', action='store_true')
    return ap.parse_args()

def main():
    args = parse_args()
    last_monday = int(epoch(args.date))
    if args.closed:
        print(closed_week(get_relengers(), last_monday))
    if args.filed:
        print(filed_week(get_phids(), last_monday))


if __name__ == '__main__':
    main()
