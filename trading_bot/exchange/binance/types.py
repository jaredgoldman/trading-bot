from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class BinanceOrderBook:
    lastUpdateId: int
    bids: List[Tuple] = field(default_factory=list)
    asks: List[Tuple] = field(default_factory=list)
