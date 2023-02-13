
import pandas as pd

import json

import unittest
from coinrankingLine import CoinPriceHistory

import requests_mock
import datetime
from unittest.mock import Mock



class TestPrice(unittest.TestCase):
    
    # checks the first price value 
    def test_retrieve_data(self):
        self.price = CoinPriceHistory(uuid='yhjMzLPhuIDl', timePeriod='24h',symbol='BTC', name='Bitcoin')
        self.headers = {'Accept': 'application/json'}
        with requests_mock.Mocker() as mock_requests:
            mock_requests.get(self.price.url, headers=self.headers, status_code=200,
                              text=json.dumps({'data': {'history':[{'price': '21000', 'timestamp': 1676264700}, 
                                                    {'price': '21844.30962222367', 'timestamp': 1676264400}, 
                                                    {'price': '21837.601363307193', 'timestamp': 1676264100}]}}))
            self.price.retrieve_data()

        assert self.price.df["price"][0] == 21000


    # checks timestamp 
    def test_retrieve_data2(self):
        self.price = CoinPriceHistory(uuid='yhjMzLPhuIDl', timePeriod='24h',symbol='BTC', name='Bitcoin')
        self.headers = {'Accept': 'application/json'}
        with requests_mock.Mocker() as mock_requests:
            mock_requests.get(self.price.url, headers=self.headers, status_code=200,
                              text=json.dumps({'data': {'history':[{'price': '21000', 'timestamp': 1676264700}, 
                                                    {'price': '21800', 'timestamp': 1676264400}, 
                                                    {'price': '21830', 'timestamp': 1676264100}]}}))
            self.price.retrieve_data()

        expected_timestamp = datetime.datetime.fromtimestamp(1676264700)

        assert self.price.df["timestamp"][0] == expected_timestamp
   
        
        

            

    

    
if __name__ == '__main__':
    unittest.main()

    