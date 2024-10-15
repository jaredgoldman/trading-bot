import websocket
import json
import threading
from typing import Callable, Any, Dict
from queue import Queue


class WebSocketManager:
    """WebSocket manager for handling subscriptions"""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.subscriptions: Dict[str, Queue] = {}
        self.ws: websocket.WebSocketApp | None = None
        self.connect()

    def connect(self):
        def on_message(ws, message):
            data = json.loads(message)
            stream = data.get("stream")
            if stream and stream in self.subscriptions:
                self.subscriptions[stream].put(data)

        def on_error(ws, error):
            print(f"WebSocket error: {error}")

        def on_close(ws, close_status_code, close_msg):
            print(f"WebSocket closed: {close_status_code} - {close_msg}")
            # Attempt to reconnect
            self.connect()

        def on_open(ws):
            print(f"WebSocket connection opened to {self.endpoint}")
            # Resubscribe to all streams
            for stream in self.subscriptions:
                self.send_subscription(stream)

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

    def subscribe(self, stream: str, callback: Callable[[Any], None]):
        if stream not in self.subscriptions:
            self.subscriptions[stream] = Queue()
            self.send_subscription(stream)

        def stream_handler():
            while True:
                data = self.subscriptions[stream].get()
                callback(data)

        threading.Thread(target=stream_handler, daemon=True).start()

    def send_subscription(self, stream: str):
        subscribe_message = json.dumps(
            {"method": "SUBSCRIBE", "params": [stream], "id": 1}
        )
        if self.ws:
            self.ws.send(subscribe_message)

    def unsubscribe(self, stream: str):
        if stream in self.subscriptions:
            del self.subscriptions[stream]
            unsubscribe_message = json.dumps(
                {"method": "UNSUBSCRIBE", "params": [stream], "id": 1}
            )
            if self.ws:
                self.ws.send(unsubscribe_message)
