package config

import (
	"strings"
	"log"
	"os"

	"github.com/joho/godotenv"
)


var (
	KafkaBroker string
	Exchanges   []string
)

func init() {
	
	err := godotenv.Load()
	if err != nil {
		log.Println("Error loading .env file, continuing with system environment variables")
	}


	KafkaBroker = os.Getenv("KAFKA_BROKER")
	if KafkaBroker == "" {
		KafkaBroker = "kafka:9092"
	}

	exchangesEnv := os.Getenv("VITE_EXCHANGES")
	if exchangesEnv != "" {
		Exchanges = strings.Split(exchangesEnv, ",")
	} else {
		Exchanges = []string{"binance", "okx", "coinbase"}
	}

	// Convert all exchange names to lowercase
	for i, exchange := range Exchanges {
		Exchanges[i] = strings.ToLower(exchange)
	}
}
