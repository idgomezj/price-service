from .websocket_price_abstract import WebSocketPriceTracker
import json

class DeribitPriceTracker(WebSocketPriceTracker):
    def __init__(self, symbols):
        super().__init__("DERIBIT", symbols)

    def on_open(self, ws):
        self._logger.info("Connected to Deribit WebSocket")
        for symbol in self.symbols:
            subscribe_message = {
                    "jsonrpc" : "2.0",
                    "id" : 8106,
                    "method" : "public/ticker",
                    "params" : {
                        "instrument_name" : "BTC-PERPETUAL"
                    }
                    }
            # subscribe_message = {
            #         "method" : "public/subscribe",
            #         "params" : {
            #             "channels":["ticker.BTC-PERPETUAL.raw"]
            #         }
            #         }
            ws.send(json.dumps(subscribe_message))
        self._logger.info(f"Subscribed to {', '.join(self.symbols)} on Deribit")

    def process_message(self, data):
        print(data)
        if 'params' in data and 'data' in data['params']:
            ticker_data = data['params']['data']
            self._logger.info(f"Deribit - {ticker_data['instrument_name']}: ${ticker_data['last_price']}")

