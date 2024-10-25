from trading_bot.types import Position


class RiskManager:
    def __init__(
        self, max_position_size: float, max_drawdown: float, stop_loss_pct: float
    ):
        self.max_position_size = max_position_size
        self.max_drawdown = max_drawdown
        self.stop_loss_pct = stop_loss_pct
        self.initial_capital = None
        self.current_capital = None

    def check_position_size(self, intended_size: float) -> bool:
        return intended_size <= self.max_position_size

    def check_drawdown(self, pnl: float) -> bool:
        if self.initial_capital is None:
            return True
        drawdown = (pnl / self.initial_capital) * 100
        return abs(drawdown) <= self.max_drawdown

    def should_stop_loss(self, position: Position, current_price: float) -> bool:
        if position.side == "long":
            loss_pct = (
                (current_price - position.entry_price) / position.entry_price * 100
            )
            return loss_pct <= -self.stop_loss_pct
        else:  # short
            loss_pct = (
                (position.entry_price - current_price) / position.entry_price * 100
            )
            return loss_pct <= -self.stop_loss_pct
