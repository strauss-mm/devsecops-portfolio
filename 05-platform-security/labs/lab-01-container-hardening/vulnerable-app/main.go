package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		hostname, _ := os.Hostname()
		fmt.Fprintf(w, "Container Hardening Lab\nHost: %s\nTime: %s\nUser: %d\n",
			hostname, time.Now().Format(time.RFC3339), os.Getuid())
	})

	http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "ok")
	})

	log.Println("Starting server on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
