from typing import Dict, Optional
from .types import OrderBook


class GlobalState:
    """Global state of the trading bot"""

    order_books: Dict[str, OrderBook]

    def __init__(self):
        self.order_books = {}

    def update_order_book(self, order_book: OrderBook, exchange: str) -> None:
        self.order_books[exchange] = order_book

    def get_order_book(self, exchange: str) -> Optional[OrderBook]:
        return self.order_books.get(exchange)
