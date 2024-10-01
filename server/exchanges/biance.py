from .websocket_price_abstract import WebSocketPriceTracker
import json

class BinancePriceTracker(WebSocketPriceTracker):
    def __init__(self, symbols):
        super().__init__(
            "BIANCE", 
            [symbol.lower() + "usdt@ticker" for symbol in symbols]
        )


    def on_open(self, ws):
        self._logger.info("Connected to Binance WebSocket")
        print("Ivan Ivan"*100)
        print(self.symbols)
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": self.symbols,
            "id": 1
        }
        ws.send(json.dumps(subscribe_message))
        self._logger.info(f"Subscribed to {', '.join(self.symbols)}")

    def process_message(self, data):
        print(data)