import requests
import header
import sqlite3
import json
import pandas as pd
import datetime

# # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey=' + header.api_AV
# r = requests.get(url)
# data = r.json()

# print(data)

class AV_Volume:
    def __init__(self,symbol):
        self.symbol = symbol
        self.headers = header.headers
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        self.url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=' + str(self.symbol) + 'market=USD&apikey=' + header.api_AV

    


        
    def retrieve_data(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Alpha Vantage API")
            exit()
        # data = response.json()['Time Series (Digital Currency Daily)']
        data = json.loads(response.text)
        print(data)
        # self.df = pd.DataFrame(data["data"]["ohlc"])
        # # print(data)
        # df = pd.DataFrame(data).T
        # volume = df['5. volume']
        # print(volume)

    def save_to_excel(self):
        self.df.to_excel('coinrankingohlc.xlsx', sheet_name= self.symbol + "_" + self.interval , index=True)

    def save_to_database(self):        
        self.df.to_sql("ohlc" + self.symbol + "_" + self.interval, self.conn, if_exists="replace")


if __name__ == "__main__":
    vol = AV_Volume("BTC")
    vol.retrieve_data()