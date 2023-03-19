import sqlite3
from coinrankcandle import CoinRankingOHLC
from coinrankingLine import CoinPriceHistory
import pandas as pd
from coinranking import *

class CoinRankingSearch:
    def __init__(self, find):
        self.find = find
        self.uuid = None
        self.name = None
        self.price = None
        self.change = None
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        
    def data(self):
        Data().retrieve_data()
        query = f'''
        SELECT symbol,name,uuid,change,[24hVolume] FROM coinrankingdata WHERE symbol = '{self.find}'
        '''
        data = pd.read_sql_query(query,self.conn)
        data = data.set_index('symbol')       

        return data
    
    def get_uuid(self):

        query = '''
        SELECT uuid FROM coinrankingdata WHERE symbol = ?
        '''
        # Execute the SELECT statement
        self.cursor.execute(query, (self.find,))
        row = self.cursor.fetchone()
        if row:
            self.uuid = row[0]
            # self.conn.commit()
            # self.cursor.close()
            return self.uuid
        else:
            return None
        
        
        

    def get_name(self):
        query = '''
        SELECT name FROM coinrankingdata WHERE symbol = ?
        '''
        # Execute the SELECT statement
        self.cursor.execute(query, (self.find,))
        row = self.cursor.fetchone()
        if row:
            self.name = row[0]
            # self.conn.commit()
            # self.cursor.close()
            return self.name
        else:
            return None

    def get_price(self):
        return self.price
    
    def get_change(self):
        return self.change
    
    def get_24Vol(self):
        query = '''
        SELECT [24hVolume] FROM coinrankingdata WHERE symbol = ?
        '''
        # Execute the SELECT statement
        self.cursor.execute(query, (self.find,))
        row = self.cursor.fetchone()
        if row:
            self.vol = row[0]
            # self.conn.commit()
            # self.cursor.close()
            return self.vol
        else:
            return None
        

    def insert_data(self):
        
        self.cursor.execute("""
            INSERT INTO coinrankingdata (name, symbol, price, uuid, change)
            VALUES (?, ?, ?, ?, ?)
        """, (self.name, self.find, self.price, self.uuid, self.change))
        self.conn.commit()
        self.cursor.close()


    def delete_data(self):

        self.cursor.execute("""
            DELETE FROM coinrankingdata WHERE symbol = ?
        """, (self.find,))
        self.conn.commit()
        


    def update_data(self):
        set_clause = ''
        if self.name:
            set_clause += 'name = "{}",'.format(self.name)
        if self.price:
            set_clause += 'price = {},'.format(self.price)
        if self.uuid:
            set_clause += 'uuid = "{}",'.format(self.uuid)
        if self.change:
            set_clause += 'change = {},'.format(self.change)

        set_clause = set_clause[:-1]  # remove the last comma

        query = '''
            UPDATE coinrankingdata SET {}
            WHERE symbol = ?
        '''.format(set_clause)

        self.cursor.execute(query, (self.find,))
        self.conn.commit()
        self.cursor.close()
        



    # def close_connection(self):
    #     self.conn.close()
    
    



if __name__ == "__main__":
    # symbol = input("Enter the symbol of the coin you want to search for: ")
    symbol = "BTC"
    search = CoinRankingSearch(symbol)    
    print(search.data())
    # uuid = search.get_uuid()
    
    # search.uuid = "Santaiscat"
    # search.name = "Santa"
    # search.price = 12500
    # search.change = 0.05
    # search.insert_data()
    # search.delete_data()
    # search.update_data()


    # uuid = search.get_uuid()
    # print(uuid)
    # name = search.get_name()
    # print(name)

        # interval = input("Enter the interval : ")
    # minute hour 8hours day week month
    # interval = "day"
    # limit = input("Enter the number of candles you want to retrieve: ")
    # limit = 200
    # 3h 24h 7d 30d 3m 1y 3y 5y
    # timePeriod = "24h"
    # symbol=search.get_symbol()
    # print(symbol)
#     ohlc = CoinRankingOHLC(uuid, interval, limit, symbol,name)
#     ohlc.retrieve_data()
#     ohlc.save_to_database()
#     ohlc.show_candlestick()
#     ohlc.close_connection()
#     cr = CoinPriceHistory(uuid, timePeriod, symbol,name)
#     cr.retrieve_data()
#     cr.save_to_database()
# #     # cr.save_to_excel()
#     cr.show_linechart()
#     cr.close_connection()
    

