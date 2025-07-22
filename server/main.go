package main

import (
	"embed"
	"log"
	"net/http"
)

var staticFiles embed.FS

func main() {
	http.HandleFunc("/api/hello", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"message": "Hello from Go!"}`))
	})

	http.Handle("/", http.FileServer(http.FS(staticFiles)))

	log.Println("Server running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}