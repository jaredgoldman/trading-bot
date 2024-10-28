from typing import Dict, Callable
from trading_bot.types import Instrument, StrategyConfig


class Config:
    """Configuration class for the trading bot"""

    INSTRUMENTS: Dict[str, Instrument] = {
        "BTC_USD": Instrument(
            name="BTC_USD",
            base_asset="BTC",
            quote_asset="USD",
            buy_threshold=67434,
            sell_threshold=67450,
            min_size_usd=30,
            max_size_usd=100,
            max_drawdown=2.0,
            stop_loss_pct=1.0,
        ),
        "ETH_USD": Instrument(
            name="ETH_USD",
            base_asset="ETH",
            quote_asset="USD",
            buy_threshold=2647,
            sell_threshold=2647,
            min_size_usd=30,
            max_size_usd=100,
            max_drawdown=2.0,
            stop_loss_pct=1.0,
        ),
    }

    STRATEGIES: dict[str, StrategyConfig] = {
        "spot": StrategyConfig(
            strategy="spot", enabled=True, min_spread=0.001, max_spread=0.005
        ),
    }

    @classmethod
    def get_strategies(cls):
        """Return the available strategies"""
        return cls.STRATEGIES

    @classmethod
    def process_instruments(
        cls, normalize_symbol: Callable[[str], str]
    ) -> dict[str, Instrument]:
        """Process instruments in config using the provided exchange-specific symbol normalizer"""
        return {
            normalize_symbol(config.name): Instrument(
                normalize_symbol(config.name),
                normalize_symbol(config.base_asset),
                normalize_symbol(config.quote_asset),
                config.buy_threshold,
                config.sell_threshold,
                config.min_size_usd,
                config.max_size_usd,
                config.max_drawdown,
                config.stop_loss_pct,
            )
            for config in cls.INSTRUMENTS.values()
        }
