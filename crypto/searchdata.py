import sqlite3
from coinrankcandle import CoinRankingOHLC
from coinrankingLine import CoinPriceHistory

class CoinRankingSearch:
    def __init__(self, find):
        self.find = find
        self.uuid = None
        self.name = None
        self.price = None
        self.change = None
        
    def data(self):
        # Connect to the database
        conn = sqlite3.connect("coinranking.db")

        # Create a cursor
        cursor = conn.cursor()

        query = '''
        SELECT name,symbol,price,uuid,change FROM coinrankingdata WHERE symbol = ?
        '''
        # Execute the SELECT statement
        cursor.execute(query, (self.find,))

        # Iterate through the rows returned by the SELECT statement and print out the data for each column
        for (name, symbol, price,uuid,change) in cursor:
            self.uuid = uuid
            self.name = name
            self.price = price
            self.change = change
            print(f'Name: {name}')
            print(f'Price: {price}')
            print(f'Change: {change}')

        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        
    def get_uuid(self):
        return self.uuid

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price
    
    def get_change(self):
        return self.change
    
    



if __name__ == "__main__":
    # symbol = input("Enter the symbol of the coin you want to search for: ")
    symbol = "BTC"
    search = CoinRankingSearch(symbol)
    search.data()
    uuid = search.get_uuid()
    name = search.get_name()
        # interval = input("Enter the interval : ")
    # minute hour 8hours day week month
    interval = "day"
    # limit = input("Enter the number of candles you want to retrieve: ")
    limit = 200
    # 3h 24h 7d 30d 3m 1y 3y 5y
    timePeriod = "24h"
    # symbol=search.get_symbol()
    # print(symbol)
    ohlc = CoinRankingOHLC(uuid, interval, limit, symbol,name)
    ohlc.retrieve_data()
    ohlc.save_to_database()
    ohlc.show_candlestick()
    ohlc.close_connection()
    cr = CoinPriceHistory(uuid, timePeriod, symbol,name)
    cr.retrieve_data()
    cr.save_to_database()
#     # cr.save_to_excel()
    cr.show_linechart()
    cr.close_connection()
    

