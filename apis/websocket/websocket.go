package websocket

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"sync"

	"github.com/gorilla/websocket"
	"apis/kafka"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type CryptoData struct {
	Exchange          string  `json:"exchange"`
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
	wg := &sync.WaitGroup{}
	messageChannel := make(chan []byte)
	ctx, cancel := context.WithCancel(context.Background()) 

	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Failed to upgrade:", err)
		cancel()
	}
	defer func() {
		cancel() // Ensure Kafka is stopped when the WebSocket is closed
		ws.Close()
	}()

	venue := r.URL.Path[len("/ws/"):]

	splitStr := strings.Split(venue, "/")
	exchange := splitStr[0]
	ticker := strings.ToUpper(splitStr[1])

	// Start the Kafka consumer in a goroutine
	wg.Add(1)
	go func() {
		defer wg.Done()
		kafka.Run(
			ctx, 
			cancel, 
			messageChannel, 
			exchange,
			fmt.Sprintf("%v_%v",exchange, ticker),
		) 
	}()

	
	wg.Add(1)
	go func() {
		defer wg.Done()
		for {
			select {
			case dataBytes := <-messageChannel:
				data, err := transformCryptoData(dataBytes)
				if err != nil {
					fmt.Println("Error:", err)
					return
				}

				if data.Ticker != ticker {
					fmt.Println("Data does not match ticker")
					continue
				}

				message, err := json.Marshal(data)
				if err != nil {
					log.Println("Error marshalling JSON:", err)
					continue
				}

				// Send data over WebSocket
				if err := ws.WriteMessage(websocket.TextMessage, message); err != nil {
					log.Println("Error writing message:", err)
					return
				}
			case <-ctx.Done(): // Stop processing when context is canceled
				return
			}
		}
	}()

	// Detect WebSocket close
	for {
		_, _, err := ws.ReadMessage()
		if err != nil {
			log.Println("WebSocket closed:", err)
			cancel() // Cancel the Kafka process when WebSocket is closed
			break
		}
	}

	// Wait for both goroutines to finish
	wg.Wait()
}
