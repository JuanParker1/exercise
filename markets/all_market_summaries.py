"""This module is testing the 24-hour summary for every market on the platform endpoint"""
import re
import requests
from jsonschema import validate
from resources.cwtest import Route

route = Route(endpoint="markets", exchange="kraken", pair="ltcusd")
response = requests.get(route.get_all_market_summaries_url(), headers={"X-CW-API-Key": route.api_key})
response_body = response.json()

def test_all_market_summaries_endpoint_status_code():
    """Tests that the status code is 200 OK"""
    assert response.status_code == 200

def test_all_market_summaries_endpoint_headers():
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

def test_all_market_summaries_endpoint_against_schema():
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

def test_all_market_summaries_endpoint_result_data():
    """Tests the result data using regex"""
    results = response_body["result"]
    for result in results:
        assert re.match(".*:.*", result)
        assert re.match("[0-9.]+", str(results[result]["price"]["last"]))
        assert re.match("[0-9.]+", str(results[result]["price"]["high"]))
        assert re.match("[0-9.]+", str(results[result]["price"]["low"]))
        assert re.match("-?[0-9.]+", str(results[result]["price"]["change"]["percentage"]))
        assert re.match("-?[0-9.]+", str(results[result]["price"]["change"]["absolute"]))
        assert re.match("[0-9.]+", str(results[result]["volume"]))
        assert re.match("[0-9.]+", str(results[result]["volumeQuote"]))

route.test_cursor_data(response_body=response_body)

route.test_allowance_data(response_body=response_body)

def test_all_market_summaries_endpoint_wrong_endpoint():
    """Negative test for checking incorrect endpoint address"""
    route2 = Route(endpoint="markets")
    resp = requests.get(route2.get_all_market_summaries_url() + "s", headers={"X-CW-API-Key": route2.api_key})
    resp_body = resp.json()
    assert resp.status_code == 404
    assert resp_body["error"] == "Exchange not found"

def test_all_market_summaries_keyby_param():
    """Tests the keyBy parameter for all market summaries endpoint"""
    # Check keyBy: id
    params={"keyBy": "id"}
    route1 = Route(endpoint="markets", exchange="kraken", pair="ltcusd")
    resp1 = requests.get(route1.get_all_market_summaries_url(), headers={"X-CW-API-Key": route1.api_key}, params=params)
    resp_body1 = resp1.json()
    for item in resp_body1["result"]:
        assert re.match("[0-9]+", item)
    # Check keyBy: symbol
    params={"keyBy": "symbols"}
    route2 = Route(endpoint="markets", exchange="kraken", pair="ltcusd")
    resp2 = requests.get(route2.get_all_market_summaries_url(), headers={"X-CW-API-Key": route2.api_key}, params=params)
    resp_body2 = resp2.json()
    for item in resp_body2["result"]:
        assert re.match(".*:.*", item)
    # Check unknown keyBy param
    params={"keyBy": "asdf"}
    route2 = Route(endpoint="markets", exchange="kraken", pair="ltcusd")
    resp2 = requests.get(route2.get_all_market_summaries_url(), headers={"X-CW-API-Key": route2.api_key}, params=params)
    resp_body2 = resp2.json()
    assert resp2.status_code == 400
    assert resp_body2["error"] == "Unkown sort parameter"

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
