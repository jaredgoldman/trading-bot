from trading_bot.exchange.binance.binance import Binance
from trading_bot.exchange.exchange import Exchange
from trading_bot.types import Instrument, OrderBook

exchanges: list[Exchange] = [Binance()]
order_books: dict[str, dict[str, OrderBook | None]] = {}


def initialize_market(instruments: list[Instrument]):
    """Initialize the market by fetching order books from all exchanges"""
    for exchange in exchanges:
        for instrument in instruments:
            exchange.get_orderbook_ws(instrument)

