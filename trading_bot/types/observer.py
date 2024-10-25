from typing import Protocol
from abc import abstractmethod
from trading_bot.types import OrderBookUpdate


class MarketDataObserver(Protocol):
    """
    Market data observer interface. Used to trigger various updates for which
    different observers can be updated with
    """

    @abstractmethod
    def on_orderbook_update(self, update: OrderBookUpdate) -> None: ...
