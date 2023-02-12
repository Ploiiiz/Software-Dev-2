import sqlite3
from coinrankcandle import CoinRankingOHLC

# def search(find):
#     coinranking.data()
#     # Connect to the database
#     conn = sqlite3.connect("coinranking.db")

#     # Create a cursor
#     cursor = conn.cursor()


#     query = '''
#     SELECT name,symbol,price,uuid,change FROM coinrankingdata WHERE symbol = ?
#     '''
#     # Execute the SELECT statement
#     cursor.execute(query, (find,))

#     # Iterate through the rows returned by the SELECT statement and print out the data for each column
#     for (name, symbol, price,uuid,change) in cursor:
#         uuid = uuid
#         print(f'Name: {name}')
#         print(f'Price: {price}')
#         print(f'Change: {change}')
    



#     # Close the cursor and connection
#     cursor.close()
#     conn.close()

#     return uuid
# # search('BTC')


class CoinRankingSearch:
    def __init__(self, find):
        self.find = find
        self.uuid = None
        
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
            print(f'Name: {name}')
            print(f'Price: {price}')
            print(f'Change: {change}')

        # Close the cursor and connection
        cursor.close()
        conn.close()
        
    def get_uuid(self):
        return self.uuid

    def get_symbol(self):
        return self.find




if __name__ == "__main__":
    # symbol = input("Enter the symbol of the coin you want to search for: ")
    symbol = "BTC"
    search = CoinRankingSearch(symbol)
    search.data()
    uuid = search.get_uuid()
    # interval = input("Enter the interval : ")
    # minute hour 8hours day week month
    interval = "minute"
    # limit = input("Enter the number of candles you want to retrieve: ")
    limit = 200
    # symbol=search.get_symbol()
    # print(symbol)
    ohlc = CoinRankingOHLC(uuid, interval, limit, symbol)
    ohlc.retrieve_data()
    ohlc.save_to_database()
    ohlc.show_candlestick()
    ohlc.close_connection()

