"""This module is testing the most recent trades endpoint"""
import re
import time
import requests
from jsonschema import validate
from resources.cwtest import Route

route = Route(endpoint="markets", exchange="kraken", pair="btcusd")
headers = {"X-CW-API-Key": route.api_key}
response = requests.get(route.get_market_trades_url(), headers=headers)
response_body = response.json()

def test_market_trades_endpoint_status_code():
    """Tests that the status code is 200 OK"""
    assert response.status_code == 200

def test_market_trades_endpoint_headers():
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

def test_market_trades_endpoint_against_schema():
    """Verifying that the returned body is correct using a schema"""
    schema = {
        "type": "object",
        "properties": {
            "result": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {"type": "number"}
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

def test_market_trades_endpoint_result_data():
    """Tests the result data using regex"""
    for values in response_body["result"]:
        for value in values:
            assert re.match("([0-9.])+", str(value))

route.test_allowance_data(response_body=response_body)

def test_market_trades_endpoint_wrong_endpoint():
    """Negative test for checking incorrect endpoint address"""
    route2 = Route(endpoint="markets", exchange="kraken", pair="btcusd")
    headers2 = {"X-CW-API-Key": route2.api_key}
    resp = requests.get(route2.get_market_trades_url() + "s", headers=headers2)
    resp_body = resp.json()
    assert resp.status_code == 404
    assert resp_body["error"] == "Route not found"

def test_market_trades_since_param():
    """Tests that since parameter works as expected"""
    timestamp = int(time.time()) - 30
    params={"since": timestamp}
    route2 = Route(endpoint="markets", exchange="kraken", pair="btcusd")
    headers2 = {"X-CW-API-Key": route.api_key}
    resp = requests.get(route2.get_market_trades_url(), params=params, headers=headers2)
    resp_body = resp.json()
    for values in resp_body["result"]:
        assert values[1] >= timestamp

def test_market_trades_limit_param():
    """Tests that limit parameter works as expected"""
    params={"limit": 10}
    route2 = Route(endpoint="markets", exchange="kraken", pair="btcusd")
    headers2 = {"X-CW-API-Key": route.api_key}
    resp = requests.get(route2.get_market_trades_url(), params=params, headers=headers2)
    resp_body = resp.json()
    assert len(resp_body["result"]) == 10
