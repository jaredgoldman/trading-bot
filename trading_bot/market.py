from trading_bot.types.observer import MarketDataObserver
from trading_bot.types.types import OrderBookUpdate


class Market(MarketDataObserver):
    def on_orderbook_update(self, update: OrderBookUpdate):
        top_bid = update.bids[0]
        top_ask = update.asks[0]
        spread = top_ask.price - top_bid.price
        pass
