# your API credentials
import credentials
api_key = credentials.av_api_key

# alpha vantage caller
import av_caller
import transformer

# testing
import datetime
import bson
import pandas
import unittest
from unittest import TestCase, mock
from unittest.mock import Mock, patch
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Assume we have a function that inserts stock data into the database
def insert_stock_data(db_client, symbol, data):
    try:
        db_client.stocks[symbol].insert_one(data)
        return True
    except PyMongoError:
        return False

def read_stock_data(db_client, symbol, start_date, end_date):
    try:
        cursor = db_client.stocks[symbol].find(
            {'date': {'$gte': start_date, '$lte': end_date}}
        ).sort('date')
        data = [doc for doc in cursor]
        return data
    except PyMongoError:
        return None

class TestAV(unittest.TestCase):
    @patch.object(av_caller.TimeSeries, 'get_daily_adjusted')
    def test_daily(self, mock_get_daily_adjusted):
         # Set the return value of the mock to be a JSON string containing the desired data
        mock_get_daily_adjusted.return_value = {'data': 'mocked data'}

        # Call the function being tested with some example arguments
        api_key = "1234"
        symbol = "ABC"
        data = av_caller.daily(api_key, symbol)

        # Check that the function returned the expected data
        self.assertEqual(data, {'data': 'mocked data'})

        # Test the function with a different API key and symbol
        api_key = "5678"
        symbol = "DEF"
        data = av_caller.daily(api_key, symbol)
        self.assertEqual(data, {'data': 'mocked data'})
    
    @patch.object(av_caller.TimeSeries, 'get_weekly_adjusted')
    def test_weekly(self, mock_get_weekly_adjusted):
         # Set the return value of the mock to be a JSON string containing the desired data
        mock_get_weekly_adjusted.return_value = {'data': 'mocked data'}

        # Call the function being tested with some example arguments
        api_key = "1234"
        symbol = "ABC"
        data = av_caller.weekly(api_key, symbol)

        # Check that the function returned the expected data
        self.assertEqual(data, {'data': 'mocked data'})

        # Test the function with a different API key and symbol
        api_key = "5678"
        symbol = "DEF"
        data = av_caller.weekly(api_key, symbol)
        self.assertEqual(data, {'data': 'mocked data'})

    @patch.object(av_caller.TimeSeries, 'get_monthly_adjusted')
    def test_monthly(self, mock_get_monthly_adjusted):
         # Set the return value of the mock to be a JSON string containing the desired data
        mock_get_monthly_adjusted.return_value = {'data': 'mocked data'}

        # Call the function being tested with some example arguments
        api_key = "1234"
        symbol = "ABC"
        data = av_caller.monthly(api_key, symbol)

        # Check that the function returned the expected data
        self.assertEqual(data, {'data': 'mocked data'})

        # Test the function with a different API key and symbol
        api_key = "5678"
        symbol = "DEF"
        data = av_caller.monthly(api_key, symbol)
        self.assertEqual(data, {'data': 'mocked data'})       

    @patch.object(av_caller.TimeSeries, 'get_daily_adjusted')
    def test_renamecol(self, mock_get_daily_adjusted):
        testdata = {
            '2023-03-03': { '1. open': '148.045',
                            '2. high': '151.11',
                            '3. low': '147.33',
                            '4. close': '151.03',
                            '5. adjusted close': '151.03',
                            '6. volume': '70732297',
                            '7. dividend amount': '0.0000',
                            '8. split coefficient': '1.0'},
            '2023-03-02': { '1. open': '144.38',
                            '2. high': '146.71',
                            '3. low': '143.9',
                            '4. close': '145.91',
                            '5. adjusted close': '145.91',
                            '6. volume': '52279761',
                            '7. dividend amount': '0.0000',
                            '8. split coefficient': '1.0'},
            '2023-03-01': { '1. open': '146.83',
                            '2. high': '147.2285',
                            '3. low': '145.01',
                            '4. close': '145.31',
                            '5. adjusted close': '145.31',
                            '6. volume': '55478991',
                            '7. dividend amount': '0.0000',
                            '8. split coefficient': '1.0'}}
        
        df = pandas.DataFrame.from_dict(testdata, orient='index')
        df.columns = ['1. open',	'2. high',	'3. low',	'4. close',	'5. adjusted close',	'6. volume',	'7. dividend amount', '8. split coefficient']
        df.index = pandas.to_datetime(df.index)
        df = df.apply(pandas.to_numeric, errors='coerce')

        mock_get_daily_adjusted.return_value = df
        api_key = "1234"
        symbol = "ABC"
        data = av_caller.daily(api_key, symbol)
        data = transformer.rename_price(data)

        self.assertEqual(list(data.columns), ['open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend amount', 'split coefficient'] )

    def test_isvalidBSONdate(self):
        date = '2023-03-03'
        self.assertIsInstance(datetime.datetime.strptime(date,'%Y-%m-%d'),bson.datetime.datetime)

    @mock.patch('pymongo.MongoClient')
    def test_insert_stock_data(self, mock_mongo_client):
        # create a mock database and collection
        mock_db = mock_mongo_client().stocks
        mock_collection = mock_db.__getitem__().insert_one
        mock_collection.return_value.inserted_id = 1234567890

        # call the function being tested
        symbol = "ABC"
        data = {'date': '2022-01-01', 'open': 100, 'high': 110, 'low': 90, 'close': 105}
        result = insert_stock_data(mock_mongo_client(), symbol, data)

        # assert that the function returns True
        self.assertTrue(result)

        # assert that the data was inserted into the correct collection
        mock_db.__getitem__().insert_one.assert_called_once_with(data)

    @mock.patch('pymongo.MongoClient')
    def test_insert_stock_data_failure(self, mock_mongo_client):
        # create a mock database and collection
        mock_db = mock_mongo_client().stocks
        mock_collection = mock_db.__getitem__().insert_one
        mock_collection.return_value.inserted_id = 1234567890

        # set the side_effect to return PyMongoError
        mock_collection.side_effect = PyMongoError


        # call the function being tested
        symbol = "ABC"
        data = {'date': '2022-01-01', 'open': 100, 'high': 110, 'low': 90, 'close': 105}
        result = insert_stock_data(mock_mongo_client(), symbol, data)

        # assert that the function returns False
        self.assertFalse(result)

    @mock.patch('pymongo.MongoClient')
    def test_read_stock_data(self, mock_mongo_client):
        # create a mock database and collection
        mock_db = mock_mongo_client().stocks
        mock_collection = mock_db.__getitem__()
        mock_cursor = mock_collection.find.return_value
        mock_cursor.sort.return_value = mock_cursor

        # define the data to be returned by the mock cursor
        mock_data = [
            {'date': '2022-01-01', 'open': 100, 'high': 110, 'low': 90, 'close': 105},
            {'date': '2022-01-02', 'open': 105, 'high': 120, 'low': 100, 'close': 115},
            {'date': '2022-01-03', 'open': 115, 'high': 125, 'low': 110, 'close': 120},
        ]
        mock_cursor.__iter__.return_value = iter(mock_data)

        # call the function being tested
        symbol = "ABC"
        start_date = "2022-01-01"
        end_date = "2022-01-03"
        result = read_stock_data(mock_mongo_client(), symbol, start_date, end_date)

        # assert that the function returns the expected data
        expected_result = [
            {'date': '2022-01-01', 'open': 100, 'high': 110, 'low': 90, 'close': 105},
            {'date': '2022-01-02', 'open': 105, 'high': 120, 'low': 100, 'close': 115},
            {'date': '2022-01-03', 'open': 115, 'high': 125, 'low': 110, 'close': 120},
        ]
        self.assertEqual(result, expected_result)

        # assert that the find and sort methods were called with the correct arguments
        mock_collection.find.assert_called_once_with(
            {'date': {'$gte': start_date, '$lte': end_date}}
        )
        mock_cursor.sort.assert_called_once_with('date')

    def test_news(self):
        mock_response = Mock()
        mock_response.json.return_value = {
    "items": "50",
    "sentiment_score_definition": "x <= -0.35: Bearish; -0.35 < x <= -0.15: Somewhat-Bearish; -0.15 < x < 0.15: Neutral; 0.15 <= x < 0.35: Somewhat_Bullish; x >= 0.35: Bullish",
    "relevance_score_definition": "0 < x <= 1, with a higher score indicating higher relevance.",
    "feed": [
        {
            "title": "Leave iPhone In The Pocket And Calculate Tips With Apple Watch - Apple  ( NASDAQ:AAPL ) ",
            "url": "https://www.benzinga.com/news/23/03/31234929/leave-your-iphone-in-pocket-and-still-calculate-tips-slyly-with-your-apple-watch",
            "time_published": "20230307T122344",
            "authors": [
                "Ananya Gairola"
            ],
            "summary": "An Apple Inc. AAPL Watch feature that lets you calculate tips is going viral on TikTok.",
            "banner_image": "https://cdn.benzinga.com/files/images/story/2023/Apple_Watch_Photo_by_Lukas_Gojda_on_Shutterstock.jpeg?width=1200&height=800&fit=crop",
            "source": "Benzinga",
            "category_within_source": "News",
            "source_domain": "www.benzinga.com",
            "topics": [
                {
                    "topic": "Technology",
                    "relevance_score": "1.0"
                }
            ],
            "overall_sentiment_score": 0.018986,
            "overall_sentiment_label": "Neutral",
            "ticker_sentiment": [
                {
                    "ticker": "AAPL",
                    "relevance_score": "0.904419",
                    "ticker_sentiment_score": "0.083408",
                    "ticker_sentiment_label": "Neutral"
                }
            ]
        }
    ]
}
        mock_get = Mock(return_value=mock_response)

        with patch('av_caller.requests.request', mock_get):
            result = av_caller.news(api_key)

        self.assertEqual(result, (mock_response.json()['feed'],mock_response.json()['items']))

    
if __name__ == "__main__":
    unittest.main()