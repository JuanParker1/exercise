"""This module is testing the market's last price endpoint"""
import re
import requests
from jsonschema import validate
from resources.cwtest import Route

route = Route(endpoint="markets", exchange="kraken", pair="etheur")
response = requests.get(route.get_market_summary_url(), headers={"X-CW-API-Key": route.api_key})
response_body = response.json()

def test_markets_last_price_endpoint_status_code():
    """Tests that the status code is 200 OK"""
    assert response.status_code == 200

def test_markets_last_price_endpoint_headers():
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

def test_markets_last_price_endpoint_against_schema():
    """Verifying that the returned body is correct using a schema"""
    schema = {
        "type": "object",
        "properties": {
            "result": {
                "type": "object",
                "properties": {
                    "price": {
                        "type": "object",
                        "properties": {
                            "last": {"type": "number"},
                            "high": {"type": "number"},
                            "low": {"type": "number"},
                            "change": {
                                "type": "object",
                                "properties": {
                                    "percentage": {"type": "number"},
                                    "absolute": {"type": "number"}
                                }
                            }
                        }
                    },
                    "volume": {"type": "number"},
                    "volumeQuote": {"type": "number"}
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

def test_markets_last_price_endpoint_result_data():
    """Tests the result data using regex"""
    result = response_body["result"]
    assert re.match("[0-9.]+", str(result["price"]["last"]))
    assert re.match("[0-9.]+", str(result["price"]["high"]))
    assert re.match("[0-9.]+", str(result["price"]["low"]))
    assert re.match("-?[0-9.]+", str(result["price"]["change"]["percentage"]))
    assert re.match("-?[0-9.]+", str(result["price"]["change"]["absolute"]))
    assert re.match("[0-9.]+", str(result["volume"]))
    assert re.match("[0-9.]+", str(result["volumeQuote"]))

route.test_allowance_data(response_body=response_body)

def test_markets_last_price_endpoint_wrong_endpoint():
    """Negative test for checking incorrect endpoint address"""
    route2 = Route(endpoint="markets", exchange="kraken", pair="btcusd")
    resp = requests.get(route2.get_market_summary_url() + "s", headers={"X-CW-API-Key": route2.api_key})
    resp_body = resp.json()
    assert resp.status_code == 404
    assert resp_body["error"] == "Route not found"
