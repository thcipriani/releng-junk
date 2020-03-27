# Cycle Time

> The time from deciding that you need to make a change to having it in
> production is known as the _cycle time_.
>
> -- _Continuous Delivery_ by Jez Humble and David Farley

This is an attempt to approximate that number by looking at the branch point
for a particular deployment and comparing the commit time of that branch point
to the commit time for the patches between that branch point and the previous
branch point.

## Example

	$ python3 core-cycle-time.py -C /srv/projects/wikimedia/mediawiki-core \
		-w 1.35.0-wmf.15 \
        -w 1.35.0-wmf.16,1.35.0-wmf.18 \
        -w 1.35.0-wmf.19 \
        -w 1.35.0-wmf.20 \
        -w 1.35.0-wmf.21 \
        -w 1.35.0-wmf.22 \
        -w 1.35.0-wmf.23 \
        -w 1.35.0-wmf.24 \
        -w 1.35.0-wmf.25
	1.35.0-wmf.15 - 7:21:6:29
	1.35.0-wmf.18 - 18:3:40:25
	1.35.0-wmf.19 - 13:6:16:14
	1.35.0-wmf.20 - 25:23:13:36
	1.35.0-wmf.21 - 11:13:4:49
	1.35.0-wmf.22 - 7:23:7:34
	1.35.0-wmf.23 - 19:18:39:22
	1.35.0-wmf.24 - 10:18:9:27
	1.35.0-wmf.25 - 9:17:56:52
	Average p95: 17:8:8:18


## How it works

* Point to a local and up-to-date `mediawiki/core` checkout via the `-C` flag.
* Find the branch point for each specified version
    * This is approximately the same thing as train deploy time. That is, the
      commit time happens, at most, a few hours before actual deployment
* Get the p95 of the difference between commit time of each patch in the
  branch, and the train branch point
* Reports an average of the p95 at the end.
