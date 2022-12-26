# import requests

# url = "https://coinranking1.p.rapidapi.com/coins"

# querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h","tiers[0]":"1","orderBy":"marketCap","orderDirection":"desc","limit":"50","offset":"0"}

# headers = {
# 	"X-RapidAPI-Key": "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0",
# 	"X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)



import requests

url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/price"

querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl"}

headers = {
	"X-RapidAPI-Key": "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0",
	"X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)