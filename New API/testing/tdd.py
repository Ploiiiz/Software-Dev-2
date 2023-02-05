import unittest
from unittest.mock import Mock, patch
import requests
import credentials
import pandas as pd
import json
# Module for fetching data and formatting
import fetch
# Module for database

#
from pymongo import MongoClient
import datetime


api_key = credentials.av_api_key
ts = fetch.timeseries
fd = fetch.fundamentals
ti = fetch.indicators
ns = fetch.news
test_symbol = 'AAPL'
invalid_symbol = 'INVALID_SYMBOL'


get_mock = Mock()
data = {
    "2023-01-26": {
        "1. open": "137.53",
        "2. high": "138.27",
        "3. low": "132.98",
        "4. close": "134.45",
        "5. adjusted close": "134.45",
        "6. volume": "17548483",
        "7. dividend amount": "0.0000",
        "8. split coefficient": "1.0"
    },
    "2023-01-25": {
        "1. open": "140.47",
        "2. high": "141.03",
        "3. low": "139.36",
        "4. close": "140.76",
        "5. adjusted close": "140.76",
        "6. volume": "7347453",
        "7. dividend amount": "0.0000",
        "8. split coefficient": "1.0"
    },
    "2023-01-24": {
        "1. open": "141.25",
        "2. high": "142.75",
        "3. low": "140.0",
        "4. close": "141.49",
        "5. adjusted close": "141.49",
        "6. volume": "4407622",
        "7. dividend amount": "0.0000",
        "8. split coefficient": "1.0"
    }
}
metadata = {
    "1. Information": "Intraday (5min) open, high, low, close prices and volume",
    "2. Symbol": "IBM",
    "3. Last Refreshed": "2023-01-26 20:00:00",
    "4. Interval": "5min",
    "5. Output Size": "Compact",
    "6. Time Zone": "US/Eastern"
}
df = fetch.to_dataframe(data)
df.index = pd.to_datetime(df.index)
get_mock.return_value = (df, metadata)

fd_mock_a = Mock()
fd_data_a = {"symbol": "IBM",
             "annualReports": [
                 {
                     "fiscalDateEnding": "2021-12-31",
                     "reportedCurrency": "USD",
                     "grossProfit": "31486000000",
                     "totalRevenue": "57350000000",
                     "costOfRevenue": "25865000000",
                     "costofGoodsAndServicesSold": "300000000",
                     "operatingIncome": "4786000000",
                     "sellingGeneralAndAdministrative": "18745000000",
                     "researchAndDevelopment": "6488000000",
                     "operatingExpenses": "26700000000",
                     "investmentIncomeNet": "None",
                     "netInterestIncome": "-1155000000",
                     "interestIncome": "52000000",
                     "interestExpense": "1155000000",
                     "nonInterestIncome": "None",
                     "otherNonOperatingIncome": "-873000000",
                     "depreciation": "3888000000",
                     "depreciationAndAmortization": "2529000000",
                     "incomeBeforeTax": "5867000000",
                     "incomeTaxExpense": "124000000",
                     "interestAndDebtExpense": "1155000000",
                     "netIncomeFromContinuingOperations": "4712000000",
                     "comprehensiveIncomeNetOfTax": "11299000000",
                     "ebit": "7022000000",
                     "ebitda": "9551000000",
                     "netIncome": "5743000000"
                 }]
             }
fd_df = pd.DataFrame.from_dict(fd_data_a["annualReports"])
fd_df.index = pd.to_datetime(fd_df.index)
fd_mock_a.return_value = (fd_df, fd_data_a["symbol"])

overview = {"Symbol": "IBM",
            "AssetType": "Common Stock",
            "Name": "International Business Machines",
            "Description": "International Business Machines Corporation (IBM) is an American multinational technology company headquartered in Armonk, New York, with operations in over 170 countries. The company began in 1911, founded in Endicott, New York, as the Computing-Tabulating-Recording Company (CTR) and was renamed International Business Machines in 1924. IBM is incorporated in New York. IBM produces and sells computer hardware, middleware and software, and provides hosting and consulting services in areas ranging from mainframe computers to nanotechnology. IBM is also a major research organization, holding the record for most annual U.S. patents generated by a business (as of 2020) for 28 consecutive years. Inventions by IBM include the automated teller machine (ATM), the floppy disk, the hard disk drive, the magnetic stripe card, the relational database, the SQL programming language, the UPC barcode, and dynamic random-access memory (DRAM). The IBM mainframe, exemplified by the System/360, was the dominant computing platform during the 1960s and 1970s.",
            "CIK": "51143"}

ti_mock = Mock()
ti_mock_data = {
    "2023-01-27": {
        "SMA": "144.6180"
    },
    "2023-01-20": {
        "SMA": "144.7410"
    }
}
ti_meta = {
    "1: Symbol": "IBM",
    "2: Indicator": "Simple Moving Average (SMA)",
    "3: Last Refreshed": "2023-01-27",
    "4: Interval": "weekly",
    "5: Time Period": 10,
    "6: Series Type": "open",
    "7: Time Zone": "US/Eastern"
}
ti_df = fetch.to_dataframe(ti_mock_data)
ti_df.index = pd.to_datetime(ti_df.index)
ti_mock.return_value = (ti_df, ti_meta)

with open('testing/news.json') as file:
    newsdata = json.load(file)

# @patch('alpha_vantage.timeseries.TimeSeries.get_intraday', get_mock)
# @patch('alpha_vantage.timeseries.TimeSeries.get_daily_adjusted', get_mock)
# @patch('alpha_vantage.fundamentaldata.FundamentalData.get_income_statement_quarterly', fd_mock_a)
# @patch('alpha_vantage.fundamentaldata.FundamentalData.get_balance_sheet_quarterly', fd_mock_a)
# @patch('alpha_vantage.fundamentaldata.FundamentalData.get_cash_flow_quarterly', fd_mock_a)
@patch('requests.get',rqmock)
class TestFetching(unittest.TestCase):
    def test_connection(self):
        req = requests.get("https://www.example.com/")
        self.assertEqual(req.status_code, 200)

    # Historical Stocks Data
    def test_intraday(self):
        data = ts.get_intraday(test_symbol)
        self.assertIsInstance(data, tuple)
        self.assertIsInstance(data[0], pd.DataFrame)
        self.assertIsInstance(data[1], dict)

    def test_dailyadj(self):
        data = ts.get_daily_adjusted(test_symbol)
        self.assertIsInstance(data, tuple)
        self.assertIsInstance(data[0], pd.DataFrame)
        self.assertIsInstance(data[1], dict)

    def test_cut_columns(self):
        data, meta = ts.get_daily_adjusted(test_symbol)
        data = fetch.cut_and_rename_col(data)
        self.assertEqual(data.shape, (3, 6))
        self.assertListEqual(list(data.columns), [
                             'open', 'high', 'low', 'close', 'adjusted close', 'volume'])

    def test_sort(self):
        data, meta = ts.get_daily_adjusted(test_symbol)
        data = fetch.cut_and_rename_col(data)
        data = fetch.sort_date_asc(data)
        self.assertTrue(data.index.is_monotonic_increasing)

    # Fundamental Data
    def test_income_statement(self):
        data, sym = fd.get_income_statement_quarterly(test_symbol)
        self.assertIsInstance(data, pd.DataFrame)

    def test_balance_sheet(self):
        data, sym = fd.get_balance_sheet_quarterly(test_symbol)
        self.assertIsInstance(data, pd.DataFrame)

    def test_cash_flow(self):
        data, sym = fd.get_cash_flow_quarterly(test_symbol)
        self.assertIsInstance(data, pd.DataFrame)

    def test_overview(self):
        data, sym = fd.get_company_overview(test_symbol)
        self.assertIsInstance(data, dict)

    # Technical indicators
    @patch('alpha_vantage.techindicators.TechIndicators.get_sma', ti_mock)
    def test_sma(self):
        data, meta = ti.get_sma(test_symbol)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertListEqual(list(data.columns),['SMA'])
        self.assertIsInstance(data.index[0],datetime.datetime)

    @patch('alpha_vantage.techindicators.TechIndicators.get_ema', ti_mock)
    def test_ema(self):
        data, meta = ti.get_ema(test_symbol)
        self.assertIsInstance(data, pd.DataFrame)

    @patch('alpha_vantage.techindicators.TechIndicators.get_vwap', ti_mock)
    def test_vwap(self):
        data, meta = ti.get_vwap(test_symbol)
        self.assertIsInstance(data, pd.DataFrame)

    @patch('alpha_vantage.techindicators.TechIndicators.get_macd', ti_mock)
    def test_macd(self):
        data, meta = ti.get_macd(test_symbol)
        self.assertIsInstance(data, pd.DataFrame)

    @patch('alpha_vantage.techindicators.TechIndicators.get_aroon', ti_mock)
    def test_aroon(self):
        data, meta = ti.get_aroon(test_symbol)
        self.assertIsInstance(data, pd.DataFrame)

    @patch('alpha_vantage.techindicators.TechIndicators.get_bbands', ti_mock)
    def test_bband(self):
        data, meta = ti.get_bbands(test_symbol,)
        self.assertIsInstance(data, pd.DataFrame)

    @patch('alpha_vantage.techindicators.TechIndicators.get_ad', ti_mock)
    def test_ad(self):
        data, meta = ti.get_ad(test_symbol,)
        self.assertIsInstance(data, pd.DataFrame)

    @patch('alpha_vantage.techindicators.TechIndicators.get_obv', ti_mock)
    def test_obv(self):
        data, meta = ti.get_obv(test_symbol,)
        self.assertIsInstance(data, pd.DataFrame)

    # News Sentiment
    # @patch('requests.get')
    # def test_news(self,mock_get):
    #     rq = Mock()
    #     rq.json.return_value = newsdata
    #     mock_get.return_value = rq

    #     data, meta = ns.news()
    #     self.assertIsInstance(data,pd.DataFrame)

    

if __name__ == "__main__":
    unittest.main()
