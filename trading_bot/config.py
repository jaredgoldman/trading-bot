from typing import Dict, Callable, Any
from trading_bot.types import Instrument, InstrumentConfig, StrategyConfig


class Config:
    """Configuration class for the trading bot"""

    INSTRUMENTS: Dict[str, InstrumentConfig] = {
        "BTC_USD": InstrumentConfig(
            buy_threshold=67434,
            sell_threshold=67450,
            min_size_usd=30,
            max_size_usd=100,
        ),
        "ETH_USD": InstrumentConfig(
            buy_threshold=2647,
            sell_threshold=2647,
            min_size_usd=30,
            max_size_usd=100,
        ),
    }

    STRATEGIES: dict[str, StrategyConfig] = {
        "spot": StrategyConfig(
            strategy="spot", enabled=True, min_spread=0.001, max_spread=0.005
        ),
    }

    @classmethod
    def get_strategies(cls):
        return cls.STRATEGIES

    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("__") and not callable(value)
        }

    @classmethod
    def process_instruments(
        cls, normalize_symbol: Callable[[str], str]
    ) -> dict[str, Instrument]:
        instruments = {}
        for symbol, config in cls.INSTRUMENTS.items():
            base_asset, quote_asset = symbol.split("_")
            name = normalize_symbol(f"{base_asset}{quote_asset}")
            base_asset = normalize_symbol(base_asset)
            quote_asset = normalize_symbol(quote_asset)
            instruments.update(
                {
                    name: Instrument(
                        name,
                        base_asset,
                        quote_asset,
                        config.buy_threshold,
                        config.sell_threshold,
                    )
                }
            )
        return instruments
