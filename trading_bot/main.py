from trading_bot.exchange import Binance, Exchange
from trading_bot.execution import Execution
from trading_bot.config import Config
from trading_bot.utils import Logger
from threading import Timer
from typing import Type
import time


exchanges: list[Type[Exchange]] = [Binance]


def add_observers(exchange: Exchange):
    """Add observers to the exchanges"""
    exchange.add_observer(Logger())
    exchange.add_observer(Execution())


def initialize_exchanges():
    for exchange in exchanges:
        instruments = Config.process_instruments(exchange.normalize_symbol)
        exchange_instance = exchange(instruments)
        add_observers(exchange_instance)
        time.sleep(1)
        exchange_instance.subscribe_orderbook()


def main():
    """Main runner"""
    initialize_exchanges()

    # keep the main thread alive
    while True:
        time.sleep(1)
