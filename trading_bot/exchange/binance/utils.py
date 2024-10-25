from .types import BinanceOrderBook
from trading_bot.types import OrderBook, Order, Instrument


def process_binance_order_book(
    order_book: BinanceOrderBook, instrument: Instrument
) -> OrderBook:
    """Process a Binance order book into a standard OrderBook object"""

    bids = []
    asks = []

    for [price, quantity] in order_book.bids:
        bids.append(Order(instrument, float(quantity), float(price), "open"))

    for [price, quantity] in order_book.asks:
        asks.append(Order(instrument, float(quantity), float(price), "open"))

    return OrderBook(bids, asks, instrument)


def normalize_binance_symbol(symbol: str) -> str:
    """Normalize a Binance symbol to the format used by the exchange"""

    return symbol.replace("/", "").upper().replace("USD", "USDT")
