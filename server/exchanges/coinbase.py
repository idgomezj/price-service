from .websocket_price_abstract import WebSocketPriceTracker
import json

class CoinbasePriceTracker(WebSocketPriceTracker):
    def __init__(self, symbols):
        super().__init__("COINBASE", symbols)

    def on_open(self, ws):
        self._logger.info("Connected to Coinbase WebSocket  | Thread [{self.thread_index}]")
        subscribe_message = {
            "type": "subscribe",
            "product_ids": [f"{symbol}-USD" for symbol in self.symbols],
            "channels": ["ticker"]
        }
        ws.send(json.dumps(subscribe_message))
        self._logger.info(f"Subscribed to {', '.join(self.symbols)} on Coinbase  | Thread [{self.thread_index}]")

    def process_message(self, data):
        if data['type'] == 'ticker':
            self._logger.info(f"{data['product_id']}: ${data['price']}  | Thread [{self.thread_index}]")
