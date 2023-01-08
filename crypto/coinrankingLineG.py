import requests
import pandas as pd
import plotly.graph_objects as go
import json
import datetime
import plotly.express as px
# Set the API key in the request header
headers = {
	"X-RapidAPI-Key": "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0",
	"X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
}


# Make a request to the Coinranking API
url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h"}
response = requests.get(url, params=params, headers=headers)

# Check the status code of the response
if response.status_code != 200:
    print("Error: Could not retrieve data from Coinranking API")
    exit()

data = json.loads(response.text)
df = pd.DataFrame(data["data"]["history"])

# Store the coin data in a DataFrame


df['timestamp']= df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))
df.to_excel('coinrankingline.xlsx', sheet_name='line', index=True)


# Create a line chart
cryt = pd.read_excel('coinrankingline.xlsx')
fug = px.line(data_frame=cryt ,x = 'timestamp',y = 'price')

# Create the figure and show the plot

fug.show()
