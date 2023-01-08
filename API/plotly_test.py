import pandas

with open('alphavantage_apple_daily_full.csv') as file:
    data = pandas.read_csv(file)

import plotly.graph_objects as go

from datetime import datetime

fig = go.Figure(data=[go.Candlestick(x=data['timestamp'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'])])

fig.show()   