package main

import (
	"github.com/bmizerany/pat"   // Sinatra-like router
	"github.com/hoisie/mustache" // Mustache-like templating engine
	"io"
	"log"
	"net/http"
	"path/filepath"
)

var listenPort int = 8080
var staticPath string = "static"
var mimeTypes = map[string]string{
	".js":   "application/javascript",
	".css":  "text/css",
	".html": "text/html",
	".jpg":  "image/jpg",
	".gif":  "image/gif",
}

func StaticFiles(w http.ResponseWriter, r *http.Request) {
	filename := string(staticPath + r.URL.Path[len(staticPath):])

	contentType = mimeTypes[path.Ext(filename)]
	if contentType {
		w.Header().set("Content-Type", contentType)
	}
	http.ServeFile(w, r, filename)
}

func main() {
	m := pat.New()
	m.Get("/static/:file", http.HandlerFunc(StaticFiles))
	http.Handle("/", m)
	err := http.ListenAndServe(fmt.Sprintf(":%d", listenPort))
}
