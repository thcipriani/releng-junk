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
      1.35.0-wmf.18   16:14:37:19
      1.35.0-wmf.19   20:3:12:19
      1.35.0-wmf.20   12:23:31:25
      1.35.0-wmf.21   15:9:21:31
      1.35.0-wmf.22   12:14:32:7
      1.35.0-wmf.23   11:20:13:52
      1.35.0-wmf.24   12:11:3:32
      1.35.0-wmf.25   10:2:25:31
      Average for p95: 14:0:22:12

## How it works

* Point to a local and up-to-date `mediawiki/core` checkout via the `-C` flag.
* Find the branch point for each specified version
    * This is approximately the same thing as train deploy time. That is, the
      commit time happens, at most, a few hours before actual deployment
* Get the p95 of the difference between commit time of each patch in the
  branch, and the train branch point
* Reports an average of the p95 at the end.
* It also expects all extensions listed in `REPO_LIST` to be under the core
  path (TODO: read from `.gitmodules` for each branch.
