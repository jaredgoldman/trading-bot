from trading_bot.exchange.binance.binance import Binance
from trading_bot.exchange.exchange import Exchange
from trading_bot.types import Instrument
from trading_bot.config import Config
from threading import Timer


exchanges: list[Exchange] = [Binance()]


def initialize_markets():
    """Initialize the market by fetching order books from all exchanges"""

    def update_order_books(instruments: list[Instrument]):
        for exchange in exchanges:
            for instrument in instruments:
                exchange.update_orderbook_ws(instrument)

    instruments = Config.process_instruments()
    Timer(5, update_order_books, [instruments]).start()
