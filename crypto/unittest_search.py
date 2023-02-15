
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
        search.data()
        search_name = search.get_name()
        
        assert expected_name == search_name
    
    def test_get_uuid(self):
        expected_uuid = "Qwsogvtv82FCd"
        search = CoinRankingSearch("BTC")
        search.data()
        search_uuid = search.get_uuid()

        assert expected_uuid == search_uuid    

    def test_insert_data2(self):
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

        mock_cur.execute.assert_called_with('\n            INSERT INTO coinrankingdata (name, symbol, price, uuid, change)\n            VALUES (?, ?, ?, ?, ?)\n        ', ('Santa', 'ST', 12500, 'santaiscat', 1.25))

        # mock_cur.execute.assert_called_with(
        #     'INSERT INTO coinrankingdata (name, symbol, price, uuid, change) VALUES (?, ?, ?, ?, ?)',
        #     ('Santa', 'ST', 12500, 'santaiscat', 1.25)
        # )

    @patch('searchdata.sqlite3')
    def test_insert_data(self, mock_sqlite3):
        mock_conn = mock_sqlite3.connect.return_value
        mock_cur = mock_conn.cursor.return_value

        search = CoinRankingSearch('ST')
        search.name = 'Santa'
        search.price = 12500
        search.uuid = 'santaiscat'
        search.change = 1.25

        search.insert_data()

        
        mock_conn.commit.assert_called_once()
        mock_cur.close.assert_called_once()
        mock_cur.execute.assert_called_with('\n            INSERT INTO coinrankingdata (name, symbol, price, uuid, change)\n            VALUES (?, ?, ?, ?, ?)\n        ', ('Santa', 'ST', 12500, 'santaiscat', 1.25))




    # def test_update_data(self):
    #     # Insert data into the temporary database
    #     self.cursor.execute("""
    #         INSERT INTO coinrankingdata (name, symbol, price, uuid, change)
    #         VALUES ('Bitcoin', 'BTC', 10000, 'abc123', 0.05)
    #     """)

    #     # Create a CoinRankingSearch object
    #     search = CoinRankingSearch("BTC")

    #     # Update the data in the temporary database
    #     search.price = 20000
    #     search.change = 0.1
    #     search.update_data(self.conn)

    #     # Check that the data was updated correctly
    #     self.cursor.execute("""
    #         SELECT * FROM coinrankingdata WHERE symbol = 'BTC'
    #     """)
    #     result = self.cursor.fetchone()
    #     self.assertEqual(result, ("Bitcoin", "BTC", 20000, "abc123", 0.1))

    # def test_delete_data(self):
    #     # Insert data into the temporary database
    #     self.cursor.execute("""
    #         INSERT INTO coinrankingdata (name, symbol, price, uuid, change)
    #         VALUES ('Bitcoin', 'BTC', 10000, 'abc123', 0.05)
    #     """)

    #     # Create a CoinRankingSearch object
    #     search = CoinRankingSearch("BTC")

    #     # Delete the data from the temporary database
    #     search.delete_data(self.conn)

    #     # Check that the data was deleted correctly
    #     self.cursor.execute("""
    #         SELECT * FROM coinrankingdata WHERE symbol = 'BTC'
    #     """)
    #     result = self.cursor.fetchone()
    #     self.assertIsNone(result)



if __name__ == '__main__':
    unittest.main()
    
