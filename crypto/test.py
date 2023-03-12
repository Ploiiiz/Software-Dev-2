import requests
import json
import pandas as pd
import coinrankingLine as cl
# from datetime import datetime
import header
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime


headers = header.headers
url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":'24h'}
response = requests.get(url, params=params, headers=headers)
if response.status_code != 200:
    print("Error: Could not retrieve data from Coinranking API")
    exit()
data = json.loads(response.text)
# print(data["data"]["history"])
df = pd.DataFrame(data["data"]["history"]) 
df["price"] = pd.to_numeric(df["price"])
df['timestamp']= df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x)) 
df_price = df
# print(df_price)


url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol=BTC&apikey=00IHK3KZ5SAJOUGE"
response = requests.get(url)
data = json.loads(response.text)
new_data = pd.DataFrame(data)

feed_data = pd.DataFrame(data['feed'])
for i in range (len(feed_data['time_published'])):
    dt_obj = datetime.datetime.strptime(feed_data['time_published'][i], '%Y%m%dT%H%M%S')
    feed_data['time_published'][i] = dt_obj.strftime( '%Y-%m-%d %H:%M:%S')

# Create the figure
fig = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.02)

# Add the price data as a trace and set title for price graph
fig.add_trace(
    go.Scatter(x=df_price['timestamp'], y=df_price['price'], name="Price"),
    row=1, col=1
)
fig.update_yaxes(title_text="Price", row=1, col=1)
fig.update_layout(title_text="Price and Sentiment Analysis for Bitcoin")
fig.update_xaxes(range=[feed_data['time_published'].iloc[-1], feed_data['time_published'].iloc[0]], row=1, col=1)



# Add the sentiment scores as a trace and set title for sentiment score graph
fig.add_trace(
    go.Scatter(x=feed_data['time_published'], y=feed_data['overall_sentiment_score'], name="Sentiment Score"),
    row=2, col=1
)
fig.update_yaxes(title_text="Sentiment Score", row=2, col=1)

# Update the layout of the figure
fig.update_layout(
    xaxis_title="Date",
    legend=dict(
        x=0,
        y=1,
        bgcolor='rgba(255, 255, 255, 0.5)',
        bordercolor='rgba(0, 0, 0, 0)'
    ),
    plot_bgcolor='rgb(230, 230, 230)',
    height=800
)

# Show the figure
fig.show()

