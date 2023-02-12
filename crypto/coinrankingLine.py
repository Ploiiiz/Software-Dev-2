import requests
import pandas as pd
import plotly.graph_objects as go
import json
import datetime
import plotly.express as px
import header
import sqlite3

# def line(uuid):

#     # Connect to the database
#     conn = sqlite3.connect("coinranking.db")

#     # Create a cursor
#     cursor = conn.cursor()

#     # Set the API key in the request header
#     headers = header.headers


#     # Make a request to the Coinranking API
#     url = "https://coinranking1.p.rapidapi.com/coin/" + uuid + "/history"
#     params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h"}
#     response = requests.get(url, params=params, headers=headers)

#     # Check the status code of the response
#     if response.status_code != 200:
#         print("Error: Could not retrieve data from Coinranking API")
#         exit()

#     data = json.loads(response.text)
#     df = pd.DataFrame(data["data"]["history"])

#     # Store the coin data in a DataFrame


#     df['timestamp']= df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))
#     df.to_excel('coinrankingline.xlsx', sheet_name='line', index=True)

#     df.to_sql("priceBTC" , conn, if_exists="replace")

#     # Create a line chart


#     cryt = pd.read_excel('coinrankingline.xlsx')

#     # line_g = px.line(data_frame=cryt,x = 'timestamp',y = 'price')
#     line_g = go.Scatter(x = cryt.timestamp ,y = cryt.price, line_color='#0066FF')
#     # print(line_g)

#     # Create the figure and show the plot
#     # fig = go.Figure(line_g)

#     # fig.show()

#     # Commit the changes to the database
#     conn.commit()

#     # Close the connection
#     conn.close()

#     # return fig.show()
#     return line_g

# line("Qwsogvtv82FCd")


class CoinPriceHistory:
    def __init__(self, uuid, timePeriod, symbol):
        self.uuid = uuid
        self.timePeriod = timePeriod        
        self.symbol = symbol
        self.headers = header.headers
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(self.uuid) + "/history"
        self.params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":self.timePeriod}

    
    def retrieve_data(self):
        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
        data = json.loads(response.text)
        self.df = pd.DataFrame(data["data"]["history"])
        self.df["price"] = pd.to_numeric(self.df["price"])

        self.df['timestamp']= self.df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))  


    def save_to_database(self):        
        self.df.to_sql("price" + self.symbol + "_" + self.timePeriod, self.conn, if_exists="replace")   
 
        
            
    def save_to_excel(self):
        self.df.to_excel('coinrankingline.xlsx', sheet_name= self.symbol + "_" + self.timePeriod , index=True)
        
    def show_linechart(self,):        
        # df = pd.read_sql_query("SELECT * from price" + self.symbol + "_" + self.timePeriod, self.conn)

        # line_chart = px.line(data_frame=df, x="timestamp", y="price")
        # line_chart.show()
        query = "SELECT * FROM price" + self.symbol + "_" + self.timePeriod 
        
        db = pd.read_sql_query(query, self.conn)
    
        fig = px.line(db, x='timestamp', y="price")
        
        fig.show()
        
        
    def close_connection(self):
        self.conn.close()


if __name__ == "__main__":
    # 3h 24h 7d 30d 3m 1y 3y 5y
    cr = CoinPriceHistory("Qwsogvtv82FCd", "24h", "BTC")
    # cr.get_symbol()
#     cr = CoinRankingOHLC(uuid, interval, limit)
    cr.retrieve_data()
    cr.save_to_database()
#     # cr.save_to_excel()
    cr.show_linechart()
    cr.close_connection()
