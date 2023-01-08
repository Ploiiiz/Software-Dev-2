import requests
import pandas as pd
import plotly.graph_objects as go
import json
import datetime
import plotly.express as px

import unittest

# Unit test
class responseTest(unittest.TestCase):
    def test_json_data(self):
        response = get_data()
        try:
            data = json.loads(response.text)
        except:
            self.assertFalse("Invalid JSON data")

        assert response.status_code == 200, "API response error"

    def test_dataframe_columns(self):
        response = get_data()
        df = make_data(response)
        self.assertEqual(set(df.columns), {"startingAt", "open", "high", "low", "close"}, "Unexpected DataFrame columns")

    def test_datetime_column(self):
        response = get_data()
        df = make_data(response)
        try:
            df["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
        except:
            self.assertFalse("Invalid datetime in startingAt column")

    def test_plot_display(self):
        response = get_data()
        df = make_data(response)
        fig = plot(df)
        try:
            fig.show()
        except:
            self.assertFalse("Error displaying plot")



def get_data():

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
    
    return response

def make_data(response):
    get_data()
    data = json.loads(response.text)
    df = pd.DataFrame(data["data"]["history"])

    # Store the coin data in a DataFrame


    df['timestamp']= df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))
    df.to_excel('coinrankingline.xlsx', sheet_name='line', index=True)

    return df

def plot(fig):
    make_data()    
    # Create a line chart
    cryt = pd.read_excel('coinrankingline.xlsx')
    fig = px.line(data_frame=cryt ,x = 'timestamp',y = 'price')

    # Create the figure and show the plot

    fig.show()

    return fig.show()


if __name__ == '__main__':
    unittest.main()