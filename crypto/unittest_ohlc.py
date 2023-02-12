
import pandas as pd

import json

import unittest
from coinrankcandle import CoinRankingOHLC

import requests_mock
import datetime
from unittest.mock import Mock



class TestOHLC(unittest.TestCase):
    # def setUp(self):
    #     self.ohlc = CoinRankingOHLC(uuid='yhjMzLPhuIDl', interval='1h', limit=10, symbol='BTC', name='Bitcoin')
    #     self.ohlc.retrieve_data()
    
    #testing the "name" attribute of the CoinRankingOHLC class
    def test_name(self): 
        ohlc = CoinRankingOHLC(uuid='yhjMzLPhuIDl', interval='day', limit=10, symbol='BTC', name='Bitcoin')

        assert ohlc.name == "Bitcoin"

    # checks the first open value 
    def test_retrieve_data(self):
        self.ohlc = CoinRankingOHLC(uuid='yhjMzLPhuIDl', interval='day', limit=10, symbol='BTC', name='Bitcoin')
        self.headers = {'Accept': 'application/json'}
        with requests_mock.Mocker() as mock_requests:
            mock_requests.get(self.ohlc.url, headers=self.headers, status_code=200,
                              text=json.dumps({'data': {'ohlc': [{'startingAt': 161398400, 'open': 28000, 'high': 29000,
                                                                'low': 27000, 'close': 28000, 'endingAt': 1613997600},
                                                               {'startingAt': 1613997600, 'open': 26000, 'high': 29000,
                                                                'low': 27000, 'close': 28000, 'endingAt': 1614011200}]}}))
            self.ohlc.retrieve_data()

        assert self.ohlc.df["open"][0] == 28000


    # checks timestamp 
    def test_retrieve_data2(self):
        self.ohlc = CoinRankingOHLC(uuid='yhjMzLPhuIDl', interval='day', limit=10, symbol='BTC', name='Bitcoin')
        self.headers = {'Accept': 'application/json'}
        with requests_mock.Mocker() as mock_requests:
            mock_requests.get(self.ohlc.url, headers=self.headers, status_code=200,
                              text=json.dumps({'data': {'ohlc': [{'startingAt': 161398400, 'open': 28000, 'high': 29000,
                                                                'low': 27000, 'close': 28000, 'endingAt': 1613997600},
                                                               {'startingAt': 1613997600, 'open': 26000, 'high': 29000,
                                                                'low': 27000, 'close': 28000, 'endingAt': 1614011200}]}}))
            self.ohlc.retrieve_data()

        expected_timestamp = datetime.datetime.fromtimestamp(161398400)

        assert self.ohlc.df["startingAt"][0] == expected_timestamp
   
        
        

            

    

    
if __name__ == '__main__':
    unittest.main()

    