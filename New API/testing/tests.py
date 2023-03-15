# your API credentials
import credentials
api_key = credentials.av_api_key

# alpha vantage caller
import av_caller
import transformer

# testing
import pandas
import unittest
from unittest import TestCase, mock 
from unittest.mock import Mock, patch,MagicMock
from prettified import *

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

        self.assertEqual(result, mock_response.json()['feed'])


    def test_prettified_daily_valid_symbol(self):
        """Test with a valid symbol"""
        # Arrange
        symbol = "AAPL"
        data = pd.DataFrame({
        "2023-03-10": {
            "1. open": "126.12",
            "2. high": "127.29",
            "3. low": "125.13",
            "4. close": "125.45",
            "5. adjusted close": "125.45",
            "6. volume": "5990867",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        "2023-03-09": {
            "1. open": "128.3",
            "2. high": "128.53",
            "3. low": "125.98",
            "4. close": "126.16",
            "5. adjusted close": "126.16",
            "6. volume": "5478317",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        }})
        api_key = "fake_api_key"
        av = MagicMock()
        av.daily.return_value = (data, {})
        
        # Act
        with patch("__main__.av", av):
            result, table_name = prettified_daily(symbol)
        
        # Assert
        expected_result = pd.DataFrame({
            "Open": [100, 110],
            "High": [120, 130],
            "Low": [90, 95],
            "Close": [105, 115],
            "Volume": [1000, 1500]
        })
        expected_table_name = "AAPL_daily_price_history"
        self.assertTrue(result.equals(expected_result))
        self.assertEqual(table_name, expected_table_name)

    def test_prettified_daily_invalid_symbol(self):
        """Test with an invalid symbol"""
        # Arrange
        symbol = "INVALID_SYMBOL"
        api_key = "fake_api_key"
        av = MagicMock()
        av.daily.side_effect = ValueError("Invalid symbol")
        
        # Act and Assert
        with patch("__main__.av", av):
            with self.assertRaises(ValueError):
                prettified_daily(symbol)
    
    def test_prettified_overview_valid_symbol(self):
        """Test with a valid symbol"""
        # Arrange
        symbol = "IBM"
        data = {
    "Symbol": "IBM",
    "AssetType": "Common Stock",
    "Name": "International Business Machines",
    "Description": "International Business Machines Corporation (IBM) is an American multinational technology company headquartered in Armonk, New York, with operations in over 170 countries. The company began in 1911, founded in Endicott, New York, as the Computing-Tabulating-Recording Company (CTR) and was renamed International Business Machines in 1924. IBM is incorporated in New York. IBM produces and sells computer hardware, middleware and software, and provides hosting and consulting services in areas ranging from mainframe computers to nanotechnology. IBM is also a major research organization, holding the record for most annual U.S. patents generated by a business (as of 2020) for 28 consecutive years. Inventions by IBM include the automated teller machine (ATM), the floppy disk, the hard disk drive, the magnetic stripe card, the relational database, the SQL programming language, the UPC barcode, and dynamic random-access memory (DRAM). The IBM mainframe, exemplified by the System/360, was the dominant computing platform during the 1960s and 1970s.",
    "CIK": "51143",
    "Exchange": "NYSE",
    "Currency": "USD",
    "Country": "USA",
    "Sector": "TECHNOLOGY",
    "Industry": "COMPUTER & OFFICE EQUIPMENT",
    "Address": "1 NEW ORCHARD ROAD, ARMONK, NY, US",
    "FiscalYearEnd": "December",
    "LatestQuarter": "2022-12-31",
    "MarketCapitalization": "112443343000",
    "EBITDA": "12369000000",
    "PERatio": "20.6",
    "PEGRatio": "1.276",
    "BookValue": "24.22",
    "DividendPerShare": "6.59",
    "DividendYield": "0.0523",
    "EPS": "6.09",
    "RevenuePerShareTTM": "67.06",
    "ProfitMargin": "0.0271",
    "OperatingMarginTTM": "0.125",
    "ReturnOnAssetsTTM": "0.0365",
    "ReturnOnEquityTTM": "0.0869",
    "RevenueTTM": "60530000000",
    "GrossProfitTTM": "32688000000",
    "DilutedEPSTTM": "6.09",
    "QuarterlyEarningsGrowthYOY": "0.151",
    "QuarterlyRevenueGrowthYOY": "0",
    "AnalystTargetPrice": "146.76",
    "TrailingPE": "20.6",
    "ForwardPE": "15.55",
    "PriceToSalesRatioTTM": "2.108",
    "PriceToBookRatio": "6.75",
    "EVToRevenue": "2.969",
    "EVToEBITDA": "25.81",
    "Beta": "0.852",
    "52WeekHigh": "151.35",
    "52WeekLow": "112.8",
    "50DayMovingAverage": "136.41",
    "200DayMovingAverage": "135.47",
    "SharesOutstanding": "896320000",
    "DividendDate": "2023-03-10",
    "ExDividendDate": "2023-02-09"
}
        api_key = "fake_api_key"
        av = MagicMock()
        av.company_overview.return_value = (data, {})
        
        # Act
        with patch("__main__.av", av):
            result, table_name = prettified_overview(symbol)
        
        # Assert
        expected_result = pd.DataFrame.from_dict(data, orient='index').T.set_index('Symbol')
        expected_table_name = "IBM_company_overview"
        self.assertTrue(result.equals(expected_result))
        self.assertEqual(table_name, expected_table_name)

    def test_prettified_overview_invalid_symbol(self):
        """Test with an invalid symbol"""
        # Arrange
        symbol = "INVALID_SYMBOL"
        api_key = "fake_api_key"
        av = MagicMock()
        av.company_overview.side_effect = ValueError("Invalid symbol")
        
        # Act and Assert
        with patch("__main__.av", av):
            with self.assertRaises(ValueError):
                prettified_overview(symbol)
        




if __name__ == "__main__":
    unittest.main()