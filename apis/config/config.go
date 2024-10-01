package config

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)


var KafkaBroker string

func init() {
	
	err := godotenv.Load()
	if err != nil {
		log.Println("Error loading .env file, continuing with system environment variables")
	}


	KafkaBroker = os.Getenv("KAFKA_BROKER")
	if KafkaBroker == "" {
		KafkaBroker = "kafka:9092"
	}
}
