"""This module is testing the information about the market endpoint"""
import re
import requests
from jsonschema import validate
from resources.cwtest import Route

route = Route(endpoint="markets", exchange="kraken", pair="ethusd")
response = requests.get(route.get_pair_url(), headers={"X-CW-API-Key": route.api_key})
response_body = response.json()

def test_information_about_the_market_exchange_pair_endpoint_status_code():
    """Tests that the status code is 200 OK"""
    assert response.status_code == 200

def test_information_about_the_market_exchange_pair_endpoint_headers():
    """Verifying that headers are present (verifying based on requirements)."""
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Connection"] == "keep-alive"
    keys = ["Date", "Content-Type", "Content-Length",
            "Connection", "Access-Control-Allow-Headers",
            "Content-Encoding", "Referrer-Policy", "Vary",
            "X-Content-Type-Options", "CF-Cache-Status",
            "Expect-CT", "Set-Cookie", "Strict-Transport-Security",
            "Server", "CF-RAY"]
    for k in keys:
        if k not in response.headers:
            assert False, "'" + k + "' is not in Headers keys"

def test_information_about_the_market_exchange_pair_endpoint_against_schema():
    """Verifying that the returned body is correct using a schema"""
    schema = {
        "type": "object",
        "properties": {
            "result": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "exchange": {"type": "string"},
                    "pair": {"type": "string"},
                    "active": {"type": "boolean"},
                    "routes": {
                        "type": "object",
                        "properties": {
                            "price": {"type": "string"},
                            "summary": {"type": "string"},
                            "orderbook": {"type": "string"},
                            "trades": {"type": "string"},
                            "ohlc": {"type": "string"}
                        },
                    }
                },
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

def test_information_about_the_market_exchange_pair_endpoint_result_data():
    """Tests the result data using regex"""
    result = response_body["result"]
    assert re.match("[0-9]+", str(result["id"]))
    assert result["exchange"] == "kraken"
    assert result["pair"] == "ethusd"
    assert re.match("(True)|(False)", str(result["active"]))
    routes = ["price", "summary", "orderbook", "trades", "ohlc"]
    for rout in routes:
        assert result["routes"][rout] == "https://api.cryptowat.ch/markets/kraken/ethusd/" + rout

route.test_allowance_data(response_body=response_body)

def test_information_about_the_market_exchange_pair_wrong_endpoint():
    """Negative test for checking incorrect endpoint address"""
    route2 = Route(endpoint="markets", exchange="kraken", pair="asdfusd")
    resp = requests.get(route2.get_pair_url(), headers={"X-CW-API-Key": route2.api_key})
    resp_body = resp.json()
    assert resp.status_code == 404
    assert resp_body["error"] == "Instrument not found"
