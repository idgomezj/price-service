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
	"apis/config"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type CryptoData struct {
	Exchange          string `json:"exchange"`
	Ticker            string `json:"ticker"`
	BestBidQuantity   string `json:"best_bid_quantity"`
	BestBidPrice      string `json:"best_bid_price"`
	LastPrice         string `json:"last_price"`
	BestOfferQuantity string `json:"best_offer_quantity"`
	BestOfferPrice    string `json:"best_offer_price"`
}

type ChannelMap map[string]chan []byte

var (
	ExchangeChans = make(ChannelMap)
	cancel        context.CancelFunc
	ctx           context.Context
	wg            sync.WaitGroup
)

func init() {
	ctx, cancel = context.WithCancel(context.Background())

	fmt.Println("Init Websocket")
	fmt.Println("Creating kafka consumer for exchanges: ", config.Exchanges)

	// Create a channel for each exchange and store it in the map
	for _, exchange := range config.Exchanges {
		ExchangeChans[exchange] = make(chan []byte)

		wg.Add(1)
		go func(exchange string) {
			defer wg.Done()
			kafka.Run(
				ctx,
				cancel,
				ExchangeChans[exchange],
				exchange,
				exchange,
			)
		}(exchange)
	}
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
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Failed to upgrade:", err)
		return
	}
	defer ws.Close()

	venue := r.URL.Path[len("/ws/"):]
	splitStr := strings.Split(venue, "/")
	if len(splitStr) < 2 {
		log.Println("Invalid URL path")
		return
	}
	exchange := splitStr[0]
	ticker := strings.ToUpper(splitStr[1])

	ch, ok := ExchangeChans[exchange]
	if !ok {
		log.Printf("Exchange %s not found", exchange)
		return
	}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	wg.Add(1)
	go func() {
		defer wg.Done()
		for {
			select {
			case dataBytes := <-ch:
				data, err := transformCryptoData(dataBytes)
				if err != nil {
					log.Println("Error:", err)
					continue
				}

				if data.Ticker != ticker {
					continue
				}

				message, err := json.Marshal(data)
				if err != nil {
					log.Println("Error marshalling JSON:", err)
					continue
				}

				if err := ws.WriteMessage(websocket.TextMessage, message); err != nil {
					log.Println("Error writing message:", err)
					return
				}
			case <-ctx.Done():
				return
			}
		}
	}()

	// Detect WebSocket close
	for {
		_, _, err := ws.ReadMessage()
		if err != nil {
			log.Println("WebSocket closed:", err)
			break
		}
	}
}