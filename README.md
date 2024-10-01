## NOTES:
1. looks like binance is not giving live data using that endpoint. 

🎉 First Working Version of Full Integration 🚀

This is the first version where everything works together, but there are some issues that need to be addressed:

1️⃣ **WebSocket Connection Handling**: I didn't create separate buses for each exchange, leading to shared WebSocket group IDs. This causes potential data loss across connections. Need to implement unique group IDs for each WebSocket connection.

2️⃣ **UI WebSocket Switching**: The UI is not properly switching the WebSocket connection when a different ticker is selected. Need to implement WebSocket disconnection when switching tickers.

3️⃣ **Golang API Improvements**: Need to add a disconnect implementation in the Go APIs to handle proper WebSocket closures.

4️⃣ **Kafka Consumer Optimization**: Currently, there's only one thread handling all exchange channels, which causes delays in ticket information transmission. Need to improve the Kafka consumer by either:
   - Creating more workers with separate threads, or
   - Splitting the Kafka bus to ensure only relevant data is read.

🕒 I'll evaluate these alternatives to find the best solution given the time constraints.

