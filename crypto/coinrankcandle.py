import requests
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
import datetime
import header
import sqlite3
# from searchdata import CoinRankingSearch

class CoinRankingOHLC:
    def __init__(self, uuid, interval, limit, symbol,name):
        self.uuid = uuid
        self.name = name 
        self.interval = interval
        self.limit = limit
        self.symbol = symbol
        self.headers = header.headers
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(self.uuid) + "/ohlc"
        self.params = {"referenceCurrencyUuid":"yhjMzLPhuIDl", "interval":self.interval, "limit":self.limit}

    


        
    def retrieve_data(self):
        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
        data = json.loads(response.text)
        self.df = pd.DataFrame(data["data"]["ohlc"])
        self.df["startingAt"] = self.df["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
        self.df["endingAt"] = self.df["endingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
               


    
          
        
            
    def save_to_excel(self):
        self.df.to_excel('coinrankingohlc.xlsx', sheet_name= self.symbol + "_" + self.interval , index=True)
        
    def show_candlestick(self):
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval
        db = pd.read_sql_query(query, self.conn)
        candlestick = go.Candlestick(
            x=db["startingAt"],
            open=db["open"],
            high=db["high"],
            low=db["low"],
            close=db["close"],            
        )
        can = go.Figure(candlestick)
        can.update_layout(title=self.name + " " + "(" + self.symbol + ")")
        can.update_yaxes() # update the y-axis according to the interval
        can.show()
        
    def close_connection(self):
        self.conn.close()
        
# if __name__ == "__main__":
    # cr = CoinRankingOHLC("Qwsogvtv82FCd", "hour", "168")
    # cr.get_symbol()
#     cr = CoinRankingOHLC(uuid, interval, limit)
#     # cr.retrieve_data()
#     # cr.save_to_database()
#     # cr.save_to_excel()
#     # cr.show_candlestick()
#     # cr.close_connection()
