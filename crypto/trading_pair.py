import requests
import json

import requests

url = "https://coinmarketcapzakutynskyv1.p.rapidapi.com/getCryptocurrenciesList"

headers = {
	"X-RapidAPI-Key": "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0",
	"X-RapidAPI-Host": "CoinMarketCapzakutynskyV1.p.rapidapi.com"
}

response = requests.request("POST", url, headers=headers)

# print(response.text)
data = json.loads(response.text)

print(data)


# data = json.loads(response.text)

# for listing in data['data']:
#     symbol = listing['symbol']
#     for quote in listing['quote']:
#         pair = quote['symbol']
#         print(f"{symbol}/{pair}")
