from dataclasses import dataclass


@dataclass
class Asset:
    name: str
    price: float


@dataclass
class Instrument:
    name: str
    base_asset: str
    quote_asset: str
    buy_threshold: float
    sell_threshold: float
    min_size: float
    max_size: float
    max_drawdown: float
    stop_loss_pct: float


@dataclass(order=True)
class Order:
    asset: str | Instrument
    quantity: float
    price: float
    status: str


@dataclass
class OrderBookUpdate:
    bids: list[Order]
    asks: list[Order]
    instrument: Instrument
    timestamp: int


@dataclass
class Position:
    size: float
    entry_price: float
    side: str  # 'long' or 'short'


@dataclass
class StrategyConfig:
    strategy: str
    enabled: bool
    min_spread: float
    max_spread: float


@dataclass
class Signal:
    action: str | None
    size: float
