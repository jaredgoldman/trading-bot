from trading_bot.types import OrderBookUpdate, Position, Signal
from trading_bot.risk import RiskManager
from typing import List, Optional
from abc import ABC, abstractmethod
import logging

from trading_bot.types.market import Signal


logger = logging.getLogger(__name__)


class BaseStrategy(ABC):
    """Base strategy class for implementing trading strategies"""

    def __init__(self, risk_manager: RiskManager):
        self.risk_manager = risk_manager
        self.position: Optional[Position] = None
        self.trades: List[Position] = []

    @abstractmethod
    def analyze_market(self, update: OrderBookUpdate) -> Signal:
        """Analyze market data and return trading signals"""
        pass

    def execute_trade(self, signal: Signal, update: OrderBookUpdate) -> None:
        """Execute trade based on signal and risk management rules"""

        if signal.action == "buy" and (
            self.position is None or self.position.side == "short"
        ):
            size = signal.size or 0
            if self.risk_manager.check_position_size(size, update.instrument):
                # Implement actual trade execution logic here
                self.position = Position(
                    size=size, entry_price=update.asks[0].price, side="long"
                )
                logger.info(f"Executed long position: {self.position}")

        elif signal.action == "sell" and (
            self.position is None or self.position.side == "long"
        ):
            size = signal.size or 0
            if self.risk_manager.check_position_size(size, update.instrument):
                # Implement actual trade execution logic here
                self.position = Position(
                    size=size, entry_price=update.bids[0].price, side="short"
                )
                logger.info(f"Executed short position: {self.position}")

    def check_exit_conditions(self, update: OrderBookUpdate) -> None:
        """Check exit conditions based on risk management rules"""

        if self.position is None:
            return

        current_price = (
            update.bids[0].price
            if self.position.side == "long"
            else update.asks[0].price
        )

        if self.risk_manager.should_stop_loss(
            self.position, current_price, update.instrument
        ):
            # Implement actual exit logic here
            logger.warning(f"Stop loss triggered for position: {self.position}")
            self.trades.append(self.position)
            self.position = None


class SpotStrategy(BaseStrategy):
    """Spot strategy class for implementing spot trading strategies"""

    def __init__(self, risk_manager: RiskManager, min_spread: float, max_spread: float):
        super().__init__(risk_manager)
        self.min_spread = min_spread
        self.max_spread = max_spread

    def analyze_market(self, update: OrderBookUpdate) -> Signal:
        best_bid = update.bids[0]
        best_ask = update.asks[0]
        spread = best_ask.price - best_bid.price
        spread_percentage = (spread / best_bid.price) * 100

        action = None
        size = 0

        # Example strategy logic based on spread
        if spread_percentage <= self.min_spread and self.position is None:
            # Market is very liquid and stable
            # Could be good time to:
            # - Start market making
            # - Take mean reversion trades
            # - Execute large orders with less slippage            pass
            action = "buy"
            size = min(best_ask.quantity, update.instrument.max_size)
        elif spread_percentage >= self.max_spread and self.position is None:
            # Market might be volatile or illiquid
            # Consider:
            # - Reducing position sizes
            # - Widening stop losses
            # - Pausing new trades
            # - Looking for arbitrage opportunities
            action = "sell"
            size = min(best_bid.quantity, update.instrument.max_size)

        return Signal(action, size)
