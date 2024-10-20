import websocket
import json
import threading
from typing import Callable, Any, Dict, TypeVar
from queue import Queue
import queue
import logging
import traceback
import sys

logger = logging.getLogger(__name__)
T = TypeVar("T")


class WebSocketManager:

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.subscriptions: Dict[str, Queue] = {}
        self.subscription_ids: Dict[int, str] = (
            {}
        )  # New: map subscription IDs to streams
        self.ws: websocket.WebSocketApp | None = None
        self.connect()

    current_stream: str

    def connect(self):

        def on_message(ws, message):
            """
            This is a hacky way to process Binance order book data which sends
            a dict with with a sub ID and result: None and then the actual data that is not
            keyed with the sub ID. This is a workaround to process the data correctly. Once
            This bot starts consuming multiple streams of data, this will need to be refactored.
            One idea is to use match cases to parse the data and add to the correct que that way.
            """
            logger.debug(f"Received message: {message[:100]}...")
            try:
                data = json.loads(message)
                subscription_id = data.get("id")
                last_update_id = data.get("lastUpdateId")

                if subscription_id:
                    current_stream = self.subscription_ids.get(subscription_id)
                    if current_stream:
                        logger.debug(
                            f"Received initializing message, assigning current stream: ${data}"
                        )
                        self.current_stream = current_stream

                elif last_update_id and self.current_stream:
                    logger.debug(
                        f"Received order book update for stream: {self.current_stream}"
                    )
                    self._process_stream_message(self.current_stream, data)
                else:
                    logger.warning(f"Received message with unknown format: {message}")

            except json.JSONDecodeError:
                logger.error(f"Failed to decode JSON message: {message}")
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}", exc_info=True)

        def on_error(ws, error):
            logger.error(f"WebSocket error: {error}")

        def on_close(ws, close_status_code, close_msg):
            logger.warning(f"WebSocket closed: {close_status_code} - {close_msg}")
            logger.info("Attempting to reconnect...")
            self.connect()

        def on_open(ws):
            logger.info(f"WebSocket connection opened to {self.endpoint}")
            for stream in self.subscriptions:
                logger.debug(f"Resubscribing to stream: {stream}")
                self.send_subscription(stream)

        logger.info(f"Connecting to WebSocket at {self.endpoint}")
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
        logger.debug("WebSocket thread started")

    def _process_stream_message(self, stream: str, data: Dict[str, Any]):
        logger.debug(f"Processing message for stream: {stream}")
        if stream in self.subscriptions:
            self.subscriptions[stream].put(data)
        else:
            logger.warning(f"Received message for unsubscribed stream: {stream}")

    def subscribe(self, stream: str, callback: Callable[[Any], T]):
        if stream not in self.subscriptions:
            self.subscriptions[stream] = queue.Queue()
            subscription_id = self.send_subscription(stream)
            self.subscription_ids[subscription_id] = stream

        def stream_handler():
            thread_id = threading.get_ident()
            logger.debug(f"Stream handler started in thread: {thread_id}")
            try:
                while True:
                    logger.debug(f"Waiting for data on stream: {stream}")
                    try:
                        data = self.subscriptions[stream].get(timeout=5)
                        logger.debug(f"Received data on stream {stream}: {data}")
                        logger.debug(f"Calling callback with data: {data}")
                        callback(data)
                        logger.debug("Callback completed")
                    except queue.Empty:
                        logger.warning(
                            f"No data received on stream {stream} for 5 seconds"
                        )
            except Exception as e:
                error_type = type(e).__name__
                error_message = str(e)
                logger.error(f"Error in stream_handler: {error_type} - {error_message}")
                logger.error("Full traceback:")
                logger.error(traceback.format_exc())
                print(
                    f"Error in stream_handler: {error_type} - {error_message}",
                    file=sys.stderr,
                )
                traceback.print_exc(file=sys.stderr)

        threading.Thread(target=stream_handler, daemon=True).start()

    def send_subscription(self, stream: str) -> int:
        subscription_id = hash(stream)  # or any other method to generate unique IDs
        subscribe_message = json.dumps(
            {"method": "SUBSCRIBE", "params": [stream], "id": subscription_id}
        )
        if self.ws:
            self.ws.send(subscribe_message)
        return subscription_id

    def unsubscribe(self, stream: str):
        if stream in self.subscriptions:
            del self.subscriptions[stream]
            # Remove the subscription ID associated with this stream
            subscription_id = next(
                (id for id, s in self.subscription_ids.items() if s == stream), None
            )
            if subscription_id:
                del self.subscription_ids[subscription_id]
                unsubscribe_message = json.dumps(
                    {"method": "UNSUBSCRIBE", "params": [stream], "id": subscription_id}
                )
                if self.ws:
                    self.ws.send(unsubscribe_message)
