from kafka_producer import KafkaProducer
from config import config
import websocket
import threading
import logging
import abc
import json
import time

class WebSocketPriceTracker(abc.ABC):
    
    def __init__(self, base_url, symbols):
        self.ws_url = config.get(f"{base_url}_URL")
        self.symbols = symbols
        self.ws = None
        self._thread_index = None
        self.should_reconnect = True
        self._logger = logging.getLogger(self.__class__.__name__)
        self._kafka_producer = KafkaProducer(config, base_url)

    @abc.abstractmethod
    def on_open(self, ws):
        """Abstract method for sending subscription messages when the WebSocket opens."""
        pass

    def on_message(self, ws, message):
        """Handles incoming messages."""
        try:
            data = json.loads(message)
            self.process_message(data)
        except json.JSONDecodeError as e:
            self._logger.error(f"Failed to decode message  | Thread [{self._thread_index}]: {e}")
        except KeyError as e:
            self._logger.error(f"Unexpected message format  | Thread [{self._thread_index}]: {e}")
        except Exception as e:
            self._logger.error(f"Error processing message  | Thread [{self._thread_index}]: {e}")

    @abc.abstractmethod
    def process_message(self, data):
        """Abstract method to process messages. Each tracker should implement how to handle messages."""
        pass

    def on_error(self, ws, error):
        self._logger.error(f"WebSocket error   Thread [{self._thread_index}]: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        self._logger.info("WebSocket connection closed")
        if self.should_reconnect:
            self._logger.info(f"Reconnecting in 5 seconds... | Thread [{self._thread_index}]")
            time.sleep(5)
            self.connect()

    def connect(self):
        self.ws = websocket.WebSocketApp(
                                            self.ws_url,
                                            on_message=self.on_message,
                                            on_error=self.on_error,
                                            on_close=self.on_close,
                                            on_open=self.on_open
                                        )
        self.ws.run_forever()

    def run_in_thread(self, thread_index: int):
        """Run the WebSocket connection in a separate thread."""
        self._thread_index = thread_index
        self._kafka_producer.set_thread(thread_index)
        ws_thread = threading.Thread(target=self.connect)
        ws_thread.daemon = True  # Allow thread to exit when the main program exits
        ws_thread.start()
        return ws_thread
