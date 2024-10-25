from trading_bot.types import OrderBookUpdate, Position
from trading_bot.risk import RiskManager
from typing import List, Optional
from abc import ABC, abstractmethod
import logging


logger = logging.getLogger(__name__)


class BaseStrategy(ABC):
    def __init__(self, risk_manager: RiskManager):
        self.risk_manager = risk_manager
        self.position: Optional[Position] = None
        self.trades: List[Position] = []

    @abstractmethod
    def analyze_market(self, update: OrderBookUpdate) -> dict:
        """Analyze market data and return trading signals"""
        pass

    def execute_trade(self, signal: dict, update: OrderBookUpdate) -> None:
        """Execute trade based on signal and risk management rules"""
        if signal.get("action") == "buy" and (
            self.position is None or self.position.side == "short"
        ):
            size = signal.get("size", 0)
            if self.risk_manager.check_position_size(size):
                # Implement actual trade execution logic here
                self.position = Position(
                    size=size, entry_price=update.asks[0].price, side="long"
                )
                logger.info(f"Executed long position: {self.position}")

        elif signal.get("action") == "sell" and (
            self.position is None or self.position.side == "long"
        ):
            size = signal.get("size", 0)
            if self.risk_manager.check_position_size(size):
                # Implement actual trade execution logic here
                self.position = Position(
                    size=size, entry_price=update.bids[0].price, side="short"
                )
                logger.info(f"Executed short position: {self.position}")

    def check_exit_conditions(self, update: OrderBookUpdate) -> None:
        """Check if we need to exit position based on risk management rules"""
        if self.position is None:
            return

        current_price = (
            update.bids[0].price
            if self.position.side == "long"
            else update.asks[0].price
        )

        if self.risk_manager.should_stop_loss(self.position, current_price):
            # Implement actual exit logic here
            logger.warning(f"Stop loss triggered for position: {self.position}")
            self.trades.append(self.position)
            self.position = None


class SpotStrategy(BaseStrategy):
    def __init__(self, risk_manager: RiskManager, min_spread: float, max_spread: float):
        super().__init__(risk_manager)
        self.min_spread = min_spread
        self.max_spread = max_spread

    def analyze_market(self, update: OrderBookUpdate) -> dict:
        best_bid = update.bids[0]
        best_ask = update.asks[0]
        spread = best_ask.price - best_bid.price

        signal = {"action": None, "size": 0}

        # Example strategy logic based on spread
        if spread < self.min_spread and self.position is None:
            signal = {
                "action": "buy",
                "size": min(best_ask.quantity, self.risk_manager.max_position_size),
            }
        elif spread > self.max_spread and self.position is None:
            signal = {
                "action": "sell",
                "size": min(best_bid.quantity, self.risk_manager.max_position_size),
            }

        return signal
