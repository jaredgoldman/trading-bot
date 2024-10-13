from trading_bot.exchange.binance.types import BinanceOrderBook
from trading_bot.types import OrderBook, Order, Instrument


def process_binance_order_book(
    order_book: BinanceOrderBook, instrument: Instrument
) -> OrderBook:
    """Process a Binance order book into a standard OrderBook object"""

    bids = []
    asks = []


    for [price, quantity] in order_book.bids:
        bids.append(Order(instrument, quantity, price, "open"))

    for [price, quantity] in order_book.asks:
        asks.append(Order(instrument, quantity, price, "open"))

    return OrderBook(bids, asks, instrument)
