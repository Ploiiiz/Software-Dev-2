# import requests
# import pandas as pd
# import plotly.express as px
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
# import json
# import datetime
# import header
# import sqlite3
# import time
# import plotly.io as pio

# # from searchdata import CoinRankingSearch


# class CoinRankingOHLC:

#     def __init__(self, uuid, timePeriod, symbol,name,interval):
#         self.uuid = uuid
#         self.name = name
#         self.timePeriod = timePeriod        
#         self.symbol = symbol
#         self.interval = interval
#         self.headers = header.headers
#         self.conn = sqlite3.connect("coinranking.db")
#         self.cursor = self.conn.cursor()
#         self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(self.uuid) + "/history"
#         self.params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":self.timePeriod}

#     def check_table(self):
#         table_name = "ohlc" + self.symbol + "_" + self.interval
#         query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     startingAt TIMESTAMP,
#                     endingAt TIMESTAMP,
#                     open TEXT,
#                     high TEXT,
#                     low TEXT,
#                     close TEXT,
#                     avg TEXT
#                     price TEXT
#                     timestamp TIMESTAMP
#                 );'''

#         self.cursor.execute(query)
#         self.conn.commit()

#     def add_column(self):
#         table_name = "ohlc" + self.symbol + "_" + self.interval
#         query = f'''ALTER TABLE {table_name} ADD COLUMN price TEXT;'''

#         self.cursor.execute(query)

#         query = f'''ALTER TABLE {table_name} ADD COLUMN timestamp TIMESTAMP;'''
#         self.cursor.execute(query)
#         self.conn.commit()

#     def get_latest_timestamp(self):
#         query = f"SELECT MAX(timestamp) FROM ohlc{self.symbol}_{self.interval}"
#         self.cursor.execute(query)
#         result = self.cursor.fetchone()[0]
#         if result is not None:
#             return datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
#         else:
#             month = datetime.timedelta(days=180)  #=6month
#             now = datetime.datetime.now()
#             target = now - month

#             formatted_target = target.strftime('%Y-%m-%d %H:%M:%S')
#             return datetime.datetime.strptime(formatted_target,
#                                               '%Y-%m-%d %H:%M:%S')

#     def set_limit(self):
#         now = datetime.datetime.now()
#         self.latest_timestamp = self.get_latest_timestamp()
#         print(self.latest_timestamp)
#         if self.latest_timestamp < now:
#             #max 5000
#             # limit = 5000
#             self.limit = (now -
#                           self.latest_timestamp).total_seconds() // (3600)
#             print(self.limit)

#             if self.limit == 1:
#                 return None

#             else:
#                 self.params['limit'] = int(self.limit) - 1

#             print(
#                 self.params['limit']
#             )  # set the limit based on the time difference between the latest timestamp and now

#         else:
#             self.params[
#                 'limit'] = 1  # set limit to 1 if the latest timestamp is in the future

#     def retrieve_data2(self):
#         self.check_table()
#         self.add_column()
#         self.set_limit()
#         self.cursor.execute(
#             f"SELECT MAX(timestamp) FROM ohlc{self.symbol}_{self.interval}")
#         result = self.cursor.fetchone()
#         response = requests.get(self.url,
#                                 params=self.params,
#                                 headers=self.headers)
#         if response.status_code != 200:
#             print("Error: Could not retrieve data from Coinranking API")
#             exit()
#         data = json.loads(response.text)
#         new_data = pd.DataFrame(data["data"]["history"])
#         new_data["price"] = pd.to_numeric(new_data["price"])
        
#         new_data['timestamp']= new_data['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))  
    
#         if self.limit == 1:
#             return None

#         else:
#             # append the new data to the database
#             new_data.to_sql(f"ohlc{self.symbol}_{self.interval}",
#                             self.conn,
#                             if_exists="append",
#                             index=False)
#             self.cursor.execute(
#                 f"SELECT * FROM ohlc{self.symbol}_{self.interval} ORDER BY startingAt DESC;"
#             )
#             self.conn.commit()

#         self.cursor.execute(
#             f"SELECT COUNT(*) FROM ohlc{self.symbol}_{self.interval}")
#         result = self.cursor.fetchone()
#         print(
#             f"Added {len(new_data)} new records to ohlc{self.symbol}_{self.interval}. Total records: {result[0]}"
#         )

#     def retrieve_data(self):
#         response = requests.get(self.url,
#                                 params=self.params,
#                                 headers=self.headers)
#         if response.status_code != 200:
#             print("Error: Could not retrieve data from Coinranking API")
#             exit()
#         data = json.loads(response.text)
#         self.df = pd.DataFrame(data["data"]["ohlc"])
#         self.df["startingAt"] = self.df["startingAt"].apply(
#             lambda x: datetime.datetime.fromtimestamp(x))
#         self.df["endingAt"] = self.df["endingAt"].apply(
#             lambda x: datetime.datetime.fromtimestamp(x))

#     def save_to_excel(self):
#         self.df.to_excel('coinrankingohlc.xlsx',
#                          sheet_name=self.symbol + "_" + self.interval,
#                          index=True)

#     def save_to_database(self):
#         self.df.to_sql("ohlc" + self.symbol + "_" + self.interval,
#                        self.conn,
#                        if_exists="replace")

#     def show_candlestick(self):
#         query = "SELECT price,timestamp FROM ohlc" + self.symbol + "_" + self.interval
#         db = pd.read_sql_query(query, self.conn)
#         fig = px.line(db, x='timestamp', y="price",title=self.name + " " + "(" + self.symbol + ")")
        
#         fig.show()

#     def close_connection(self):
#         self.conn.close()


# if __name__ == "__main__":
#     cr = CoinRankingOHLC("Qwsogvtv82FCd", "24h", "BTC","Bitcoin","hour")
#     # cr = CoinRankingOHLC("Qwsogvtv82FCd", "hour","BTC","Bitcoin")
#     # cr = CoinRankingOHLC("xz24e0BjL", "minute","SHIB","Shiba Inu")
#     # cr.get_symbol()
#     # cr = CoinRankingOHLC(uuid, interval, limit)
#     # cr.retrieve_data()
#     # cr.save_to_database()
#     cr.retrieve_data2()
#     #     # cr.save_to_excel()
#     cr.show_candlestick()

# #     # cr.close_connection()




import requests
import pandas as pd
import plotly.graph_objects as go
import json
import datetime
import plotly.express as px
import header
import sqlite3

class CoinPriceHistory:
    def __init__(self, uuid, symbol,name):
        self.uuid = uuid
        self.name = name
        self.timePeriod = "30d"        
        self.symbol = symbol
        self.headers = header.headers
        self.interval = 'hour'
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(self.uuid) + "/history"
        self.params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":self.timePeriod}

    
    def retrieve_data(self):
        self.add_column()
        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
        data = json.loads(response.text)
        # print(data["data"]["history"])
        self.df = pd.DataFrame(data["data"]["history"])
        # self.df["price"] = pd.to_numeric(self.df["price"])
        # self.df['timestamp']= self.df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x)) 

        
         # Insert the data into the 'ohlc' table
        for i in range(len(self.df)):
            timestamp = int(self.df['timestamp'][i])
            timestamp = datetime.datetime.fromtimestamp(timestamp)
            price = self.df['price'][i]
                
            query = f"UPDATE ohlc{self.symbol}_{self.interval} SET price = ? WHERE startingAt = ?"
            self.cursor.execute(query, (price,timestamp))
            self.cursor.execute(
                f"SELECT * FROM ohlc{self.symbol}_{self.interval} ORDER BY startingAt DESC;"
            )
            
            self.conn.commit()

       
        # self.df.to_sql(f"ohlc{self.symbol}_{self.interval}",
        #                     self.conn,
        #                     if_exists="replace",
        #                     index=False)
        
            # self.conn.commit()

    # def add_column(self):
    #     table_name = "ohlc" + self.symbol + "_" + self.interval
    #     query = f'''ALTER TABLE {table_name} ADD COLUMN price TEXT;'''

    #     self.cursor.execute(query)

    #     query = f'''ALTER TABLE {table_name} ADD COLUMN timestamp TIMESTAMP;'''
    #     self.cursor.execute(query)
    #     self.conn.commit()

    def add_column(self):
        table_name = "ohlc" + self.symbol + "_" + self.interval

        # Check if 'price' column exists in the table
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()
        price_exists = False
        for column in columns:
            if column[1] == 'price':
                price_exists = True
                break

        # If 'price' column does not exist, add it
        if not price_exists:
            query = f'''ALTER TABLE {table_name} ADD COLUMN price REAL;'''
            self.cursor.execute(query)

        self.conn.commit()



    def save_to_database(self):        
        self.df.to_sql("price" + self.symbol + "_" + self.timePeriod, self.conn, if_exists="replace")   
 
        
            
    def save_to_excel(self):
        self.df.to_excel('coinrankingline.xlsx', sheet_name= self.symbol + "_" + self.timePeriod , index=True)
        
    def show_linechart(self,):        
        # df = pd.read_sql_query("SELECT * from price" + self.symbol + "_" + self.timePeriod, self.conn)

        # line_chart = px.line(data_frame=df, x="timestamp", y="price")
        # line_chart.show()
        query = "SELECT price,startingAt FROM ohlc" + self.symbol + "_" + self.interval + " ORDER BY startingAt DESC;"
        
        db = pd.read_sql_query(query, self.conn)
        
    
        fig = px.line(db, x='startingAt', y="price",title=self.name + " " + "(" + self.symbol + ")")
        
        fig.show()
        
        
    def close_connection(self):
        self.conn.close()


if __name__ == "__main__":
    # 3h 24h 7d 30d 3m 1y 3y 5y
    cr = CoinPriceHistory("Qwsogvtv82FCd", "BTC","Bitcoin")
    # cr = CoinPriceHistory("razxDUgYGNAdQ", "ETH", "Ethereum")
    # cr.get_symbol()
#     cr = CoinRankingOHLC(uuid, interval, limit)
    cr.retrieve_data()
    # cr.save_to_database()
#     # cr.save_to_excel()
    # cr.show_linechart()
    cr.close_connection()

