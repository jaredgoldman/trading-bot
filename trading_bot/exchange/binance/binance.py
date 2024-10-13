from trading_bot.types import Instrument
from .types import BinanceOrderBook
from ..exchange import Exchange
from .utils import process_binance_order_book


class Binance(Exchange):
    """Binance exchange class"""

    base_url = "https://api.binance.com"

    def get_order_book(self, instrument: Instrument, depth=1):
        """Fetch binance orderbook"""

        endpoint = f"{self.base_url}/api/v3/depth"
        order_book = self.request(
            "GET",
            endpoint,
            BinanceOrderBook,
            params={"symbol": instrument.name, "limit": depth},
        )
        return process_binance_order_book(order_book, instrument)
