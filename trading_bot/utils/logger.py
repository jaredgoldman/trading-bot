from trading_bot.types.observer import MarketDataObserver
import pendulum
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Logger(MarketDataObserver):
    """Logger class for logging main events"""

    def on_orderbook_update(self, update):
        """Log orderbook update"""
        logger.info(
            f"{update.instrument.name} - {pendulum.from_timestamp(update.timestamp)} - {update.bids[:5]} - {update.asks[:5]}"
        )
