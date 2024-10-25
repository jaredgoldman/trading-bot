from .types import DeribitOrderBook
from trading_bot.exchange import Exchange
import requests


class Deribit(Exchange):
    """Deribit exchange class"""

    # def buy(self, asset: str, quantity: float, price: float):
    #     """Execute a limit buy order"""
    #     return self.request(
    #         "POST",
    #         f"{self.private_url}/buy",
    #         json={"instrument_name": asset, "amount": quantity, "price": price},
    #     )
    #     pass

    # def sell(self, asset: str, quantity: float, price: float):
    #     """Execute a limit sell order"""
    #     return self.request(
    #         "POST",
    #         f"{self.private_url}/sell",
    #         json={"instrument_name": asset, "amount": quantity, "price": price},
    #     )
    #     pass

    def get_order_book(self, currency="BTC", depth=None):
        """Fetch an exchange orderbook"""
        # Use testnet URL for testing, change to www.deribit.com for live trading
        base_url = (
            "https://deribit.com/api/v2/public"
        )
        endpoint = f"{base_url}/get_book_summary_by_currency"

        params = {"currency": currency}
        if depth is not None:
            params["depth"] = depth

        try:
            order_book = self.request("GET", endpoint, DeribitOrderBook, params=params)
            print(order_book)
            return order_book
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error occurred: {e}")
            print(f"Response content: {e.response.content}")
            raise

    # def get_balance(self, asset: str):
    #     """Fetch an exchange balance"""
    #     self.request("GET", f"{self.private_url}/get_balance", json={"currency": asset})
    #     pass

    # def get_assets(self):
    #     """Fetch exchange assets"""
    #     self.request("GET", f"{self.public_url}/get_instruments")
    #     pass

    # def get_asset(self, asset: str):
    #     """Fetch exchange assets"""
    #     self.request(
    #         "GET", f"{self.public_url}/get_instruments", json={"currency": asset}
    #     )
    #     pass
