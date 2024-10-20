from typing import Dict, Any

from trading_bot.types import Instrument


class Config:
    INSTRUMENTS = ["BTC_USD"]

    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("__") and not callable(value)
        }

    @classmethod
    def process_instruments(cls) -> list[Instrument]:
        instruments = []
        for symbol in cls.INSTRUMENTS:
            base_asset, quote_asset = symbol.split("_")
            name = f"{base_asset}{quote_asset}"
            instruments.append(Instrument(name, base_asset, quote_asset))
        return instruments
