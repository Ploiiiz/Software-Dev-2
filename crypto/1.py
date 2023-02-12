import requests
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json

import datetime
from searchdata import CoinRankingSearch


# class CoinRankingGraphs:
#     def __init__(self,symbol):        
#         self.uuid = search(symbol)
#         # self.db = None
#         # self.candlestick = None
#         # self.line = None
#         # self.fig = None
        
#     # def get_uuid(self):
#     #     self.uuid = search(self.symbol)
    
#     def connect_to_database(self):
#         self.conn = sqlite3.connect("coinranking.db")
#         self.cursor = self.conn.cursor()
    
#     def fetch_data(self):
#         headers = header.headers
#         url = "https://coinranking1.p.rapidapi.com/coin/" + self.uuid + "/ohlc"
#         params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","interval":"hour", "limit":"168"}
#         response = requests.get(url, params=params, headers=headers)

#         if response.status_code != 200:
#             print("Error: Could not retrieve data from Coinranking API")
#             exit()

#         data = json.loads(response.text)
#         self.df = pd.DataFrame(data["data"]["ohlc"])
#         self.df["startingAt"] = self.df["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
#         self.df["endingAt"] = self.df["endingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))

#     def save_to_excel(self):
#         self.df.to_excel('coinrankingohlc.xlsx', sheet_name= self.symbol, index=True)

#     def save_to_sql(self):
#         self.df.to_sql("ohlc" + self.symbol, self.conn, if_exists="replace")

#     def retrieve_from_sql(self):
#         query = "SELECT * FROM ohlc" + self.symbol
#         self.db = pd.read_sql_query(query, self.conn)

#     def create_candlestick(self):
#         self.candlestick = go.Candlestick(
#             x=self.db["startingAt"],
#             open=self.db["open"],
#             high=self.db["high"],
#             low=self.db["low"],
#             close=self.db["close"]
#         )
        
#     def create_line(self):
#         self.line = line(self.uuid)
        
#     def create_fig(self):
#         self.fig = make_subplots(specs=[[{"secondary_y": True}]])
#         self.fig.add_trace(self.candlestick)
#         self.fig.add_trace(self.line, secondary_y=True)
#         self.fig.update_layout(title='Candle and Line Graphs',xaxis_rangeslider_visible=False)

#     def show_fig(self):
#         self.fig.show()

#     def close_conn(self):
#         self.conn.close()

# data = CoinRankingGraphs('BTC')
def test_get_uuid():
        expected_uuid = "Qwsogvtv82FCd"
        # search = CoinRankingSearch("BTC")
        # search.uuid = "test_uuid"
        # self.assertEqual(search.get_uuid(), "test_uuid")

        search = CoinRankingSearch("BTC")
        search.data()
        search_uuid = search.get_uuid()
        print("expected_uuid:", expected_uuid)
        print("search_uuid:", search_uuid)

test_get_uuid()