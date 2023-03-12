import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import header
import sqlite3
import math



class Data:
    def __init__(self):
        self.conn = sqlite3.connect("coinranking.db")
        self.df = None
        self.headers = header.headers
        self.url = "https://api.coinranking.com/v2/coins"
        self.params = {"limit": 100,"timePeriod":"1h"}

    def retrieve_data(self):
        
        response = requests.get(self.url, params=self.params, headers=self.headers)

        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()

        data = json.loads(response.text)

        self.df = pd.DataFrame(data['data']['coins'])
        # print(df)

        self.df.to_excel('coinranking.xlsx', sheet_name='dataCoin', index=True)

        cryt = pd.read_excel('coinranking.xlsx')

        cryt.to_sql("coinrankingdata", self.conn, if_exists="replace")

        self.conn.commit()

    def pandas_data(self):
        response = requests.get(self.url, params=self.params, headers=self.headers)

        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()

        data = json.loads(response.text)

        self.df = pd.DataFrame(data['data']['coins'])
        return self.df

    def get_list_symbol(self):
        list_symbol = list(self.df['symbol'])
        return list_symbol
    
    def get_list_uuid(self):
        list_uuid = list(self.df['uuid'])
        return list_uuid
    
    def get_list_name(self):
        list_name = list(self.df['name'])
        return list_name

    def get_list_price(self):
        price = list(self.df['price'])
        list_price = [float(number) for number in price]
        list_price = [format(number, ",.5g") for number in list_price]

        return list_price

    def get_list_change(self):
        self.df['change'] = pd.to_numeric(self.df['change'], errors='coerce')
        list_change = []
        change = list(self.df['change'])
        for c in change:
            if c >= 0:
                ch = '+' + '{:.2f}'.format(c) + '%'
            else:
                ch = '{:.2f}'.format(c) + '%'
            
            list_change.append(ch)

        # print(list_change)
        return list_change
    
    def get_list_change_color(self):
        self.df['change'] = pd.to_numeric(self.df['change'], errors='coerce')
        list_change_color = []
        change_color = list(self.df['change'])
        for c in change_color:
            if c >= 0:
                color = "#19fd53"
            else:
                color = "#fa0104"
            
            list_change_color.append(color)

        # print(list_change)
        return  list_change_color

    def get_list_marketcap(self):
        marketcap = list(self.df['marketCap'])
        list_marketcap = [float(number) for number in marketcap]
        list_marketcap = [format(num / 1000000, ',.0f') + ' M' for num in list_marketcap]
        return list_marketcap



    def close_connection(self):
        self.conn.close()


# data = Data()
# data.retrieve_data()
# # data.get_list_change()
# print(data.get_list_marketcap())
# data.close_connection()





