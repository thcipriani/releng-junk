png/phabricator.png:
	./bin/plot log/2019/phab.csv Count Phabricator | gnuplot -p > png/phabricator.png

png/gerrit.png:
	./bin/plot log/2019/gerrit.csv Count Gerrit | gnuplot -p > png/gerrit.png
