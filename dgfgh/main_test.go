package main

import (
	"testing"
)

func TestGithubUrl(t *testing.T) {
	url := githubRepo("foo")
	if url != "https://github.com/wikimedia/foo" {
		t.Errorf("Github url is incorrect: %s", url)
	}
}

func TestGerritReplica(t *testing.T) {
	url := gerritReplicaRepo("foo")
	if url != "https://gerrit-replica.wikimedia.org/r/foo" {
		t.Errorf("Gerrit url is incorrect: %s", url)
	}
}

func TestGithubRepoName(t *testing.T) {
	url := githubRepoName("Foo/Bar")
	if url != "Foo-Bar" {
		t.Errorf("github repo is incorrect: %s", url)
	}
}

func TestRepoExists(t *testing.T) {
	if repoExists("Nope") {
		t.Errorf("github repo shouldn't exist: Nope")
	}
}
