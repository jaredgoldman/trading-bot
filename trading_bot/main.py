from trading_bot.market import initialize_markets
from trading_bot.state import GlobalState
import time
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

global_state = GlobalState()


def main():
    """Main runner"""
    initialize_markets()

    while True:
        time.sleep(1)
