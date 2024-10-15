from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Any, ClassVar
from trading_bot.types import Instrument, OrderBook
from trading_bot.utils.ws import WebSocketManager
import requests


T = TypeVar("T")


class Exchange(ABC):
    """Exchange abstract class for integrations"""

    orderbook_ws_endpoint: ClassVar[str]

    def __init__(self):
        if hasattr(self.__class__, "orderbook_ws_endpoint"):
            self.ws_manager = WebSocketManager(self.__class__.orderbook_ws_endpoint)

    # @abstractmethod
    # def buy(self, asset: str, quantity: float, price: float) -> Order:
    #     """execute a limit buy order"""

    # @abstractmethod
    # def sell(self, asset: str, quantity: float, price: float) -> Order:
    #     """execute a limit sell order"""

    @abstractmethod
    def get_order_book(self, instrument: Instrument) -> OrderBook | None:
        """fetch an exchange orderbook"""

    # @abstractmethod
    # def get_balance(self, asset: str) -> float:
    #     """fetch an exchange balance"""

    # @abstractmethod
    # def get_assets(self) -> list[Asset]:
    #     """fetch exchange assets"""

    # @abstractmethod
    # def get_asset(self, asset: str) -> Asset:
    #     """fetch exchange assets"""

    def get_name(self) -> str:
        """return the exchange name"""
        return self.__class__.__name__.lower()

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

    def ws_subscribe(self, stream: str, callback: Callable[[Any], None]):
        """Subscribe to a websocket stream"""

        self.ws_manager.subscribe(stream, callback)

    def ws_unsubscribe(self, stream: str):
        """Unsubscribe from a websocket stream"""

        self.ws_manager.unsubscribe(stream)
