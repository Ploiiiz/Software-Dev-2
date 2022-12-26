import requests

url = "https://coinmarketcapzakutynskyv1.p.rapidapi.com/getCryptocurrenciesList"

payload = "start=1&limit=20"
headers = {
	"content-type": "application/x-www-form-urlencoded",
	"X-RapidAPI-Key": "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0",
	"X-RapidAPI-Host": "CoinMarketCapzakutynskyV1.p.rapidapi.com"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)