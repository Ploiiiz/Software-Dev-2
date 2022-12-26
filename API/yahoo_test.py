import requests

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/auto-complete"

querystring = {"q":"tesla","region":"US"}

headers = {
	"X-RapidAPI-Key": "b64fde5ed3msh355fc42f993b1f3p198029jsn81999cd42ee8",
	"X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)