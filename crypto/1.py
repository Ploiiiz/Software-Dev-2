import requests
import header
import json
import pandas as pd


url = "https://api.coinpaprika.com/v1/coins/btc-bitcoin/ohlcv/historical"

headers = header.headers_CoinPaprika

response = requests.request("GET", url, headers=headers)

print(response.text)