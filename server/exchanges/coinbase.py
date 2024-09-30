import websockets
import logging
import asyncio
import json


class CoinbasePriceTracker:
    def __init__(self, symbols):
        self.ws_url = "wss://ws-feed.exchange.coinbase.com"
        self.symbols = symbols
        self._logger = logging.getLogger(__name__)

    async def connect(self):
        while True:
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    self._logger.info("Connected to Coinbase WebSocket")
                    await self.subscribe(websocket)
                    await self.receive_messages(websocket)
            except websockets.exceptions.ConnectionClosed as e:
                self._logger.error(f"Coinbase WebSocket connection closed: {e}")
                await asyncio.sleep(5)
            except Exception as e:
                self._logger.error(f"An error occurred: {e}")
                await asyncio.sleep(5)

    async def subscribe(self, websocket):
        subscribe_message = {
            "type": "subscribe",
            "product_ids": [f"{symbol}-USD" for symbol in self.symbols],
            "channels": ["ticker"]
        }
        await websocket.send(json.dumps(subscribe_message))
        self._logger.info(f"Subscribed to {', '.join(self.symbols)} on Coinbase")

    async def receive_messages(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                if data['type'] == 'ticker':
                    self._logger.info(f"Coinbase - {data['product_id']}: ${data['price']}")
            except json.JSONDecodeError as e:
                self._logger.error(f"Failed to decode Coinbase message: {e}")
            except KeyError as e:
                self._logger.error(f"Unexpected Coinbase message format: {e}")
            except Exception as e:
                self._logger.error(f"Error processing Coinbase message: {e}")
                break
