import websockets
import asyncio
import logging
import json

class DeribitPriceTracker:
    def __init__(self, symbols):
        self.ws_url = "wss://www.deribit.com/ws/api/v2"
        self.symbols = symbols
        self._logger = logging.getLogger(__name__)

    async def connect(self):
        while True:
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    self._logger.info("Connected to Deribit WebSocket")
                    await self.subscribe(websocket)
                    await self.receive_messages(websocket)
            except websockets.exceptions.ConnectionClosed as e:
                self._logger.error(f"Deribit WebSocket connection closed: {e}")
                await asyncio.sleep(5)
            except Exception as e:
                self._logger.error(f"An error occurred: {e}")
                await asyncio.sleep(5)

    async def subscribe(self, websocket):
        for symbol in self.symbols:
            subscribe_message = {
                "jsonrpc": "2.0",
                "method": "public/subscribe",
                "params": {
                    "channels": [f"ticker.{symbol.lower()}_usd"]
                }
            }
            await websocket.send(json.dumps(subscribe_message))
        self._logger.info(f"Subscribed to {', '.join(self.symbols)} on Deribit")

    async def receive_messages(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                if 'params' in data and 'data' in data['params']:
                    ticker_data = data['params']['data']
                    self._logger.info(f"Deribit - {ticker_data['instrument_name']}: ${ticker_data['last_price']}")
            except json.JSONDecodeError as e:
                self._logger.error(f"Failed to decode Deribit message: {e}")
            except KeyError as e:
                self._logger.error(f"Unexpected Deribit message format: {e}")
            except Exception as e:
                self._logger.error(f"Error processing Deribit message: {e}")
                break
