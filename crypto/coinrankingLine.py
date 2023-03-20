import requests
import pandas as pd
import plotly.graph_objects as go
import json
import datetime
import plotly.express as px
import header
import sqlite3

class CoinPriceHistory:
    def __init__(self, uuid, symbol,name,interval,fiat):
        self.uuid = uuid
        self.name = name
        self.interval = interval
        if self.interval == 'hour':
            self.timePeriod = "30d"   
        elif self.interval == 'day' or "week" or "month":
            self.timePeriod = "3y"         
        self.symbol = symbol
        self.headers = header.headers        
        self.fiat = fiat
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(self.uuid) + "/history"
        self.params = {"referenceCurrencyUuid":fiat,"timePeriod":self.timePeriod}

    
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
        # print(self.df)

        
         # Insert the data into the 'ohlc' table
        for i in range(len(self.df)):
            timestamp = int(self.df['timestamp'][i])
            timestamp = datetime.datetime.fromtimestamp(timestamp)
            price = self.df['price'][i]
                
            query = f"UPDATE ohlc{self.symbol}_{self.interval} SET price = ? WHERE endingAt = ?"
            self.cursor.execute(query, (price,timestamp))
            self.cursor.execute(
                f"SELECT * FROM ohlc{self.symbol}_{self.interval} ORDER BY endingAt DESC;"
            )
            
            self.conn.commit()
        self.conn.close()

    def pandas_data(self):
        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
        data = json.loads(response.text)
        # print(data["data"]["history"])
        self.df = pd.DataFrame(data["data"]["history"]) 
        self.df["price"] = pd.to_numeric(self.df["price"])
        self.df['timestamp']= self.df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x)) 
        return self.df
     
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
    # cr = CoinPriceHistory("Qwsogvtv82FCd", "BTC","Bitcoin")
    cr = CoinPriceHistory("razxDUgYGNAdQ", "ETH", "Ethereum","hour","yhjMzLPhuIDl")
    # print(cr.pandas_data())
    # l = cr.pandas_data()
    # print(l['timestamp'])
    # cr.get_symbol()
#     cr = CoinRankingOHLC(uuid, interval, limit)
    cr.retrieve_data()
    # cr.save_to_database()
#     # cr.save_to_excel()
    # cr.show_linechart()
    # cr.close_connection()

