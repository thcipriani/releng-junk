#!/usr/bin/env python3

import argparse
import os
import re

import requests

from bs4 import BeautifulSoup

BASE_URL = 'https://www.mediawiki.org/wiki/'
FMT_URL = 'MediaWiki_{}/Changelog'

ap = argparse.ArgumentParser()
ap.add_argument(
    '-w',
    '--wmf-version',
    dest='versions',
    action='append',
    required=True,
    help='wmf version'
)
args = ap.parse_args()

for version in args.versions:
    # Get the url for 1.35.0-wmf.10
    major, minor = version.split('-')
    major = '.'.join(major.split('.')[:-1])
    url_version = os.path.join(major, minor)
    url = os.path.join(BASE_URL, FMT_URL.format(url_version))

    r = requests.get(url)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, 'html.parser')

    links = soup.find_all('a', href=True)

    count = 0
    for link in links:
        if not link['href'].startswith('https://gerrit.wikimedia.org/r/'):
            continue
        count += 1
    print('{}\t{}'.format(version, count))
