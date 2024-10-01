from .websocket_price_abstract import WebSocketPriceTracker
import json

class CoinbasePriceTracker(WebSocketPriceTracker):
    def __init__(self, symbols):
        super().__init__("coinbase", symbols)

    def on_open(self, ws):
        self._logger.info(f"Connected to Coinbase WebSocket  | Thread [{self._thread_index}]")
        subscribe_message = {
            "type": "subscribe",
            "product_ids": [f"{symbol}-USD" for symbol in self.symbols],
            "channels": ["ticker"]
        }
        ws.send(json.dumps(subscribe_message))
        self._logger.info(f"Subscribed to {', '.join(self.symbols)} on Coinbase  | Thread [{self._thread_index}]")

    def process_message(self, data):
        if data['type'] == 'ticker':
            ticker = data["product_id"].split("-")[0]
            self._kafka_producer.send({
                "exchange":"coinbase",
                "ticker": ticker, 
                "best_bid_quantity": data["best_bid_size"],
                "best_bid_price": data["best_bid"],
                "last_price": data["price"],
                "best_offer_quantity": data["best_ask_size"],
                "best_offer_price": data["best_ask"],
            })
            self._logger.info(f"{ticker}: ${data['price']}  | Thread [{self._thread_index}]")

