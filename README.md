# Price Service

## Overview

This project implements a real-time cryptocurrency price service that fetches data from multiple exchanges (Coinbase, Binance, Deribit, and OKX), publishes it to a Kafka message bus, and exposes it via a WebSocket API for consumption by a UI client.

#### Important Note: Please wait a few seconds for the UI to load and become ready.

## Architecture

The system consists of the following components:

1. **Python Server**: Connects to exchange WebSockets and publishes data to Kafka.
2. **Kafka Message Bus**: Single-node setup for message queuing.
3. **Golang API**: Consumes Kafka messages and exposes data via WebSocket.
4. **React UI**: Displays real-time price data (not fully implemented).

## Components

### Python Server

- Connects to WebSocket APIs of Coinbase, Binance, Deribit, and OKX.
- Retrieves real-time price data for specified tickers/symbols.
- Publishes data to Kafka topics (one topic per exchange).

### Kafka Message Bus

- Single-node setup.
- Four topics, one for each exchange.
- Accessible via UI on port 8088 for monitoring topics, messages, and consumers.

### Golang API

- Consumes messages from Kafka topics.
- Exposes data via WebSocket for UI consumption.

### React UI (Partially Implemented)

- Connects to Golang API via WebSocket.
- Displays real-time price data.

## Implementation Details

- The project extends beyond the original Coinbase-only requirement to include multiple exchanges.
- A single Kafka topic is used per exchange, rather than per ticker, for initial simplicity.
- The Golang API currently reads all tickers, which may cause delays with large ticker lists.

## Future Improvements

1. Optimize Kafka topic structure:
   - Consider creating separate topics per ticker for more efficient data handling.
2. Enhance Golang API performance:
   - Implement worker pool to process messages in parallel.
   - Evaluate race condition risks in parallel processing.

# Price Service

## Setup and Running

There are two ways to set up and run the project:

### Option 1: Using Docker Compose (Recommended)

To run the entire project, including all services and Kafka, use:

```
docker-compose up
```

This will start all components of the system in one go.

### Option 2: Running Components Individually

If you prefer to run components separately for development or debugging purposes, follow these steps:

1. **Start Kafka:**
   You'll need to run Docker Compose to build and start Kafka:
   ```
   docker-compose up kafka
   ```

2. **Run the Python Server:**
   Navigate to the Python server directory and run:
   ```
   python3 main.py
   ```

3. **Run the Golang API:**
   Navigate to the Golang API directory and run:
   ```
   go run .
   ```

4. **Run the React UI:**
   Navigate to the React UI directory and run:
   ```
   npm run dev
   ```

Note: When running components individually, make sure you're in the correct terminal/directory for each service.



## Monitoring

- Kafka UI is available on port 8088 for monitoring topics, messages, and consumers.

## Known Limitations

- The current implementation may experience delays when processing large numbers of tickers.
- The single-node Kafka setup may limit scalability for high-volume scenarios.
- Based on what I can read and evaluate, Deribit's API has certain limitations compared to other exchanges.  To access more frequent updates or to subscribe to multiple instruments, you may need to use authenticated endpoints or consider a paid API tier

## Conclusion

This Price Service project provides a flexible foundation for real-time cryptocurrency price tracking across multiple exchanges. While meeting the core requirements, it also offers opportunities for further optimization and scaling to handle larger datasets and higher throughput scenarios.