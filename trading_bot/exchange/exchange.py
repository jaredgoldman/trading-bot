from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Any, ClassVar, Set, List
from trading_bot.types import (
    Instrument,
    OrderBook,
    MarketDataObserver,
    OrderBookUpdate,
)
from trading_bot.utils import WebSocketManager
import requests


T = TypeVar("T")


class Exchange(ABC):
    """Exchange abstract class for integrations"""

    base_url: ClassVar[str]
    orderbook_ws_endpoint: ClassVar[str]
    instruments: dict[str, Instrument]

    def __init__(self, instruments: dict[str, Instrument]):
        self.instruments = instruments
        self.observers: Set[MarketDataObserver] = set()
        self.ws_manager = WebSocketManager(self.__class__.orderbook_ws_endpoint)

    def get_name(self) -> str:
        """return the exchange name"""
        return self.__class__.__name__.lower()

    def add_observer(self, observer: MarketDataObserver):
        """add an observer to the exchange"""
        self.observers.add(observer)

    def notify_orderbook_update(self, update: OrderBookUpdate):
        """notify all observers of an orderbook update"""
        for observer in self.observers:
            observer.on_orderbook_update(update)

    @abstractmethod
    def get_orderbook_snapshot(self, instrument: Instrument) -> OrderBook | None:
        """fetch an exchange orderbook"""

    @staticmethod
    @abstractmethod
    def normalize_symbol(symbol: str) -> str:
        """normalize a symbol to the exchange format"""

    @abstractmethod
    def extract_stream_names(self, instruments: dict[str, Instrument]) -> List[str]:
        """extract stream names from instruments"""

    @abstractmethod
    def extract_orderbook_and_notify(self, data: Any):
        """extract orderbook data from a websocket message"""

    def subscribe_orderbook(self):
        """subscribe to the exchange orderbook and notify observers"""
        self.ws_manager.subscribe(
            self.extract_stream_names(self.instruments),
            self.extract_orderbook_and_notify,
        )

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
