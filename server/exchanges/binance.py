from .websocket_price_abstract import WebSocketPriceTracker
import json

class BinancePriceTracker(WebSocketPriceTracker):
    def __init__(self):
        super().__init__("binance")


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
            "exchange":"binance",
            "ticker": ticker,                 
            "best_bid_quantity": data["B"],      
            "best_bid_price": data["b"],          
            "last_price": data["b"],       #FIXME This is not the last price. But, i will keep that value until I find how to get all together        
            "best_offer_quantity": data["A"],   
            "best_offer_price": data["a"],     
        })
        self._logger.info(f"{ticker}: ${data['b']}  | Thread [{self._thread_index}]")

