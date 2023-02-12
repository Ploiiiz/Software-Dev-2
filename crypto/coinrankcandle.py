# import requests
# import pandas as pd
# import plotly.express as px
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
# import json

# import datetime
# import header
# import sqlite3

# # import searchdata
# from searchdata import CoinRankingSearch
# # import coinrankingLine
# from coinrankingLine import line
# from coinranking import data


# search = CoinRankingSearch("BTC")
# # search.data()
# uuid = search.get_uuid()
# print(str(uuid))
# # Connect to the database
# conn = sqlite3.connect("coinranking.db")

# # Create a cursor
# cursor = conn.cursor()
# # Set the API key in the request header
# headers = header.headers

# # Make a request to the Coinranking API
# # url = "https://coinranking1.p.rapidapi.com/coin/" + str(uuid) + "/ohlc"
# url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/ohlc"
# params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","interval":"hour", "limit":"168"}
# response = requests.get(url, params=params, headers=headers)

# p = params["interval"]
# # print(params["interval"])


# # Check the status code of the response
# if response.status_code != 200:
#     print("Error: Could not retrieve data from Coinranking API")
#     exit()


# data = json.loads(response.text)
# # print(data)


# df = pd.DataFrame(data["data"]["ohlc"])
# df["startingAt"] = df["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
# df["endingAt"] = df["endingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))

# # Save the DataFrame to a table in the database

# df.to_excel('coinrankingohlc.xlsx', sheet_name= "BTC" , index=True)

# cryt = pd.read_excel('coinrankingohlc.xlsx')


# cryt.to_sql("ohlc" + "BTC" , conn, if_exists="replace")

# # Create a candlestick plot of the price data

# query = "SELECT * FROM ohlc" + "BTC"

# db = pd.read_sql_query(query, conn)


# candlestick = go.Candlestick(
#     x=db["startingAt"],
#     open=db["open"],
#     high=db["high"],
#     low=db["low"],
#     close=db["close"]
# )
# can = go.Figure(candlestick)
# can.update_yaxes() #เปลี่ยนตาม intervals 
# can.show()
# # line_g = line(uuid)
# # linee = go.Figure(line_g)

# # linee.show()

# # Create a figure with 2 subplots
# # fig = make_subplots(rows=2, cols=1)
# # fig = make_subplots(specs=[[{"secondary_y": True}]]) #ซ้อนในกราฟเดียวกัน

# # fig.add_trace(candlestick,
# # )
#             # row=1, col=1)


# # fig.add_trace(line_g,
# # secondary_y=True)
# # row = 2 , col = 1)



# # Create the figure and show the plot
# # fig.update_layout(title='Candle and Line Graphs',xaxis_rangeslider_visible=False)

# # fig = go.Figure(candlestick)
# # fig.show()

# conn.close()
# # line(uuid)


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
    def __init__(self, uuid, interval, limit, symbol):
        self.uuid = uuid
        self.interval = interval
        self.limit = limit
        self.symbol = symbol
        self.headers = header.headers
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(self.uuid) + "/ohlc"
        self.params = {"referenceCurrencyUuid":"yhjMzLPhuIDl", "interval":self.interval, "limit":self.limit}

    # def get_symbol(self):
    #     self.symbol = CoinRankingSearch.get_symbol()


        
    def retrieve_data(self):
        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
        data = json.loads(response.text)
        self.df = pd.DataFrame(data["data"]["ohlc"])
        self.df["startingAt"] = self.df["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
        self.df["endingAt"] = self.df["endingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
               


    def save_to_database(self):        
        self.df.to_sql("ohlc" + self.symbol + "_" + self.interval, self.conn, if_exists="replace")          
        
            
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
            close=db["close"]
        )
        can = go.Figure(candlestick)
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
