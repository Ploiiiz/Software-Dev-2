import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

import datetime
# Set the API key in the request header
headers = {
	"X-RapidAPI-Key": "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0",
	"X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
}

# Make a request to the Coinranking API
url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/ohlc"
params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","interval":"month", "limit":"100"}
response = requests.get(url, params=params, headers=headers)

import datetime



# Check the status code of the response
if response.status_code != 200:
    print("Error: Could not retrieve data from Coinranking API")
    exit()


data = json.loads(response.text)
# print(data)


df = pd.DataFrame(data["data"]["ohlc"])
df["startingAt"] = df["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
  
print(df)
df.to_excel('coinrankingohlc.xlsx', sheet_name='ohlc', index=True)


# Create a candlestick plot of the price data
candlestick = go.Candlestick(
    x=df["startingAt"],
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"]
)

# Create the figure and show the plot
fig = go.Figure(candlestick)
fig.show()

