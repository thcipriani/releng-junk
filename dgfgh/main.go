// Download Gerrit from Github
// ===========================
//
// This is the lowest impact way I could think to download all of gerrit with notes.
//
// Copyright Tyler Cipriani 2020
// License: GPLv3+
package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"os/exec"
	"net/http"
	"net/url"
	"path"
	"sync"
	"strings"
)

var (
	githubUrl = "https://github.com/wikimedia"
	gerritUrl = "https://gerrit.wikimedia.org/r"
	gerritReplicaUrl = "https://gerrit-replica.wikimedia.org/r"
)

// Join a path to a url: harder than it should be...
func urlJoin(baseUrl string, repo string) string {
	u, err := url.Parse(baseUrl)
	if err != nil {
		log.Fatal(err)
	}
	u.Path = path.Join(u.Path, repo)
	return u.String()
}

// Check to see if a repo exists on a remote
func repoExists(repo string) bool {
	repoFullName := "https://api.github.com/repos/wikimedia/" + githubRepoName(repo)
	resp, err := http.Get(repoFullName)
	if err != nil {
		log.Fatal(err)
	}
	return resp.StatusCode == 200
}

// Utility function for generating a github repo uri
func githubRepo(repo string) string {
	return urlJoin(githubUrl, githubRepoName(repo))
}

// Utility function for generating a gerrit-replica repo uri
func gerritReplicaRepo(repo string) string {
	return urlJoin(gerritReplicaUrl, repo)
}

// Utility function for generating a github repo name
func githubRepoName(repo string) string {
	return strings.ReplaceAll(repo, "/", "-")
}

// Clone a repo
func cloneRepo(repo string) {
		repo = githubRepo(repo)
		out, err := exec.Command("git", "clone", repo).CombinedOutput()
		if err != nil {
			log.Fatal(fmt.Sprintf("%s\n%s\n%s", repo, out, err))
		}

		fmt.Printf("%s", out)
}

// Close repo notes
func cloneNotes(repo string) {
	out, _ := exec.Command("git", "-C", githubRepoName(repo), "fetch", gerritReplicaRepo(repo), "refs/notes/review:refs/notes/review").CombinedOutput()
	fmt.Printf("%s", out)
}

// Parse args -- path to repo file
func parseArgs() string {
    f := flag.String("repos", "repos", "file path to read repos from")
    flag.Parse()
	return *f
}

func main() {
    sem := make(chan struct{}, 12)
    f, err := os.Open(parseArgs())
    if err != nil {
        log.Fatal(err)
    }
    defer func() {
        if err = f.Close(); err != nil {
        log.Fatal(err)
    }
    }()

	var wg sync.WaitGroup
    s := bufio.NewScanner(f)

	// Read the repo file line-by-line
    for s.Scan() {
		// Add an item to the waitgroup
		wg.Add(1)
		sem <- struct{}{}

		// Clone repo async
		go func(repo string) {
		    defer func() { <-sem }()
		    defer wg.Done()

		    if repoExists(repo) {
			cloneRepo(repo)
			cloneNotes(repo)
		}
		}(s.Text())
    }
    err = s.Err()
    if err != nil {
        log.Fatal(err)
	}

	// Wait for all repos to be cloned
	wg.Wait()
}
