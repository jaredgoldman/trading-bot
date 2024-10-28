from abc import ABC, abstractmethod
from typing import TypeVar, Any, ClassVar, Set, List
from trading_bot.types import (
    Instrument,
    MarketDataObserver,
    OrderBookUpdate,
)
from trading_bot.utils import WebSocketManager


T = TypeVar("T")


class Exchange(ABC):
    """Abstract class for exchange integrations"""

    base_url: ClassVar[str]
    orderbook_ws_endpoint: ClassVar[str]
    instruments: dict[str, Instrument]

    def __init__(self, instruments: dict[str, Instrument]):
        self.instruments = instruments
        self.observers: Set[MarketDataObserver] = set()
        self.ws_manager = WebSocketManager(self.__class__.orderbook_ws_endpoint)

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

    def subscribe_orderbook(self):
        """subscribe to the exchange orderbook and notify observers"""
        self.ws_manager.subscribe(
            self.extract_stream_names(self.instruments),
            self.extract_orderbook_and_notify,
        )
