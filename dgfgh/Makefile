dgfgh:
	go build

repos:
	curl -sL https://gerrit.wikimedia.org/r/projects/ | \
		tail -c +6 | \
		jq -r '.|to_entries| map(select(.value.state == "ACTIVE")) | .[].key' > repos
