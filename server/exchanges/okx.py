from .websocket_price_abstract import WebSocketPriceTracker
import json


class OKXPriceTracker(WebSocketPriceTracker):
    def __init__(self, symbols):
        super().__init__("okx", symbols)

    def on_open(self, ws):
        self._logger.info(f"Connected to OKX WebSocket | Thread [{self._thread_index}]")
        subscribe_message = {
            "op": "subscribe",
            "args": [{"channel": "tickers", "instId": f"{symbol}-USDT"} for symbol in self.symbols]
        }
        ws.send(json.dumps(subscribe_message))
        self._logger.info(f"Subscribed to {', '.join(self.symbols)} on OKX  | Thread [{self._thread_index}]")

    def process_message(self, data):
        if 'data' in data and len(data['data']) > 0:
            ticker_data = data['data'][0]
            ticker = ticker_data['instId'].split("-")[0]
            self._kafka_producer.send( {
                "exchange":"okx",
                "ticker": ticker,
                "best_bid_quantity": ticker_data["bidSz"],
                "best_bid_price": ticker_data["bidPx"],
                "last_price": ticker_data["last"],
                "best_offer_quantity": ticker_data["askSz"],
                "best_offer_price": ticker_data["askPx"],
            })
            self._logger.info(f"OKX - {ticker}: ${ticker_data['last']}  | Thread [{self._thread_index}]")

