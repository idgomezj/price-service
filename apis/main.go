package main

import (
	"fmt"
	"log"
	"net/http"

	"apis/src/services/websocket"

)




func main() {
	http.HandleFunc("/ws/", func(w http.ResponseWriter, r *http.Request) {
		websocket.HandleWebSocket(w, r)
	})

	fmt.Println("WebSocket server started on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
