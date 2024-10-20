from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Any, ClassVar
from trading_bot.types import Instrument, OrderBook
from trading_bot.utils.ws import WebSocketManager
import requests


T = TypeVar("T")


class Exchange(ABC):
    """Exchange abstract class for integrations"""

    base_url: ClassVar[str]
    orderbook_ws_endpoint: ClassVar[str]

    def __init__(self):
        if hasattr(self.__class__, "orderbook_ws_endpoint"):
            self.ws_manager = WebSocketManager(self.__class__.orderbook_ws_endpoint)

    def get_name(self) -> str:
        """return the exchange name"""
        return self.__class__.__name__.lower()

    @abstractmethod
    def get_orderbook_snapshot(self, instrument: Instrument) -> OrderBook | None:
        """fetch an exchange orderbook"""

    @abstractmethod
    def get_orderbook_ws(self, instrument: Instrument) -> OrderBook | None:
        """fetch an exchange orderbook"""

    def request(
        self, method: str, endpoint: str, response_type: Callable[[Any], T], **kwargs
    ) -> T:
        """Make a request to the exchange API and return the expected type."""

        try:
            response = requests.request(method, endpoint, **kwargs)
            response.raise_for_status()  # Raises an HTTPError for bad responses

            # Check if the response is JSON
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                data = response.json()
            else:
                data = response.text

            return response_type(data)
        except requests.RequestException as e:
            # Handle network errors, timeouts, etc.
            raise RuntimeError(f"Request failed: {str(e)}") from e
        except ValueError as e:
            # Handle JSON decoding errors
            raise RuntimeError(f"Failed to parse response: {str(e)}") from e
