import websockets
import asyncio
import logging
import json

class BinancePriceTracker:
    def __init__(self, symbols):
        self.ws_url = "wss://stream.binance.com:9443/ws"
        self.symbols = [symbol.lower() + "usdt@ticker" for symbol in symbols]
        self._logger = logging.getLogger(__name__)

    async def connect(self):
        while True:
            try:
                async with websockets.connect(f"{self.ws_url}/{'/'.join(self.symbols)}") as websocket:
                    self._logger.info("Connected to Binance WebSocket")
                    await self.receive_messages(websocket)
            except websockets.exceptions.ConnectionClosed as e:
                self._logger.error(f"Binance WebSocket connection closed: {e}")
                await asyncio.sleep(5)
            except Exception as e:
                self._logger.error(f"An error occurred: {e}")
                await asyncio.sleep(5)

    async def receive_messages(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                self._logger.info(f"Binance - {data['s']}: ${data['c']}")
            except json.JSONDecodeError as e:
                self._logger.error(f"Failed to decode Binance message: {e}")
            except KeyError as e:
                self._logger.error(f"Unexpected Binance message format: {e}")
            except Exception as e:
                self._logger.error(f"Error processing Binance message: {e}")
                break
