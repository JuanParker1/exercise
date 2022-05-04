"""This module is testing the order book for a given market endpoint"""
import re
import requests
from jsonschema import validate
from resources.cwtest import Route

headers={"X-CW-API-Key":"ID9AJPGQ0ZNPZLSG2ML0"}

route = Route(endpoint="markets", exchange="kraken", pair="btcusd")
response = requests.get(route.get_order_book_url(), headers=headers)
response_body = response.json()

def test_order_book_endpoint_status_code():
    """Tests that the status code is 200 OK"""
    assert response.status_code == 200

def test_order_book_endpoint_headers():
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

def test_order_book_endpoint_against_schema():
    """Verifying that the returned body is correct using a schema"""
    schema = {
        "type": "object",
        "properties": {
            "result": {
                "type": "object",
                "properties": {
                    "asks": {"type": "array"},
                    "bids": {"type": "array"},
                    "seqNum": {"type": "integer"}
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
    for items in result["asks"]:
        for item in items:
            assert re.match("([0-9.])+", str(item))
    for items in result["bids"]:
        for item in items:
            assert re.match("([0-9.])+", str(item))
    assert re.match("([0-9.])+", str(result["seqNum"]))

route.test_allowance_data(response_body=response_body)

def test_order_book_endpoint_wrong_endpoint():
    """Negative test for checking incorrect endpoint address"""
    route2 = Route(endpoint="markets", exchange="kraken", pair="btcusd")
    resp = requests.get(route2.get_order_book_url() + "s", headers=headers)
    resp_body = resp.json()
    assert resp.status_code == 404
    assert resp_body["error"] == "Route not found"

def test_order_book_limit_param():
    """Tests that limit parameter works as expected"""
    params={"limit": 10}
    route2 = Route(endpoint="markets", exchange="kraken", pair="btcusd")
    resp = requests.get(route2.get_order_book_url(), params=params, headers=headers)
    resp_body = resp.json()
    assert len(resp_body["result"]["asks"]) == 10
    assert len(resp_body["result"]["bids"]) == 10

def test_order_book_depth_param():
    """Tests that depth parameter works as expected"""
    orderbook_depths = [2, 4, 6, 8, 10, 15, 20]
    for orderbook_depth in orderbook_depths:
        params={"depth": orderbook_depth}
        route2 = Route(endpoint="markets", exchange="kraken", pair="btcusd")
        resp = requests.get(route2.get_order_book_url(), params=params, headers=headers)
        resp_body = resp.json()
        # Checking asks values
        returned_obd_asks = 0
        for item in resp_body["result"]["asks"]:
            returned_obd_asks += item[1]
        assert orderbook_depth <= returned_obd_asks
        # Checking bids values
        returned_obd_bids = 0
        for item in resp_body["result"]["bids"]:
            returned_obd_bids += item[1]
        assert orderbook_depth <= returned_obd_bids

def test_order_book_span_param():
    """Tests that span parameter works as expected"""
    orderbook_spans = [0.1, 0.5, 0.8, 1, 2, 4, 6]
    for orderbook_span in orderbook_spans:
        params={"span": orderbook_span}
        route2 = Route(endpoint="markets", exchange="kraken", pair="btcusd")
        # Get the price first
        price_resp = requests.get(route2.get_pair_price_url(), headers=headers)
        price = price_resp.json()["result"]["price"]
        # Now get the order book with span param
        span_resp = requests.get(route2.get_order_book_url(), params=params, headers=headers)
        span_resp_body = span_resp.json()
        # Checking asks values
        compare_price = price * (1 + orderbook_span / 100) * (1 + 0.001)
        for item in span_resp_body["result"]["asks"]:
            assert compare_price >= item[0]
        # Checking bids values
        compare_price = price * (1 - orderbook_span / 100) * (1 - 0.001)
        for item in span_resp_body["result"]["bids"]:
            assert compare_price <= item[0]
