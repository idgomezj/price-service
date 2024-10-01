from .websocket_price_abstract import WebSocketPriceTracker
import json

class DeribitPriceTracker(WebSocketPriceTracker):
    def __init__(self, symbols):
        super().__init__("DERIBIT", symbols)

    def on_open(self, ws):
        self._logger.info(f"Connected to Deribit WebSocket | Thread [{self._thread_index}]")
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
        self._logger.info(f"Subscribed to {', '.join(self.symbols)} on Deribit | Thread [{self._thread_index}]")

    def process_message(self, data):
        ticker_data = data['result']
        ticker = ticker_data['instrument_name'].split("-")[0]
        self._kafka_producer.send( {
            "ticker": ticker,
            "best_bid_quantity": ticker_data["best_bid_amount"],
            "best_bid_price": ticker_data["best_bid_price"],
            "last_price": ticker_data["last_price"],
            "best_offer_quantity": ticker_data["best_ask_amount"],
            "best_offer_price": ticker_data["best_ask_price"],
        })
        self._logger.info(f"DERIBIT - {ticker}: ${ticker_data['last_price']}  | Thread [{self._thread_index}]")

