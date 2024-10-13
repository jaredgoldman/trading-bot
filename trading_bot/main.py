from trading_bot.config import Config
from trading_bot.market import initialize_market


def main():
    instruments = Config.process_instruments()
    initialize_market(instruments)
