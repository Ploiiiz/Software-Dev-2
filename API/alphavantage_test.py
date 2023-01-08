import requests
import csv

url = "https://alpha-vantage.p.rapidapi.com/query"

querystring = {	#"interval":"1min",
				"function":"TIME_SERIES_DAILY_ADJUSTED",
				"symbol":"AAPL",
				"outputsize":"compact",
				"datatype":"csv",
				"slice":"year2month12"}

headers = {
	"X-RapidAPI-Key": "b64fde5ed3msh355fc42f993b1f3p198029jsn81999cd42ee8",
	"X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

# with open('avant.csv','w') as m:
# 	m.write(response.content.decode('utf-8'))
decoded_content = response.content.decode('utf-8')
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
my_list = list(cr)
with open('alphavantage_apple_daily_compact.csv','w') as m:
	for row in my_list:
		m.write(','.join(row))
		m.write('\n')
	