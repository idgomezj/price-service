package main

import (
	"fmt"
	"log"
	"net/http"
	


	"apis/websocket"
	"apis/config"
)



func main() {


	fmt.Printf("Kafka Broker %v\n", config.KafkaBroker)


	http.HandleFunc("/ws/", func(w http.ResponseWriter, r *http.Request) {
		websocket.HandleWebSocket(w, r)
	})


	fmt.Println("WebSocket server started on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}