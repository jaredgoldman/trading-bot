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


@dataclass(order=True)
class Order:
    asset: str | Instrument
    quantity: float
    price: float
    status: str


@dataclass
class OrderBook:
    bids: list[Order]
    asks: list[Order]
    instrument: Instrument
