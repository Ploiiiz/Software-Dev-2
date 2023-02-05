import pandas
import av_getdata
import credentials
from pymongo import MongoClient
import datetime

class DatabaseConnection:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', credentials.db_port)
        self.fetcher = av_getdata.StocksData()
        self.dir = self.client.stocksdata.usa_stocks
        # self.dir = None
        self.dates = []
        self.today = datetime.datetime.today
    
    # def usa_stocks(self):
    #     self.dir = self.client.stocksdata.usa_stocks
    
    def new_entry(self,ticker):
        if self.dir.find_one({'ticker': ticker}) == None:
            schema = {
                "ticker": ticker,
                "data": {
                    "ticker": ticker,
                    "date": [],
                    "open": [],
                    "high": [],
                    "low": [],
                    "close": [],
                    "adjusted_close": [],
                    "volume": []
                }
            }
            self.dir.insert_one(schema)
    
    def _update(self,ticker,date,data):
        open,high,low,close,adj,vol = data[0],data[1],data[2],data[3],data[4],data[5]
        self.dir.update_one(
            {'ticker': ticker}, 
            {'$push': {
                'data._id' : date,
                'data.open' : open,
                'data.high' : high,
                'data.low' : low,
                'data.close' : close,
                'data.adjusted_close' : adj,
                'data.volume' : vol
                }
            }
        )
    
    def get_dates(self,ticker):
        data_objects = self.dir.find_one(
            {'ticker': ticker}, 
            {'data': {
                'date':1,
                    }
                }
            )
        self.dates = data_objects['data']['date']

    def _push_data(self,ticker,data):
        self.get_dates(ticker)
        for date,values in zip(data.index,data.values):
            data_arr = values[:-2] # no dividend amount, split coefficient
            if date not in self.dates:
                self._update(ticker,date,data_arr)

    def _data(self,ticker):
        data = self.dir.find_one(
            {'ticker': ticker}, {'data': {
                'date':1,
                'open':1,
                'high':1,
                'low':1,
                'close':1,
                'volume':1
                }
            }
        )
        return data

    def make_dataframe(self,data):
        dataframe = pandas.DataFrame(
            {
                'date' : data['data']['date'],
                'open' : data['data']['open'],
                'high' : data['data']['high'],
                'low' : data['data']['low'],
                'close' : data['data']['close'],
                'volume' : data['data']['volume'],
            }
        )
        return dataframe

    def get_data(self,ticker):
        #self.update_data(ticker)
        data = self._data(ticker)
        df = self.make_dataframe(data)
        return df          

    def fetch(self,ticker):
        stocks_data, metadata = self.fetcher.daily_adjusted(ticker,'full')
        return stocks_data

    def update_data(self,ticker):
        fulldata = self.fetch(ticker)
        fulldata = fulldata.drop(['7. dividend amount', '8. split coefficient'],axis=1)
        fulldata.sort_index()
        self._push_data(ticker,fulldata)


# conn = DatabaseConnection()
# db = conn.client.stocksdata.usa_stocks
# db.insert_one(conn.post('IBM'))
