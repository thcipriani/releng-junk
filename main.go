package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

type Relenger struct {
	Name string
	Irc string
	Timezone string
}

var (
	relengers []Relenger
)

func handleHttp(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "hi")
}

func setupRelengers() {
	data, err := ioutil.ReadFile("team.json")
	if err != nil {
		fmt.Println("error:", err)
		os.Exit(1)
	}
	err = json.Unmarshal(data, &relengers)
	if err != nil {
		fmt.Println("error:", err)
		os.Exit(1)
	}
}

func main() {
	setupRelengers()

	http.HandleFunc("/", handleHttp)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
