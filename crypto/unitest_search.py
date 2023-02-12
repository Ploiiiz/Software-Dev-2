
import pandas as pd

import json

import unittest
from coinrankcandle import CoinRankingOHLC

import requests_mock
import datetime
from unittest.mock import Mock
from searchdata import CoinRankingSearch

class TestSearch(unittest.TestCase):

    def test_get_name(self):
        expected_name = "Bitcoin"
        search = CoinRankingSearch("BTC")
        search.data()
        search_name = search.get_name()
        
        assert expected_name == search_name
    
    def test_get_uuid(self):
        expected_uuid = "Qwsogvtv82FCd"
        search = CoinRankingSearch("BTC")
        search.data()
        search_uuid = search.get_uuid()

        assert expected_uuid == search_uuid



if __name__ == '__main__':
    unittest.main()
