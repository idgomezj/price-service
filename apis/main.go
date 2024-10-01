package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"

	"apis/websocket"
	"apis/kafka"

)



func main() {
	messageChannel := make(chan []byte)

	wg := &sync.WaitGroup{}
	wg.Add(1)
	go func() {
		defer wg.Done()
		kafka.Run(messageChannel)
	}()

	http.HandleFunc("/ws/", func(w http.ResponseWriter, r *http.Request) {
		websocket.HandleWebSocket(w, r, messageChannel)
	})

	

	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Println("WebSocket server started on :8080")
		log.Fatal(http.ListenAndServe(":8080", nil))
	}()

	// Wait for both goroutines to finish
	wg.Wait()
}