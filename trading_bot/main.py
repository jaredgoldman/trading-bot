from trading_bot.exchange import Binance, Exchange
from trading_bot.execution import Execution
from trading_bot.types import Instrument
from trading_bot.config import Config
from trading_bot.utils import Logger
from threading import Timer
import time


exchanges: list[Exchange] = [Binance()]


def add_observers(exchange: Exchange):
    """Add observers to the exchanges"""
    exchange.add_observer(Logger())
    exchange.add_observer(Execution())


def initialize_markets():
    """Initialize the market by fetching order books from all exchanges"""

    def initialize_exchanges(instruments: list[Instrument]):
        for exchange in exchanges:
            add_observers(exchange)
            for instrument in instruments:
                exchange.update_orderbook_ws(instrument)

    instruments = Config.process_instruments()
    Timer(5, initialize_exchanges, [instruments]).start()


def main():
    """Main runner"""
    initialize_markets()

    # keep the main thread alive
    while True:
        time.sleep(1)
