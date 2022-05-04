"""This module is testing the order book liquidity for a given market endpoint"""
import re
import requests
from jsonschema import validate
from resources.cwtest import Route

route = Route(endpoint="markets", exchange="kraken", pair="btcusd")
response = requests.get(route.get_order_book_liq_url(), headers={"X-CW-API-Key": route.api_key})
response_body = response.json()

def test_order_book_liquidity_endpoint_status_code():
    """Tests that the status code is 200 OK"""
    assert response.status_code == 200

def test_order_book_liquidity_endpoint_headers():
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

def test_order_book_liquidity_endpoint_against_schema():
    """Verifying that the returned body is correct using a schema"""
    schema = {
        "type": "object",
        "properties": {
            "result": {
                "type": "object",
                "properties": {
                    "ask": {
                        "type": "object",
                        "properties": {
                            "base": {"type": "object"},
                            "quote": {"type": "object"}
                        }
                    },
                    "bid": {
                        "type": "object",
                        "properties": {
                            "base": {"type": "object"},
                            "quote": {"type": "object"}
                        }
                    },
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

def test_order_book_endpoint_result_data():
    """Tests the result data using regex"""
    result = response_body["result"]
    for item in result["bid"]["base"]:
        assert re.match("([0-9.])+", str(result["bid"]["base"][item]))
    for item in result["bid"]["quote"]:
        assert re.match("([0-9.])+", str(result["bid"]["quote"][item]))
    for item in result["ask"]["base"]:
        assert re.match("([0-9.])+", str(result["ask"]["base"][item]))
    for item in result["ask"]["quote"]:
        assert re.match("([0-9.])+", str(result["ask"]["quote"][item]))

route.test_allowance_data(response_body=response_body)

def test_order_book_endpoint_wrong_endpoint():
    """Negative test for checking incorrect endpoint address"""
    route2 = Route(endpoint="markets", exchange="kraken", pair="btcusd")
    resp = requests.get(route2.get_order_book_liq_url() + "s", headers={"X-CW-API-Key": route2.api_key})
    resp_body = resp.json()
    assert resp.status_code == 404
    assert resp_body["error"] == "Route not found"
