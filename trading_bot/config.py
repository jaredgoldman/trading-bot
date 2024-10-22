from dataclasses import dataclass
from typing import Dict, List, Any
from trading_bot.types.market import Instrument


@dataclass
class InstrumentConfig:
    buy_threshold: float
    sell_threshold: float


class Config:
    """Configuration class for the trading bot"""

    INSTRUMENTS: Dict[str, InstrumentConfig] = {
        "BTC_USD": InstrumentConfig(buy_threshold=67434, sell_threshold=67435),
        "ETH_USD": InstrumentConfig(buy_threshold=2647, sell_threshold=2647),
    }

    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("__") and not callable(value)
        }

    @classmethod
    def process_instruments(cls) -> List[Instrument]:
        instruments = []
        for symbol, config in cls.INSTRUMENTS.items():
            base_asset, quote_asset = symbol.split("_")
            name = f"{base_asset}{quote_asset}"
            instruments.append(
                Instrument(
                    name,
                    base_asset,
                    quote_asset,
                    config.buy_threshold,
                    config.sell_threshold,
                )
            )
        return instruments

    @classmethod
    def get_thresholds(cls, symbol: str) -> InstrumentConfig:
        return cls.INSTRUMENTS[symbol]
