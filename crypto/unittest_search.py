
from mock import patch
import mock
import pandas as pd

import json

import unittest

import requests_mock
import datetime
from unittest.mock import MagicMock
from searchdata import CoinRankingSearch
import sqlite3

class TestSearch(unittest.TestCase):

    def test_get_name(self):
        expected_name = "Bitcoin"
        search = CoinRankingSearch("BTC")
        # search.data()
        search_name = search.get_name()
        
        assert expected_name == search_name
    
    def test_get_uuid(self):
        expected_uuid = "Qwsogvtv82FCd"
        search = CoinRankingSearch("BTC")
        # search.data()
        search_uuid = search.get_uuid()
        assert expected_uuid == search_uuid   


    def test_insert_data(self):
        # Create a MagicMock object for the database cursor
        mock_conn = MagicMock()

        sqlite3.connect = MagicMock(return_value=mock_conn)

        mock_cur = MagicMock()
        mock_conn.cursor.return_value = mock_cur

        search = CoinRankingSearch('ST')
        search.uuid = "santaiscat"
        search.name = "Santa"
        search.price = 12500
        search.change = 1.25
        search.insert_data()

        # assert_called_with เป็นการตรวจสอบว่า Mock Object นั้นได้ถูกเรียกด้วยข้อมูลชุดนี้หรือไม่
        mock_cur.execute.assert_called_with('\n            INSERT INTO coinrankingdata (name, symbol, price, uuid, change)\n            VALUES (?, ?, ?, ?, ?)\n        ', ('Santa', 'ST', 12500, 'santaiscat', 1.25))
    #
       

    def test_update_data(self):
        # Create a MagicMock object for the database cursor
        mock_conn = MagicMock()

        sqlite3.connect = MagicMock(return_value=mock_conn)

        mock_cur = MagicMock()
        mock_conn.cursor.return_value = mock_cur

        search = CoinRankingSearch('ST')
        search.uuid = "santaiscat"
        search.name = "Santa"
        search.price = 10000
        search.change = 1.25
        search.update_data()

        # assert_called_with เป็นการตรวจสอบว่า Mock Object นั้นได้ถูกเรียกด้วยข้อมูลชุดนี้หรือไม่
        mock_cur.execute.assert_called_with('\n            UPDATE coinrankingdata SET name = "Santa",price = 10000,uuid = "santaiscat",change = 1.25\n            WHERE symbol = ?\n        ', ('ST',))
        # mock_cur.execute.assert_called_with('\n            UPDATE coinrankingdata SET {}\n            WHERE symbol = ?\n        ', ('ST',))


    def test_delete_data(self):
        # Create a MagicMock object for the database cursor
        mock_conn = MagicMock()

        sqlite3.connect = MagicMock(return_value=mock_conn)

        mock_cur = MagicMock()
        mock_conn.cursor.return_value = mock_cur

        search = CoinRankingSearch('BTC')      
        
        search.delete_data()

        # assert_called_with เป็นการตรวจสอบว่า Mock Object นั้นได้ถูกเรียกด้วยข้อมูลชุดนี้หรือไม่
        mock_cur.execute.assert_called_with('\n            DELETE FROM coinrankingdata WHERE symbol = ?\n        ', ('BTC',))



if __name__ == '__main__':
    unittest.main()
