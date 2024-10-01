package websocket

import (
	"encoding/json"
	"fmt"
	"log"
	"sync"
	"strings"
	"net/http"


	"github.com/gorilla/websocket"
	"apis/kafka"
)

// WebSocketUpgrader is used to upgrade HTTP connections to WebSocket connections
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type CryptoData struct {
	Exchange 		  string  `json:"exchange"`
	Ticker            string  `json:"ticker"`
	BestBidQuantity   string  `json:"best_bid_quantity"`
	BestBidPrice      string  `json:"best_bid_price"`
	LastPrice         string  `json:"last_price"`
	BestOfferQuantity string  `json:"best_offer_quantity"`
	BestOfferPrice    string  `json:"best_offer_price"`
}


func transformCryptoData(data []byte) (*CryptoData, error) {
	var cryptoData CryptoData
	err := json.Unmarshal(data, &cryptoData)
	if err != nil {
		return nil, err
	}
	return &cryptoData, nil
}

func HandleWebSocket(w http.ResponseWriter, r *http.Request) {
	// Upgrade the HTTP request to a WebSocket connection
	wg := &sync.WaitGroup{}
	messageChannel := make(chan []byte)
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Failed to upgrade:", err)
		return
	}
	defer ws.Close()


	venue := r.URL.Path[len("/ws/"):]
	fmt.Printf("Client connected to venue: %s\n", venue)

	splitStr := strings.Split(venue, "/")

	exchange := splitStr[0]
    ticker := strings.ToUpper(splitStr[1])

	wg.Add(1)
	go func() {
		defer wg.Done()
		kafka.Run(messageChannel, exchange)
	}()

	wg.Add(1)
	go func() {
		defer wg.Done()
		for {
				data_bytes := <-messageChannel
				data, err := transformCryptoData(data_bytes)
				if err != nil {
					fmt.Println("Error:", err)
					return
				}
				fmt.Println(data)
				fmt.Println(exchange)
				fmt.Println(ticker)
				if  data.Ticker != ticker {
					fmt.Println("Data not match")
					continue
				}

				fmt.Println(data)
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
	}()

	// Wait for both goroutines to finish
	wg.Wait()
}
