import websocket
import json
import threading
from typing import Callable, Any, Dict, List, TypeVar
from queue import Queue
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
T = TypeVar("T")

class WebSocketManager:
    """Generic WebSocket manager for handling subscriptions"""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.callbacks: Dict[int, Callable[[Any], None]] = {}  # Store callbacks by subscription ID
        self.subscription_ids: Dict[int, List[str]] = {}  # Track streams by subscription ID
        self.current_id = 0
        self.ws: websocket.WebSocketApp | None = None
        self.connect()

    def _get_next_id(self) -> int:
        self.current_id += 1
        return self.current_id

    def connect(self):
        def on_message(ws, message):
            data = json.loads(message)
            logger.debug(f"Received message: {data}")

            # Handle subscription confirmations
            if isinstance(data, dict) and "result" in data and "id" in data:
                logger.debug(f"Received subscription confirmation for ID {data['id']}")
                return

            # Route message to all active callbacks
            # This could be refined based on message content if needed
            for sub_id, callback in self.callbacks.items():
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in callback for subscription {sub_id}: {e}")

        def on_error(ws, error):
            logger.error(f"WebSocket error: {error}")

        def on_close(ws, close_status_code, close_msg):
            logger.info(f"WebSocket closed: {close_status_code} - {close_msg}")
            self.connect()

        def on_open(ws):
            logger.info(f"WebSocket connection opened to {self.endpoint}")
            # Resubscribe to all streams
            for sub_id, streams in self.subscription_ids.items():
                self.send_subscription(streams, sub_id)

        self.ws = websocket.WebSocketApp(
            self.endpoint,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open,
        )

        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def subscribe(self, streams: List[str], callback: Callable[[Any], None]) -> int:
        """
        Subscribe to streams and return the subscription ID
        """
        sub_id = self._get_next_id()
        self.subscription_ids[sub_id] = streams
        self.callbacks[sub_id] = callback

        self.send_subscription(streams, sub_id)
        logger.debug(f"Sent subscription request for streams: {streams} with ID: {sub_id}")
        return sub_id

    def send_subscription(self, streams: List[str], sub_id: int):
        subscribe_message = json.dumps(
            {"method": "SUBSCRIBE", "params": streams, "id": sub_id}
        )
        if self.ws:
            self.ws.send(subscribe_message)

    def unsubscribe(self, sub_id: int):
        if sub_id in self.subscription_ids:
            streams = self.subscription_ids[sub_id]
            unsubscribe_message = json.dumps(
                {"method": "UNSUBSCRIBE", "params": streams, "id": sub_id}
            )
            if self.ws:
                self.ws.send(unsubscribe_message)

            # Clean up subscriptions
            if sub_id in self.callbacks:
                del self.callbacks[sub_id]
            del self.subscription_ids[sub_id]
