from trading_bot.types.observer import MarketDataObserver
from trading_bot.types.market import OrderBookUpdate
import logging

logger = logging.getLogger(__name__)


class Execution(MarketDataObserver):
    def maybe_execute_buy(self, top_bid: float, buy_threshold: float):
        if top_bid >= buy_threshold:
            logger.info(f"Buy at {top_bid}")

    def maybe_execute_sell(self, top_ask: float, sell_threshold: float):
        if top_ask <= sell_threshold:
            logger.info(f"Sell at {top_ask}")

    def on_orderbook_update(self, update: OrderBookUpdate):

        instrument = update.instrument
        top_bid = update.bids[0].price
        top_ask = update.asks[0].price
        spread = top_ask - top_bid

        self.maybe_execute_buy(top_bid, instrument.buy_threshold)
        self.maybe_execute_sell(top_ask, instrument.sell_threshold)

        logger.info(
            f"Instrument: {instrument.name}, spread: {spread}, Top bid: {top_bid}, Top ask: {top_ask}"
        )
