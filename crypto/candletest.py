import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

import unittest

# Unit test
class responseTest(unittest.TestCase):
    def test_getTest(self):
        result = getData()[0]
        assert result == 200
    
    def test_dataShapeTest(self):
        result = makeData(getData()).shape
        assert result == (100,7)

def getData():
    headers = {
        "X-RapidAPI-Key": "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }

    # Make a request to the Coinranking API
    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/ohlc"
    params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","interval":"month", "limit":"100"}
    response = requests.get(url, params=params, headers=headers)
    return (response.status_code,response.text)

def makeData(response):
    data = json.loads(response[1])
    df = pd.DataFrame(data["data"]["ohlc"])
    #df["startingAt"] = df["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
    return df

# Set the API key in the request header


# Check the status code of the response
# if response.status_code != 200:
#     print("Error: Could not retrieve data from Coinranking API")
#     exit()



# print(makeData(getData()).shape)

if __name__ == '__main__':
    unittest.main()