import requests
import json
import pandas as pd

url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol=BTC&apikey=00IHK3KZ5SAJOUGE"

response = requests.get(url)

# print(response.json())

data = json.loads(response.text)
new_data = pd.DataFrame(data['feed']['ticker_sentiment'])
print(new_data)