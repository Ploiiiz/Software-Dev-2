import requests
import json
import pandas as pd

url = "https://coinranking1.p.rapidapi.com/reference-currencies"

querystring = {"limit":"50","offset":"0"}

headers = {
	"X-RapidAPI-Key": "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0",
	"X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
data = json.loads(response.text)
new_data = pd.DataFrame(data['data']["currencies"])


print(new_data)