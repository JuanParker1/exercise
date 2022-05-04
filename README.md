# REST API Testing Exercise
This exercise is testing the markets endpoints using `pytest` and `requests` modules.

## Used versions:
* Python: 3.10.4
* requests module: 2.27.1
* jsonschema module: 4.4.0
* pytest modyke: 7.1.2

## Usage:
On windows execute the following command from the root folder:
`pytest .\markets\all_market_prices.py .\markets\all_market_summaries.py .\markets\details_exchange.py .\markets\details_pair.py .\markets\list.py .\markets\market_price.py .\markets\market_summary.py .\markets\ohlc.py .\markets\orderbook.py .\markets\orderbook_calculator.py .\markets\orderbook_liquidity.py .\markets\trades.py`

## Example execution in Powershell:
```
PS C:\dev\rest_api_exercise> pytest .\markets\all_market_prices.py .\markets\all_market_summari
es.py .\markets\details_exchange.py .\markets\details_pair.py .\markets\list.py .\markets\marke
t_price.py .\markets\market_summary.py .\markets\ohlc.py .\markets\orderbook.py .\markets\order
book_calculator.py .\markets\orderbook_liquidity.py .\markets\trades.py
===================================== test session starts =====================================
platform win32 -- Python 3.10.4, pytest-7.1.2, pluggy-1.0.0
rootdir: C:\dev\rest_api_exercise
plugins: html-3.1.1, metadata-2.0.1
collected 60 items

markets\all_market_prices.py ......                                                      [ 10%]
markets\all_market_summaries.py .......                                                  [ 21%]
markets\details_exchange.py .....                                                        [ 30%]
markets\details_pair.py .....                                                            [ 38%]
markets\list.py .......                                                                  [ 50%]
markets\market_price.py .....                                                            [ 58%]
markets\market_summary.py .....                                                          [ 66%]
markets\orderbook.py ........                                                            [ 80%]
markets\orderbook_liquidity.py .....                                                     [ 88%]
markets\trades.py .......                                                                [100%]

===================================== 60 passed in 20.01s ===================================== 
PS C:\dev\rest_api_exercise> 
```
