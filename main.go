package main

import (
	"fmt"
	eventsource "github.com/antage/eventsource/http"
	"github.com/bmizerany/pat"          // Sinatra-like router
	"github.com/fiorix/go-web/autogzip" // gzip support
	//"github.com/hoisie/mustache"  Mustache-like templating engine
	"log"
	"net/http"
	"path"
	"time"
    "strconv"
)

var listenPort int = 8080
var staticPath string = "static"

func Api(w http.ResponseWriter, r *http.Request) {
}

func Source(es eventsource.EventSource) {
	id := 1
	for {
		es.SendMessage("tick", "tick-event", strconv.Itoa(id))
		id++
		time.Sleep(5 * time.Second)
	}
}

func main() {

	es := eventsource.New(nil, nil)
	defer es.Close()

	http.Handle("/event", es)
	go Source(es)

	r := pat.New()
	r.Get("/api/:id", http.HandlerFunc(Api))
	http.Handle("/api", r)

	// Serve static files
	http.Handle("/static", autogzip.Handle(http.FileServer(http.Dir(staticPath))))

	// Serve site root
	http.HandleFunc("/", autogzip.HandleFunc(func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, path.Join(staticPath, "index.html"))
	}))

	err := http.ListenAndServe(fmt.Sprintf(":%d", listenPort), nil)
	if err != nil {
		log.Fatal(err)
	}
}
