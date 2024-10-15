from trading_bot.types import Instrument
from .types import BinanceOrderBook
from ..exchange import Exchange
from .utils import normalize_binance_symbol, process_binance_order_book


class Binance(Exchange):
    """Binance exchange class"""

    base_url = "https://api.binance.com"
    orderbook_ws_endpoint = "wss://stream.binance.com:9443/ws"

    def get_order_book_snapshot(self, instrument: Instrument, depth=1):
        """Fetch binance orderbook via http"""

        endpoint = f"{self.base_url}/api/v3/depth"

        symbol = normalize_binance_symbol(instrument.name)

        order_book = self.request(
            "GET",
            endpoint,
            BinanceOrderBook,
            params={"symbol": symbol, "limit": depth},
        )

        return process_binance_order_book(order_book, instrument)

    def get_order_book_ws(self, instrument: Instrument):
        """Fetch binance orderbook via websocket"""

        symbol = normalize_binance_symbol(instrument.name)

        self.ws_manager.subscribe(
            f"{symbol.lower()}@depth", process_binance_order_book(data, instrument)
        )
