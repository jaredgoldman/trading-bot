from trading_bot.types import Instrument, Order, OrderBookUpdate
from ..exchange import Exchange
from typing import List
import logging
import pendulum

logger = logging.getLogger(__name__)


class Binance(Exchange):
    """Binance exchange class"""

    orderbook_ws_endpoint = "wss://stream.binance.com:9443/ws"

    def extract_stream_names(self, instruments: dict[str, Instrument]) -> List[str]:
        return [
            instrument.name.lower() + "@depth" for instrument in instruments.values()
        ]

    def extract_orderbook_and_notify(self, data):
        update_instrument = data.get("s")
        if (instrument := self.instruments.get(update_instrument)) is None:
            logger.error(
                f"Received orderbook update for unknown instrument: {update_instrument}"
            )
            return

        bids = [
            Order(self.instruments[update_instrument], float(qty), float(price), "open")
            for price, qty in data["b"]
        ]

        asks = [
            Order(self.instruments[update_instrument], float(qty), float(price), "open")
            for price, qty in data["a"]
        ]

        order_book = OrderBookUpdate(
            bids, asks, instrument, pendulum.now().int_timestamp
        )

        self.notify_orderbook_update(order_book)

    @staticmethod
    def normalize_symbol(symbol: str) -> str:
        return symbol.replace("/", "").upper().replace("USD", "USDT")
