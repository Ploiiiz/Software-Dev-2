import credentials
import pandas
import requests
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.techindicators import TechIndicators

class StocksData:
    ''' Stocks data from AlphaVantage'''
    def __init__(self):
        self.api_key = credentials.av_api_key
        self.outputtype = "pandas"
        self.outputsize = "full"
        self.ts = TimeSeries(self.api_key, output_format=self.outputtype)
        self.ti = TechIndicators(self.api_key, output_format=self.outputtype)
        self.fd = FundamentalData(self.api_key)



    # Time Series
    def intraday(self,symbol:str,interval):
        return self.ts.get_intraday(symbol=symbol,interval=interval,outputsize=self.outputsize)

    def daily_adjusted(self,symbol:str,output='compact'):
        return self.ts.get_daily_adjusted(symbol=symbol,outputsize=output)

    def weekly_adjusted(self,symbol:str):
        return self.ts.get_weekly_adjusted(symbol=symbol)  
    
    def monthly_adjusted(self,symbol:str):
        return self.ts.get_monthly_adjusted(symbol=symbol)


    
    # Technical Indicators
    def ema(self,symbol:str,interval,period,series_type):
        return self.ti.get_ema(symbol,interval,period,series_type)

    def sma(self,symbol:str,interval,period,series_type):
        return self.ti.get_sma(symbol,interval,period,series_type)
    
    def macd(self,symbol:str,interval,period,series_type,*args,**kwargs):
        return self.ti.get_macd(symbol,interval,period,series_type,*args,**kwargs)

    def bbands(self,symbol:str,interval,period,series_type,*args,**kwargs):
        return self.ti.get_bbands(symbol,interval,period,series_type,*args,**kwargs)
    
    def vwap(self,symbol:str,interval):
        return self.ti.get_vwap(symbol,interval)
    
    def aroon(self,symbol,interval,period):
        return self.ti.get_aroon(symbol,interval,period)

    def ad(self,symbol,interval):
        return self.ti.get_ad(symbol,interval)
    
    def obv(self,symbol,interval):
        return self.ti.get_obv(symbol,interval)



    # Fundamental Data
    def overview(self,symbol):
        return self.fd.get_company_overview(symbol)

    def annual_income_statement(self,symbol):
        return self.fd.get_income_statement_annual(symbol)

    def quarterly_income_statement(self,symbol):
        return self.fd.get_income_statement_quarterly(symbol)

    def annual_cash_flow(self,symbol):
        return self.fd.get_cash_flow_annual(symbol)
    
    def quarterly_cash_flow(self,symbol):
        return self.fd.get_cash_flow_quarterly(symbol)
    
    def quarterly_balance_sheet(self,symbol):
        return self.fd.get_balance_sheet_quarterly(symbol)
 
    def annual_balance_sheet(self,symbol):
        return self.fd.get_balance_sheet_annual(symbol)
    
class NewsSentiment:
    def __init__(self) -> None:
        self.api_key = credentials.av_api_key
        self.url = credentials.av_url

    def news(self,tickers=None,topics=None,time_from=None,time_to=None,sort=None,limit=None):
        params = {
        "function"  :   "NEWS_SENTIMENT",
        "apikey"    :   self.api_key,
        "tickers"   :   tickers,
        "topics"    :   topics,
        "time_from" :   time_from,
        "time_to"   :   time_to,
        "sort"      :   sort,
        "limit"     :   limit
        }
        response = requests.request("GET",self.url,params=params)
        json = response.json()

        items = json['items']
        feed = json['feed']
        newsfeed = self._format(feed)
        return (items,newsfeed)

    def _format(self,content):
        return pandas.DataFrame.from_dict(content)

    def filter_sentiments(self,feed,sentiment_label):
        return feed[feed['overall_sentiment_label']==sentiment_label]
    
    #Future Module
    def view_ticker_relevance(self,news):
        return None 
