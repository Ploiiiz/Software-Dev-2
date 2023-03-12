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
        data = transformer.rename_price_columns(data)

        self.assertEqual(list(data.columns), ['open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend_amount'] )

    @patch.object(av_caller.FundamentalData, 'get_company_overview')
    def test_overview_to_dataframe(self, mock_get_company_overview):
        overview,meta = (
            {   'Symbol': 'AAPL',
                'AssetType': 'Common Stock',
                'Name': 'Apple Inc',
                'Description': "Apple Inc. is an American multinational technology company that specializes in consumer electronics, computer software, and online services. Apple is the world's largest technology company by revenue (totalling $274.5 billion in 2020) and, since January 2021, the world's most valuable company. As of 2021, Apple is the world's fourth-largest PC vendor by unit sales, and fourth-largest smartphone manufacturer. It is one of the Big Five American information technology companies, along with Amazon, Google, Microsoft, and Facebook.",
                'CIK': '320193',
                'Exchange': 'NASDAQ',
                'Currency': 'USD',
                'Country': 'USA',
                'Sector': 'TECHNOLOGY'}
                ,None)
        df = transformer.overview_to_dataframe(overview)
        self.assertEqual(df.index.name,('Symbol'))
        self.assertEqual(list(df.columns), ['AssetType', 'Name', 'Description', 'CIK', 'Exchange', 'Currency', 'Country', 'Sector'])

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