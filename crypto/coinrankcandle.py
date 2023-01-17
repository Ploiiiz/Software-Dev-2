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
# import coinrankingLine
from coinrankingLine import line
from coinranking import data

# def d_tick (p):
#     if p == "hour":
#         dTick = 200
#     elif p == "minute":
#         dTick = 40
#     elif p == "day":
#         dTick = 500
#     elif p == "week":
#         dTick = 1000
#     elif p == "month":
#         dTick = 5000

#     return dTick
    


a = 'BTC'

# # a = input('Symbol: ')

uuid = search(a)
# print(uuid)
# Connect to the database
conn = sqlite3.connect("coinranking.db")

# Create a cursor
cursor = conn.cursor()
# Set the API key in the request header
headers = header.headers

# Make a request to the Coinranking API
url = "https://coinranking1.p.rapidapi.com/coin/" + uuid + "/ohlc"
# url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/ohlc"
params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","interval":"hour", "limit":"168"}
response = requests.get(url, params=params, headers=headers)

p = params["interval"]
# print(params["interval"])


# Check the status code of the response
if response.status_code != 200:
    print("Error: Could not retrieve data from Coinranking API")
    exit()


data = json.loads(response.text)
# print(data)


df = pd.DataFrame(data["data"]["ohlc"])
df["startingAt"] = df["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
df["endingAt"] = df["endingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))

# Save the DataFrame to a table in the database

df.to_excel('coinrankingohlc.xlsx', sheet_name= a , index=True)

cryt = pd.read_excel('coinrankingohlc.xlsx')


cryt.to_sql("ohlc" + a , conn, if_exists="replace")

# Create a candlestick plot of the price data

query = "SELECT * FROM ohlc" + a

db = pd.read_sql_query(query, conn)


candlestick = go.Candlestick(
    x=db["startingAt"],
    open=db["open"],
    high=db["high"],
    low=db["low"],
    close=db["close"]
)
can = go.Figure(candlestick)
can.update_yaxes() #เปลี่ยนตาม intervals 
can.show()
line_g = line(uuid)
linee = go.Figure(line_g)

linee.show()

# Create a figure with 2 subplots
# fig = make_subplots(rows=2, cols=1)
fig = make_subplots(specs=[[{"secondary_y": True}]]) #ซ้อนในกราฟเดียวกัน

fig.add_trace(candlestick,
)
            # row=1, col=1)


fig.add_trace(line_g,
secondary_y=True)
# row = 2 , col = 1)



# Create the figure and show the plot
fig.update_layout(title='Candle and Line Graphs',xaxis_rangeslider_visible=False)

# fig = go.Figure(candlestick)
fig.show()

conn.close()
# line(uuid)


