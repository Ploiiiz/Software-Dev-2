import sqlite3
import pandas
import av_getdata
from pymongo import MongoClient

class DatabaseBridger:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        self.database = None
        self.collection = None
    
    def connect_database(self,database):
        self.database = self.client[database]
    
    def get_collection(self,database,collection):
        self.collection = self.database[collection]
    
    def post(self,ticker,open,high,low,close,adj_close,vol):
        schema = {
            "ticker": ticker,
            "open": open,
            "high": high,
            "low": low,
            "close": close,
            "adjusted_close": adj_close,
            "volume": vol
        }
        self.collection.insert_one(schema)


client = MongoClient('localhost', 27017)
client['stocksdata']['usa_stocks'].insert_one({
            "ticker": 'IBM',
            "open": 144.06,
            "high": 146.1,
            "low": 144.01,
            "close": 145.89,
            "adjusted_close": 145.89,
            "volume": 2455786.0
        })

    
