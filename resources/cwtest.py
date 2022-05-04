"""cwtest contains all the necessary blueprints for running the tests"""
import re

class Route:
    """
    Route represents the url.

    Attributes:
        base_url: str, in this case it is 'https://api.cryptowat.ch/'
        endpoint: str
        exchange: str
        pair: str
    """
    def __init__(self, endpoint, exchange=None, pair=None):
        """Constructs all the necessary attributes for the url"""
        self.base_url = "https://api.cryptowat.ch/"
        self.api_key = "ID9AJPGQ0ZNPZLSG2ML0"
        self.endpoint = endpoint
        self.exchange = exchange
        self.pair = pair

    def get_endpoint_url(self):
        """
        Returns the endpoint url
            E.g.: 'https://api.cryptowat.ch/markets'
        """
        return self.base_url + self.endpoint

    def get_exchange_url(self):
        """Returns the exchange url"""
        return self.get_endpoint_url() + "/" + self.exchange

    def get_pair_url(self):
        """Returns the pair url"""
        return self.get_exchange_url() + "/" + self.pair

    def get_pair_price_url(self):
        """Returns the pair price url"""
        return self.get_pair_url() + "/price"

    def get_all_market_prices_url(self):
        """Returns all market prices url"""
        return self.get_endpoint_url() + "/prices"

    def get_market_trades_url(self):
        """Returns the market trades url"""
        return self.get_pair_url() + "/trades"

    def get_market_summary_url(self):
        """Returns the market summary url"""
        return self.get_pair_url() + "/summary"

    def get_all_market_summaries_url(self):
        """Returns all market prices url"""
        return self.get_endpoint_url() + "/summaries"

    def get_order_book_url(self):
        """Returns the order book url"""
        return self.get_pair_url() + "/orderbook"

    def get_order_book_liq_url(self):
        """Returns the order book liquidty url"""
        return self.get_order_book_url() + "/liquidity"

    def test_allowance_data(self, response_body):
        """Tests the allowance data using regex"""
        assert re.match("([0-9a-z.])+", str(response_body["allowance"]["cost"]))
        assert re.match("([0-9.])+", str(response_body["allowance"]["remaining"]))
        if "remainingPaid" in response_body["allowance"]:
            assert re.match("([0-9.])+", str(response_body["allowance"]["remainingPaid"]))
        if "upgrade" in response_body["allowance"]:
            assert re.match("([0-9a-zA-z.])+", str(response_body["allowance"]["upgrade"]))
        if "account" in response_body["allowance"]:
            assert re.match("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                str(response_body["allowance"]["account"]))

    def test_cursor_data(self, response_body):
        """Tests the cursor data using regex"""
        assert re.match("([0-9a-zA-Z])+", str(response_body["cursor"]["last"]))
        assert re.match("(True)|(False)", str(response_body["cursor"]["hasMore"]))
