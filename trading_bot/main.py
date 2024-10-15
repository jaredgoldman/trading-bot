from trading_bot.config import Config
from trading_bot.market import initialize_market
from threading import Timer
import time


def main():
    """Main runner"""
    instruments = Config.process_instruments()
    Timer(5, initialize_market, [instruments]).start()

    while True:
        time.sleep(1)
