package main

import (
	"fmt"
	"github.com/bmizerany/pat" // Sinatra-like router
	//"github.com/hoisie/mustache"  Mustache-like templating engine
	"log"
	"net/http"
)

var listenPort int = 8080
var staticPath string = "/static/"

func Api(w http.ResponseWriter, r *http.Request) {
}

func main() {
	m := pat.New()
	m.Get("/api/:id", http.HandlerFunc(Api))
	http.Handle("/", m)
    http.Handle(staticPath, http.StripPrefix(staticPath, http.FileServer(http.Dir("." + staticPath))))
	err := http.ListenAndServe(fmt.Sprintf(":%d", listenPort), nil)
	if err != nil {
		log.Fatal(err)
	}
}
