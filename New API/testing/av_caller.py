from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.fundamentaldata import FundamentalData
# from alpha_vantage.sectorperformance import SectorPerformance
import requests

def daily(api_key,symbol,output_format='pandas',outputsize='full'):
    daily = TimeSeries(api_key,output_format).get_daily_adjusted(symbol,outputsize)
    return daily

def weekly(api_key,symbol,output_format='pandas'):
    weekly = TimeSeries(api_key,output_format).get_weekly_adjusted(symbol)
    return weekly

def monthly(api_key,symbol,output_format='pandas'):
    monthly = TimeSeries(api_key,output_format).get_monthly_adjusted(symbol)
    return monthly

def quote_endpoint(api_key,symbol):
    quote = TimeSeries(api_key).get_quote_endpoint(symbol)
    return quote[0]

def macd_daily(api_key,symbol):
    macd = TechIndicators(api_key).get_macd(symbol,'daily')
    return macd

def macd_weekly(api_key,symbol):
    macd = TechIndicators(api_key).get_macd(symbol,'weekly')
    return macd

def macd_monthly(api_key,symbol):
    macd = TechIndicators(api_key).get_macd(symbol,'monthly')
    return macd

def sma_daily(api_key,symbol):
    sma = TechIndicators(api_key).get_sma(symbol,'daily')
    return sma

def sma_weekly(api_key,symbol):
    sma = TechIndicators(api_key).get_sma(symbol,'weekly')
    return sma

def sma_monthly(api_key,symbol):
    sma = TechIndicators(api_key).get_sma(symbol,'monthly')
    return sma

def ema_daily(api_key,symbol):
    ema = TechIndicators(api_key).get_ema(symbol,'daily')
    return ema

def ema_weekly(api_key,symbol):
    ema = TechIndicators(api_key).get_ema(symbol,'weekly')
    return ema

def ema_monthly(api_key,symbol):
    ema = TechIndicators(api_key).get_ema(symbol,'monthly')
    return ema

def bbands_daily(api_key,symbol):
    bbands = TechIndicators(api_key).get_bbands(symbol,'daily')
    return bbands

def bbands_weekly(api_key, symbol):
    bbands = TechIndicators(api_key).get_bbands(symbol, 'weekly')
    return bbands

def bbands_monthly(api_key, symbol):
    bbands = TechIndicators(api_key).get_bbands(symbol, 'monthly')
    return bbands

def news(api_key,tickers=None,topics=None,time_from=None,time_to=None,sort=None,limit=None):
        url = "https://www.alphavantage.co/query"
        params = {
        "function"  :   "NEWS_SENTIMENT",
        "apikey"    :   api_key,
        "tickers"   :   tickers,
        "topics"    :   topics,
        "time_from" :   time_from,
        "time_to"   :   time_to,
        "sort"      :   sort,
        "limit"     :   limit
        }
        response = requests.request("GET",url,params=params)
        json = response.json()

        items = json['items']
        feed = json['feed']
        return (feed,items)

def company_overview(api_key,symbol):
    comp = FundamentalData(api_key).get_company_overview(symbol)
    return comp

def income_statement_annual(api_key,symbol):
    income_statement = FundamentalData(api_key).get_income_statement_annual(symbol)
    return income_statement