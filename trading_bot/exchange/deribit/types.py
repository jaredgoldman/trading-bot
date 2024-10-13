from dataclasses import dataclass, field
from typing import List, Optional, Generic, TypeVar

T = TypeVar("T")


@dataclass
class OrderEntry:
    quantity: int
    price: float
    cm: int


@dataclass
class DeribitResponse(Generic[T]):
    jsonrpc: str
    id: int
    result: T
    usIn: int
    usOut: int
    usDiff: int
    testnet: bool


@dataclass
class DeribitOrderBook:
    bids: List[OrderEntry] = field(default_factory=list)
    asks: List[OrderEntry] = field(default_factory=list)
    state: str = "open"
    settlement_price: Optional[float] = None
    instrument: str = ""
    tstamp: int = 0
    last: Optional[float] = None
    low: Optional[float] = None
    high: Optional[float] = None
    mark: Optional[float] = None
    u_px: Optional[float] = None
    u_ix: Optional[str] = None
    i_r: float = 0
    mark_iv: Optional[float] = None
    ask_iv: Optional[float] = None
    bid_iv: Optional[float] = None
    max: Optional[float] = None
    min: Optional[float] = None

    # XXX: Build this into class exchange-specific order-book classes will inherit from
    def __post_init__(self):
        if self.state not in ["open", "closed"]:
            raise ValueError("State must be either 'open' or 'closed'")
        if not self.instrument:
            raise ValueError("Instrument is required")
