from .websocket_price_abstract import WebSocketPriceTracker
import json

class BinancePriceTracker(WebSocketPriceTracker):
    def __init__(self, symbols):
        super().__init__(
            "BIANCE", 
            [symbol.lower() + "usdt@ticker" for symbol in symbols]
        )


    def on_open(self, ws):
        self._logger.info(f"Connected to Binance WebSocket | Thread [{self._thread_index}]")
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": self.symbols,
            "id": 1
        }
        ws.send(json.dumps(subscribe_message))
        self._logger.info(f"Subscribed to {', '.join(self.symbols)} | Thread [{self._thread_index}]")

    def process_message(self, data):
        ticker = data["s"].split("USDT")[0]
        self._kafka_producer.send({
            "ticker": ticker,                 # Extracting ticker value
            "best_bid_quantity": data["Q"],       # Quantity of the last trade
            "best_bid_price": data["c"],          # Last traded price
            "last_price": data["c"],              # Closing price
            "best_offer_quantity": data["Q"],     # Same as last trade quantity in this case
            "best_offer_price": data["c"],        # Last traded price is used here for consistency
        })
        self._logger.info(f"{ticker}: ${data['c']}  | Thread [{self._thread_index}]")

