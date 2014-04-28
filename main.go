package main

import (
	"fmt"
	"github.com/bmizerany/pat" // Sinatra-like router
    "github.com/fiorix/go-web/autogzip" // gzip support
	//"github.com/hoisie/mustache"  Mustache-like templating engine
	"log"
    "path"
	"net/http"
)

var listenPort int = 8080
var staticPath string = "static"

func Api(w http.ResponseWriter, r *http.Request) {
}

func main() {
	m := pat.New()
	m.Get("/api/:id", http.HandlerFunc(Api))
	http.Handle("/api", m)

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
