from trading_bot.types import Position, Instrument


class RiskManager:
    """Risk manager class for managing risk and position sizing"""

    def __init__(
        self,
    ):
        self.initial_capital = None
        self.current_capital = None

    def check_position_size(self, intended_size: float, instrument: Instrument) -> bool:
        """Check if the intended position size is within risk limits"""
        return intended_size <= instrument.max_size

    def check_drawdown(self, pnl: float, instrument: Instrument) -> bool:
        """Check if the drawdown is within risk limits"""
        if self.initial_capital is None:
            return True
        drawdown = (pnl / self.initial_capital) * 100
        return abs(drawdown) <= instrument.max_drawdown

    def should_stop_loss(
        self,
        position: Position,
        current_price: float,
        instrument: Instrument,
    ) -> bool:
        """Check if the position should be stopped out based on stop loss"""
        if position.side == "long":
            loss_pct = (
                (current_price - position.entry_price) / position.entry_price * 100
            )
            return loss_pct <= -instrument.stop_loss_pct
        else:  # short
            loss_pct = (
                (position.entry_price - current_price) / position.entry_price * 100
            )
            return loss_pct <= -instrument.stop_loss_pct
