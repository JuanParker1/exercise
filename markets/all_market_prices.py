"""This module is testing the market price for every market on the platform endpoint"""
import re
import requests
from jsonschema import validate
from resources.cwtest import Route

route = Route(endpoint="markets", exchange="kraken", pair="ltcusd")
response = requests.get(route.get_all_market_prices_url(), headers={"X-CW-API-Key": route.api_key})
response_body = response.json()

def test_all_market_prices_endpoint_status_code():
    """Tests that the status code is 200 OK"""
    assert response.status_code == 200

def test_all_market_prices_endpoint_headers():
    """Verifying that headers are present (verifying based on requirements)."""
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Connection"] == "keep-alive"
    keys = ["Date", "Content-Type",
            "Connection", "Access-Control-Allow-Headers",
            "Content-Encoding", "Referrer-Policy", "Vary",
            "X-Content-Type-Options", "CF-Cache-Status",
            "Expect-CT", "Set-Cookie", "Strict-Transport-Security",
            "Server", "CF-RAY"]
    for k in keys:
        if k not in response.headers:
            assert False, "'" + k + "' is not in Headers keys"

def test_all_market_prices_endpoint_against_schema():
    """Verifying that the returned body is correct using a schema"""
    schema = {
        "type": "object",
        "properties": {
            "result": {
                "type": "object",
                "propertyNames": {"pattern": ".*:(bitfinex)|(coinbase-pro)|(bitstamp)|"+
                    "(kraken)|(wex)|(cryptsy)|(cexio)|(gemini)|(quoine)|(liquid)|(bitflyer)|"+
                    "(okcoin)|(796)|(bitvc)|(btc-china)|(bitmex)|(mexbt)|(huobi)|"+
                    "(vault-of-satoshi)|(luno)|(poloniex)|(mtgox)|(bisq)|(bithumb)|(bittrex)|"+
                    "(quadriga)|(binance)|(zonda)|(okx)|(coinone)|(hitbtc)|(kraken-futures)|"+
                    "(bitz)|(gateio)|(binance-us)|(dex-aggregated)|(ftx)|(deribit)|(uniswap-v2)|"+
                    "(ftx-us)|(kucoin):.*"
                    }
            },
            "cursor": {
                "type": "object",
                "properties": {
                    "last": {"type": "string"},
                    "hasMore": {"type": "boolean"}
                }
            },
            "allowance": {
                "type": "object",
                "properties": {
                    "cost": {"type": "number"},
                    "remaining": {"type": "number"},
                    "remainingPaid": {"type": "number"},
                    "account": {"type": "string"},
                    "upgrade": {"type": "string"}
                }
            }
        }
    }
    validate(instance=response_body, schema=schema)

def test_all_market_prices_endpoint_result_data():
    """Tests the result data using regex"""
    results = response_body["result"]
    for result in results:
        assert re.match(".*:.*:.*", result)
        assert re.match("[0-9.]+", str(results[result]))

route.test_cursor_data(response_body=response_body)

route.test_allowance_data(response_body=response_body)

def test_all_market_prices_endpoint_wrong_endpoint():
    """Negative test for checking incorrect endpoint address"""
    route2 = Route(endpoint="markets")
    resp = requests.get(route2.get_all_market_prices_url() + "s", headers={"X-CW-API-Key": route2.api_key})
    resp_body = resp.json()
    assert resp.status_code == 404
    assert resp_body["error"] == "Exchange not found"

def test_list_all_markets_endpoint_params():
    """Tests the parameters"""
    # First request
    params1 = {"limit": 10}
    resp1 = requests.get(route.get_endpoint_url(), headers={"X-CW-API-Key": route.api_key}, params=params1)
    resp_body1 = resp1.json()
    assert len(resp_body1["result"]) == 10
    for i in range(10):
        assert resp_body1["result"][i]["id"] == (i + 1)
    # Second request
    params2 = {"limit": 10, "cursor": resp_body1["cursor"]["last"]}
    resp2 = requests.get(route.get_endpoint_url(), headers={"X-CW-API-Key": route.api_key}, params=params2)
    resp_body2 = resp2.json()
    assert len(resp_body2["result"]) == 10
    for i in range(10):
        assert resp_body2["result"][i]["id"] == (i + 11)
