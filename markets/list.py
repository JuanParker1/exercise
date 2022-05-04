"""This module is testing the list all markets endpoint"""
import re
import requests
from jsonschema import validate
from resources.cwtest import Route

route = Route("markets")
response = requests.get(route.get_endpoint_url(), headers={"X-CW-API-Key": route.api_key})
response_body = response.json()

def test_list_all_markets_endpoint_status_code():
    """Tests that the status code is 200 OK"""
    assert response.status_code == 200

def test_list_all_markets_endpoint_headers():
    """Verifying that headers are present (verifying based on requirements)."""
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Transfer-Encoding"] == "chunked"
    assert response.headers["Connection"] == "keep-alive"
    keys = ["Date", "Content-Type", "Transfer-Encoding",
            "Connection", "Access-Control-Allow-Headers",
            "Content-Encoding", "Referrer-Policy", "Vary",
            "X-Content-Type-Options", "CF-Cache-Status",
            "Expect-CT", "Set-Cookie", "Strict-Transport-Security",
            "Server", "CF-RAY"]
    for k in keys:
        if k not in response.headers:
            assert False, "'" + k + "' is not in Headers keys"

def test_list_all_markets_endpoint_against_schema():
    """Verifying that the returned body is correct using a schema"""
    schema = {
        "type": "object",
        "properties": {
            "result": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "number"},
                        "exchange": {"type": "string"},
                        "pair": {"type": "string"},
                        "active": {"type": "boolean"},
                        "route": {"type": "string"}
                    }
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

def test_list_all_markets_endpoint_result_data():
    """Tests the result data using regex"""
    for obj in response_body["result"]:
        assert re.match("[0-9]+", str(obj["id"]))
        assert re.match("(bitfinex)|(coinbase-pro)|(bitstamp)|(kraken)|(wex)|(cryptsy)|(cexio)|"+
                        "(gemini)|(quoine)|(liquid)|(bitflyer)|(okcoin)|(796)|(bitvc)|(btc-china)|"+
                        "(bitmex)|(mexbt)|(huobi)|(vault-of-satoshi)|(luno)|(poloniex)|(mtgox)|"+
                        "(bisq)|(bithumb)|(bittrex)|(quadriga)|(binance)|(zonda)|(okx)|(coinone)|"+
                        "(hitbtc)|(kraken-futures)|(bitz)|(gateio)|(binance-us)|(dex-aggregated)|"+
                        "(ftx)|(deribit)|(uniswap-v2)|(ftx-us)|(kucoin)", str(obj["exchange"]))
        assert re.match("([0-9a-z])+", str(obj["pair"]))
        assert re.match("(True)|(False)", str(obj["active"]))
        assert re.match("https://api.cryptowat.ch/markets/*/*", str(obj["route"]))

route.test_cursor_data(response_body=response_body)

route.test_allowance_data(response_body=response_body)

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

def test_list_all_markets_endpoint_wrong_params():
    """Negative test for the parameters"""
    params = {"cursor": "asdf"}
    resp = requests.get(route.get_endpoint_url(), headers={"X-CW-API-Key": route.api_key}, params=params)
    resp_body = resp.json()
    assert resp.status_code == 400
    assert resp_body["error"] == "Invalid input"

def test_list_all_markets_wrong_endpoint():
    """Negative test for checking incorrect endpoint address"""
    route2 = Route("marketss")
    resp = requests.get(route2.get_endpoint_url(), headers={"X-CW-API-Key": route2.api_key})
    resp_body = resp.json()
    assert resp.status_code == 404
    assert resp_body["error"] == "Route not found"
