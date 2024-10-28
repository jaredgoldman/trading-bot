from trading_bot.types import OrderBookUpdate, MarketDataObserver
from trading_bot.config import Config
from trading_bot.risk import RiskManager
from trading_bot.strategy import SpotStrategy
from trading_bot.config import Config
import logging

logger = logging.getLogger(__name__)


class Execution(MarketDataObserver):
    """Execution class for the trading bot"""

    def __init__(self):
        # Initialize risk manager with example parameters
        risk_manager = RiskManager()

        # Initialize strategy with risk manager
        self.spot_strategy = SpotStrategy(
            risk_manager=risk_manager,
            min_spread=0.001,  # 0.1% minimum spread
            max_spread=0.005,  # 0.5% maximum spread
        )

    def on_orderbook_update(self, update: OrderBookUpdate):
        if Config.STRATEGIES["spot"].enabled:
            # Analyze market and get trading signals
            signal = self.spot_strategy.analyze_market(update)

            # Check risk management and execute trades
            self.spot_strategy.check_exit_conditions(update)
            self.spot_strategy.execute_trade(signal, update)
