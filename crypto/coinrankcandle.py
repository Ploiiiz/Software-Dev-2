import requests
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json

import datetime
import header
import sqlite3

# import searchdata
from searchdata import search
import coinrankingLine
from coinrankingLine import line
from coinranking import data


# a = input('Symbol: ')
# uuid = search(a)
uuid = search("BTC")
# Connect to the database
conn = sqlite3.connect("coinranking.db")

# Create a cursor
cursor = conn.cursor()
# Set the API key in the request header
headers = header.headers

# Make a request to the Coinranking API
url = "https://coinranking1.p.rapidapi.com/coin/" + uuid + "/ohlc"
# url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/ohlc"
params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","interval":"hour", "limit":"100"}
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

# candlestick = go.Figure(go.Candlestick(
#     x=db["startingAt"],
#     open=db["open"],
#     high=db["high"],
#     low=db["low"],
#     close=db["close"]
# ))
candlestick = go.Candlestick(
    x=db["startingAt"],
    open=db["open"],
    high=db["high"],
    low=db["low"],
    close=db["close"]
)
can = go.Figure(candlestick)
# can.show()
line_g = line(uuid)
linee = go.Figure(line_g)

# linee.show()

# Create a figure with 2 subplots
fig = make_subplots(rows=2, cols=1)

fig.add_trace(candlestick,
            row=1, col=1)


fig.add_trace(line_g,row = 2 , col = 1)



# Create the figure and show the plot
fig.update_layout(title='Candle and Line Graphs',xaxis_rangeslider_visible=False)
# fig = go.Figure(candlestick)
fig.show()

conn.close()
# line(uuid)


