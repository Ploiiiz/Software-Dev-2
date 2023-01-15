import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import header
import datetime

import sqlite3

import searchdata
from searchdata import search
import coinrankingLine
from coinrankingLine import line


# a = input('Symbol: ')
# uuid = search(a)

# Connect to the database
conn = sqlite3.connect("coinranking.db")

# Create a cursor
cursor = conn.cursor()
# Set the API key in the request header
headers = header.headers

# Make a request to the Coinranking API
# url = "https://coinranking1.p.rapidapi.com/coin/" + uuid + "/ohlc"
url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/ohlc"
params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","interval":"day", "limit":"100"}
response = requests.get(url, params=params, headers=headers)




# Check the status code of the response
if response.status_code != 200:
    print("Error: Could not retrieve data from Coinranking API")
    exit()


data = json.loads(response.text)
# print(data)


df = pd.DataFrame(data["data"]["ohlc"])
df["startingAt"] = df["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
    
# print(df)
# Save the DataFrame to a table in the database


df.to_excel('coinrankingohlc.xlsx', sheet_name='ohlc', index=True)

cryt = pd.read_excel('coinrankingohlc.xlsx')


cryt.to_sql("coinrankingcandle", conn, if_exists="replace")

# Create a candlestick plot of the price data

db = pd.read_sql_query("SELECT * FROM coinrankingcandle", conn)
candlestick = go.Candlestick(
    x=db["startingAt"],
    open=db["open"],
    high=db["high"],
    low=db["low"],
    close=db["close"]
)

# Create the figure and show the plot
fig = go.Figure(candlestick)
fig.show()

conn.close()
# line(uuid)

