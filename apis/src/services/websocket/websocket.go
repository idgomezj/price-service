package websocket

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/websocket"
)

// WebSocketUpgrader is used to upgrade HTTP connections to WebSocket connections
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type CryptoData struct {
	BestBid      float64 `json:"bestBid"`
	LastPrice    float64 `json:"lastPrice"`
	BestOffer    float64 `json:"bestOffer"`
	BidQuantity  float64 `json:"bidQuantity"`
	OfferQuantity float64 `json:"offerQuantity"`
}


func HandleWebSocket(w http.ResponseWriter, r *http.Request) {
	// Upgrade the HTTP request to a WebSocket connection
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Failed to upgrade:", err)
		return
	}
	defer ws.Close()


	venue := r.URL.Path[len("/ws/"):]
	fmt.Printf("Client connected to venue: %s\n", venue)

	// Simulate sending crypto price data every second
	ticker := time.NewTicker(1 * time.Second)
	defer ticker.Stop()

	for {
		select {
			case <-ticker.C:
				// Generate mock data for the crypto asset
				data := CryptoData{
					BestBid:      50000.12 + float64(time.Now().UnixNano()%1000)/100,
					LastPrice:    50500.67 + float64(time.Now().UnixNano()%1000)/100,
					BestOffer:    51000.89 + float64(time.Now().UnixNano()%1000)/100,
					BidQuantity:  1.23 + float64(time.Now().UnixNano()%100)/100,
					OfferQuantity: 2.34 + float64(time.Now().UnixNano()%100)/100,
				}

				// Send the mock data as JSON
				message, err := json.Marshal(data)
				if err != nil {
					log.Println("Error marshalling JSON:", err)
					continue
				}
				if err := ws.WriteMessage(websocket.TextMessage, message); err != nil {
					log.Println("Error writing message:", err)
					return
				}
		}
	}
}
