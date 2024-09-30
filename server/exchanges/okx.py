import websockets
import asyncio
import logging
import json

class OKXPriceTracker:
    def __init__(self, symbols):
        self.ws_url = "wss://ws.okx.com:8443/ws/v5/public"
        self.symbols = symbols
        self._logger = logging.getLogger(__name__)

    async def connect(self):
        while True:
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    self._logger.info("Connected to OKX WebSocket")
                    await self.subscribe(websocket)
                    await self.receive_messages(websocket)
            except websockets.exceptions.ConnectionClosed as e:
                self._logger.error(f"OKX WebSocket connection closed: {e}")
                await asyncio.sleep(5)
            except Exception as e:
                self._logger.error(f"An error occurred: {e}")
                await asyncio.sleep(5)

    async def subscribe(self, websocket):
        subscribe_message = {
            "op": "subscribe",
            "args": [{"channel": "tickers", "instId": f"{symbol}-USDT"} for symbol in self.symbols]
        }
        await websocket.send(json.dumps(subscribe_message))
        self._logger.info(f"Subscribed to {', '.join(self.symbols)} on OKX")

    async def receive_messages(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                if 'data' in data and len(data['data']) > 0:
                    ticker_data = data['data'][0]
                    self._logger.info(f"OKX - {ticker_data['instId']}: ${ticker_data['last']}")
            except json.JSONDecodeError as e:
                self._logger.error(f"Failed to decode OKX message: {e}")
            except KeyError as e:
                self._logger.error(f"Unexpected OKX message format: {e}")
            except Exception as e:
                self._logger.error(f"Error processing OKX message: {e}")
                break