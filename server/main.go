package main

import (
	"log"
	"net/http"

	"github.com/klauspost/compress/gzhttp"
	"github.com/niftyers/niftyers-syslabmgr/lib/handlers"
)



func main() {
	spaHandler := handlers.NewSPAHandler("./web") 
	apiHandler := handlers.NewAPIHandler()

	handler := http.StripPrefix("/", spaHandler)
	wrappedHandler := gzhttp.GzipHandler(handler)

	http.Handle("/", wrappedHandler)
	http.Handle("/api/", handlers.APIMiddleware(apiHandler))

	log.Println("Server running on :9101")
	log.Fatal(http.ListenAndServe(":9101", nil))
}