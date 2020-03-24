#!/usr/bin/env python3

import re

import requests

from bs4 import BeautifulSoup

BASE_URL = 'https://wikitech.wikimedia.org'
URL = BASE_URL + '/wiki/Incident_documentation' # | grep -P '<a.*20190[789]\d\d-'

TIME_REGEX = r'.*20200[123]\d\d.*'

r = requests.get(URL)
r.raise_for_status()

soup = BeautifulSoup(r.text, 'html.parser')

links = soup.find_all('a')

scap_incidents = 0

for link in links:
    if re.match(TIME_REGEX, str(link)):
        r = requests.get(BASE_URL + link['href'])
        r.raise_for_status()

        incident_soup = BeautifulSoup(r.text, 'html.parser')
        x = incident_soup.find('span', id='Actionables')
        for item in (x.parent.next_siblings):
            if 'scap' in str(item).lower():
                print('Found one! {}'.format(item))
                scap_incidents += 1

print('------------------------')
print('Scap incidents: {}'.format(scap_incidents))
