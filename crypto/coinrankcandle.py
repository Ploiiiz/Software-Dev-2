import requests
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
import datetime
import header
import sqlite3
import time
import plotly.io as pio

# from searchdata import CoinRankingSearch

class CoinRankingOHLC:
    # def __init__(self, uuid, interval, symbol, name):
    #     self.uuid = uuid
    #     self.name = name 
    #     self.interval = interval
    #     self.symbol = symbol
    #     self.headers = header.headers
    #     self.conn = sqlite3.connect("coinranking.db")
    #     self.cursor = self.conn.cursor()
    #     self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(self.uuid) + "/ohlc"
    #     self.latest_timestamp = None  # store the latest timestamp in the database

    # def retrieve_data(self):
    #     self.cursor.execute(f"SELECT MAX(endingAt) FROM ohlc{self.symbol}_{self.interval}")
    #     result = self.cursor.fetchone()
    #     # self.latest_timestamp = result[0] if result[0] else 0  # get the latest timestamp
    #     latest_timestamp = datetime.datetime.strptime(self.latest_timestamp, '%Y-%m-%d %H:%M:%S')

    #     now = int(time.time())
    #     # set the limit based on the difference between the latest timestamp and now
    #     time_difference = datetime.datetime.now() - latest_timestamp
    #     limit = time_difference.seconds // self.interval

    #     # limit = (now - self.latest_timestamp) // self.interval
    #     self.params = {"referenceCurrencyUuid": "yhjMzLPhuIDl", "interval": self.interval, "limit": limit}
    #     response = requests.get(self.url, params=self.params, headers=self.headers)
    #     if response.status_code != 200:
    #         print("Error: Could not retrieve data from Coinranking API")
    #         exit()
    #     data = json.loads(response.text)
    #     new_data = pd.DataFrame(data["data"]["ohlc"])
    #     new_data["startingAt"] = new_data["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
    #     new_data["endingAt"] = new_data["endingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
    #     # filter out the data before the latest timestamp
    #     if self.latest_timestamp:
    #         new_data = new_data[new_data["endingAt"] > self.latest_timestamp]
    #     # append the new data to the database
    #     new_data.to_sql(f"ohlc{self.symbol}_{self.interval}", self.conn, if_exists="append", index=False)
    #     self.cursor.execute(f"SELECT COUNT(*) FROM ohlc{self.symbol}_{self.interval}")
    #     result = self.cursor.fetchone()
    #     print(f"Added {len(new_data)} new records to ohlc{self.symbol}_{self.interval}. Total records: {result[0]}")

    def __init__(self, uuid, interval, symbol, name):
        self.uuid = uuid
        self.name = name 
        self.interval = interval
        self.symbol = symbol
        self.headers = header.headers
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        self.limit = None
        self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(self.uuid) + "/ohlc"
        self.params = {"referenceCurrencyUuid": "yhjMzLPhuIDl", "interval": self.interval, "limit": None}
    
    def check_table(self):
        table_name = "ohlc" + self.symbol + "_" + self.interval
        query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    startingAt TIMESTAMP,
                    endingAt TIMESTAMP,
                    open TEXT,
                    high TEXT,
                    low TEXT,
                    close TEXT,
                    avg TEXT
                );'''

        self.cursor.execute(query)
        self.conn.commit()

        
        

    def get_latest_timestamp(self):
        query = f"SELECT MAX(startingAt) FROM ohlc{self.symbol}_{self.interval}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        if result is not None:
            return datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
        else:
            one_day = datetime.timedelta(days=1)
            now = datetime.datetime.now()
            target = now - one_day

            formatted_target = target.strftime('%Y-%m-%d %H:%M:%S')
            return datetime.datetime.strptime(formatted_target, '%Y-%m-%d %H:%M:%S')
            
    
    def set_limit(self):
        now = datetime.datetime.now()
        self.latest_timestamp = self.get_latest_timestamp()
        print(self.latest_timestamp)
        if self.latest_timestamp < now:
            limit = (now - self.latest_timestamp).total_seconds() // (60)
            print(limit)
            self.params['limit'] = int(limit)-1
            print(self.params['limit'])  # set the limit based on the time difference between the latest timestamp and now
        else:
            self.params['limit'] = 1  # set limit to 1 if the latest timestamp is in the future

    def retrieve_data2(self):
        self.check_table()
        self.set_limit()
        self.cursor.execute(f"SELECT MAX(endingAt) FROM ohlc{self.symbol}_{self.interval}")
        result = self.cursor.fetchone()
        # self.latest_timestamp = result[0] if result[0] else 0  # get the latest timestamp
        # latest_timestamp = datetime.datetime.strptime(self.latest_timestamp, '%Y-%m-%d %H:%M:%S')

        # now = int(time.time())
        # # set the limit based on the difference between the latest timestamp and now
        # time_difference = datetime.datetime.now() - latest_timestamp
        # limit = time_difference.seconds // self.interval

        # limit = (now - self.latest_timestamp) // self.interval
        # self.params = {"referenceCurrencyUuid": "yhjMzLPhuIDl", "interval": self.interval, "limit": self.set_limit}
        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
        data = json.loads(response.text)
        new_data = pd.DataFrame(data["data"]["ohlc"])
        new_data["startingAt"] = new_data["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
        new_data["endingAt"] = new_data["endingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))

        # filter out the data before the latest timestamp
        # if self.latest_timestamp:
        #     new_data = new_data[new_data["endingAt"] > self.latest_timestamp]

        # append the new data to the database
        new_data.to_sql(f"ohlc{self.symbol}_{self.interval}", self.conn, if_exists="append", index= False )
        self.cursor.execute(f"SELECT * FROM ohlc{self.symbol}_{self.interval} ORDER BY startingAt DESC;")
        self.conn.commit()
        self.cursor.execute(f"SELECT COUNT(*) FROM ohlc{self.symbol}_{self.interval}")
        # # self.cursor.execute(f"SELECT * FROM ohlc{self.symbol}_{self.interval} ORDER BY startingAt;")
        result = self.cursor.fetchone()
        print(f"Added {len(new_data)} new records to ohlc{self.symbol}_{self.interval}. Total records: {result[0]}")
    
    # def retrieve_data(self):
    #     self.set_limit()  # call set_limit method to set the limit parameter
    #     response = requests.get(self.url, params=self.params, headers=self.headers)
    #     if response.status_code != 200:
    #         print("Error: Could not retrieve data from Coinranking API")
    #         exit()
    #     data = json.loads(response.text)
    #     self.df = pd.DataFrame(data["data"]["ohlc"])
    #     self.df["startingAt"] = self.df["startingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))
    #     self.df["endingAt"] = self.df["endingAt"].apply(lambda x: datetime.datetime.fromtimestamp(x))          
        
    # def __init__(self, uuid, interval, limit, symbol,name):
    #     self.uuid = uuid
    #     self.name = name 
    #     self.interval = interval
    #     self.limit = limit
    #     self.symbol = symbol
    #     self.headers = header.headers
    #     self.conn = sqlite3.connect("coinranking.db")
    #     self.cursor = self.conn.cursor()
    #     self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(self.uuid) + "/ohlc"
    #     self.params = {"referenceCurrencyUuid":"yhjMzLPhuIDl", "interval":self.interval, "limit":self.limit}

    


        
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

    def save_to_database(self):        
        self.df.to_sql("ohlc" + self.symbol + "_" + self.interval, self.conn, if_exists="replace")
        
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
        can.update_layout(title=self.name + " " + "(" + self.symbol + ")",paper_bgcolor="#001f2e",plot_bgcolor='#003951',title_font_color = 'white')
        js = '''document.body.style.backgroundColor = "#001f2e"; '''        
        can.update_yaxes(showgrid=False,color = 'white') # update the y-axis according to the interval
        can.update_xaxes(showgrid=False,color = 'white')
        # can.show(renderer="browser",post_script=[js])
        can_html = pio.to_html(can, include_plotlyjs='cdn',post_script=[js])

        return can_html
        
    def close_connection(self):
        self.conn.close()
        
if __name__ == "__main__":
    # cr = CoinRankingOHLC("razxDUgYGNAdQ", "minute","ETH","Ethereum")
    cr = CoinRankingOHLC("Qwsogvtv82FCd", "minute","BTC","Bitcoin")
    # cr.get_symbol()
    # cr = CoinRankingOHLC(uuid, interval, limit)
    # cr.retrieve_data()
    # cr.save_to_database()
    # cr.retrieve_data2()
#     # cr.save_to_excel()
    cr.show_candlestick()
    
#     # cr.close_connection()
