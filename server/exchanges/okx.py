from .websocket_price_abstract import WebSocketPriceTracker
import json


class OKXPriceTracker(WebSocketPriceTracker):
    def __init__(self, symbols):
        super().__init__("OKX", symbols)

    def on_open(self, ws):
        self._logger.info("Connected to OKX WebSocket")
        subscribe_message = {
            "op": "subscribe",
            "args": [{"channel": "tickers", "instId": f"{symbol}-USDT"} for symbol in self.symbols]
        }
        ws.send(json.dumps(subscribe_message))
        self._logger.info(f"Subscribed to {', '.join(self.symbols)} on OKX  | Thread [{self.thread_index}]")

    def process_message(self, data):
        if 'data' in data and len(data['data']) > 0:
            ticker_data = data['data'][0]
            self._logger.info(f"OKX - {ticker_data['instId']}: ${ticker_data['last']}  | Thread [{self.thread_index}]")
