from trading_bot.market import initialize_markets
from trading_bot.exchange.binance.binance import Binance
from trading_bot.exchange.exchange import Exchange
from trading_bot.types.types import Instrument
from trading_bot.config import Config
from threading import Timer
from trading_bot.utils.logger import Logger
import time


exchanges: list[Exchange] = [Binance()]


def initialize_markets():
    """Initialize the market by fetching order books from all exchanges"""

    def initialize_exchanges(instruments: list[Instrument]):
        for exchange in exchanges:
            exchange.add_observer(Logger())
            for instrument in instruments:
                exchange.update_orderbook_ws(instrument)

    instruments = Config.process_instruments()
    Timer(5, initialize_exchanges, [instruments]).start()


def main():
    """Main runner"""
    initialize_markets()

    while True:
        time.sleep(1)
