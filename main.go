package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"regexp"
)

type Redirect struct {
	Cname string
	Path string
}

var (
	redirects []Redirect
)

func matchCname(h string) (string, error) {
	for _, redirect := range redirects {
		matched, err := regexp.Match(redirect.Cname, []byte(h))
		if err != nil {
			return "", err
		}

		if matched && redirect.Path != "" {
			return redirect.Path, nil
		}
	}
	return "", errors.New("nope")

}

func handleRedirect(w http.ResponseWriter, r *http.Request) {
	redirect, err := matchCname(r.Host)
	if err != nil {
		fmt.Fprintf(w, "No redirect found :(")
		return
	}
	http.Redirect(w, r, redirect, 301)
}

func setupRedirects() {
	data, err := ioutil.ReadFile("redirect.json")
	if err != nil {
		fmt.Println("error:", err)
		os.Exit(1)
	}
	err = json.Unmarshal(data, &redirects)
	if err != nil {
		fmt.Println("error:", err)
		os.Exit(1)
	}
}

func main() {
	setupRedirects()

	http.HandleFunc("/", handleRedirect)
	fmt.Println("Listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
