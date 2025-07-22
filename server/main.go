package main

import (
	"embed"
	"log"
	"net/http"

	"github.com/klauspost/compress/gzhttp"
	"github.com/niftyers/niftyers-syslabmgr/lib/handlers"
)

var embeddedFiles embed.FS

func main() {
	spaHandler := handlers.NewSPAHandler(embeddedFiles)
	apiHandler := handlers.NewAPIHandler()

	handler := http.StripPrefix("/", spaHandler)
	wrappedHandler := gzhttp.GzipHandler(handler)

	http.Handle("/", wrappedHandler)
	http.Handle("/api/", handlers.APIMiddleware(apiHandler))

	log.Println("Server running on :9101")
	log.Fatal(http.ListenAndServe(":9101", nil))
}