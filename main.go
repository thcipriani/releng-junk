package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

type Redirect struct {
	Cname string
	Redirect string
}

var (
	redirects []Redirect
)

func handleRedirect(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, redirects)
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
	log.Fatal(http.ListenAndServe(":8080", nil))
}
