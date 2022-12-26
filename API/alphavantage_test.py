import requests

url = "https://alpha-vantage.p.rapidapi.com/query"

querystring = {"interval":"5min","function":"TIME_SERIES_INTRADAY","symbol":"MSFT","datatype":"json","output_size":"compact"}

headers = {
	"X-RapidAPI-Key": "b64fde5ed3msh355fc42f993b1f3p198029jsn81999cd42ee8",
	"X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)