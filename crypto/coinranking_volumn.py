import requests
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json

import datetime
import header
import sqlite3
import coinrankcandle

conn = sqlite3.connect("coinranking.db")

# Create a cursor
cursor = conn.cursor()

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/"
# ?vs_currency=usd&days=1&interval=hourly
querystring = {"vs_currency":"usd","days":"1" , "interval" : "hourly"}# interval : days minite(5 min) hourly

# headers = header.headers_CoinGecko

response = requests.request("GET", url, 
params=querystring)

if response.status_code != 200:
    print("Error: Could not retrieve data from CoinGecko API")
    exit()


data = json.loads(response.text)

# print(data)


df = pd.DataFrame(data["total_volumes"])
df[0] = df[0].sort_values(ascending=True)
df[0] = df[0].apply(lambda x: datetime.datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M'))

df.to_excel('coinGecko.xlsx', sheet_name='volumn', index=True)

cryt = pd.read_excel('coinGecko.xlsx')


cryt.to_sql("coinGeckoVolumn", conn, if_exists="replace")

# Create a candlestick plot of the price data

db = pd.read_sql_query("SELECT * FROM coinGeckoVolumn", conn)

bar = go.Bar(x=df[0], y=df[1])
bar_show = go.Figure(bar)
bar_show.show()

# Create a figure with 2 subplots
# fig = make_subplots(rows=2, cols=1)
fig_ = make_subplots(specs=[[{"secondary_y": True}]]) #ซ้อนในกราฟเดียวกัน

# fig_.add_trace(coinrankcandle.candlestick,)
#             row=1, col=1)


fig_.add_trace(bar,
secondary_y=True)
# row = 2 , col = 1)



# # Create the figure and show the plot
fig_.update_layout(title='',xaxis_rangeslider_visible=False)

# # fig = go.Figure(candlestick)
# fig_.show()

conn.close()
# print(df)