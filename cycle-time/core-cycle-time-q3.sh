#!/usr/bin/env bash
# I found all this stuff by looking at the SAL and at gerrit
# There's got to be a way to automate this
python3 cycletime.py 'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.35.0-wmf.11..0ef0443?no-merges&format=JSON' '2020-01-09T20:06:00+00:00'
python3 cycletime.py 'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.35.0-wmf.10..c4ef4c4?no-merges&format=JSON' '2019-12-19T13:02:00+00:00'
python3 cycletime.py 'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.35.0-wmf.8..67432d0?no-merges&format=JSON' '2019-12-12T20:18:00+00:00'
python3 cycletime.py 'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.35.0-wmf.5..f20930f?no-merges&format=JSON' '2019-12-090T23:00:00+00:00'
python3 cycletime.py 'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.35.0-wmf.4..dfc5e704?no-merges&format=JSON' '2019-11-07T20:42:00+00:00'
python3 cycletime.py 'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.35.0-wmf.3..986eea6?no-merges&format=JSON' '2019-11-04T19:08:00+00:00'
python3 cycletime.py 'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.35.0-wmf.2..1ed75b4?no-merges&format=JSON' '2019-10-24T13:06:00+00:00'
python3 cycletime.py 'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.35.0-wmf.1..0a20cae?no-merges&format=JSON' '2019-10-17T19:00:00+00:00'
python3 cycletime.py 'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.34.0-wmf.25..64f5c4c?no-merges&format=JSON' '2019-10-10T19:20:00+00:00'
python3 cycletime.py 'https://gerrit.wikimedia.org/g/mediawiki/core/+log/wmf/1.34.0-wmf.24..417b023?no-merges&formt=JSON' '2019-10-03T19:21:00+00:00'
