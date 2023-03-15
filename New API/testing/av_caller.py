from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.fundamentaldata import FundamentalData
# from alpha_vantage.sectorperformance import SectorPerformance
import requests
# Price ----------------------------------------------------------------
def daily(api_key,symbol,output_format='pandas',outputsize='full'):
    try:
        daily = TimeSeries(api_key,output_format).get_daily_adjusted(symbol,outputsize)
        return daily
    except Exception:
        return None

def weekly(api_key,symbol,output_format='pandas'):
    try:
        weekly = TimeSeries(api_key,output_format).get_weekly_adjusted(symbol)
        return weekly
    except Exception:
        return None

def monthly(api_key,symbol,output_format='pandas'):
    try:
        monthly = TimeSeries(api_key,output_format).get_monthly_adjusted(symbol)
        return monthly
    except Exception:
        return None

# Fundamentaldata ----------------------------------------------------------------
def company_overview(api_key,symbol):
    try:
        comp = FundamentalData(api_key).get_company_overview(symbol)
        return comp
    except Exception:
        return None

def income_statement_annual(api_key,symbol):
    try:
        income_statement = FundamentalData(api_key).get_income_statement_annual(symbol)
        return income_statement
    except Exception:
        return None

def income_statement_quarterly(api_key, symbol):
    try:
        income_statement = FundamentalData(api_key).get_income_statement_quarterly(symbol)
        return income_statement
    except Exception:
        return None

def balance_sheet_annual(api_key, symbol):
    try:
        balance_sheet = FundamentalData(api_key).get_balance_sheet_annual(symbol)
        return balance_sheet
    except Exception:
        return None

def balance_sheet_quarterly(api_key, symbol):
    try:
        balance_sheet = FundamentalData(api_key).get_balance_sheet_quarterly(symbol)
        return balance_sheet
    except Exception:
        return None

def cash_flow_annual(api_key, symbol):
    try:
        cash_flow = FundamentalData(api_key).get_cash_flow_annual(symbol)
        return cash_flow
    except Exception:
        return None

def cash_flow_quarterly(api_key, symbol):
    try:
        cash_flow = FundamentalData(api_key).get_cash_flow_quarterly(symbol)
        return cash_flow
    except Exception:
        return None

# Technical Indicators -------------------------------------------------------------
def macd_daily(api_key,symbol):
    try:
        macd = TechIndicators(api_key).get_macd(symbol,'daily')
        return macd
    except Exception:
        return None

def macd_weekly(api_key,symbol):
    try:
        macd = TechIndicators(api_key).get_macd(symbol,'weekly')
        return macd
    except Exception:
        return None

def macd_monthly(api_key,symbol):
    try:
        macd = TechIndicators(api_key).get_macd(symbol,'monthly')
        return macd
    except Exception:
        return None

def sma_daily(api_key,symbol):
    try:
        sma = TechIndicators(api_key).get_sma(symbol,'daily')
        return sma
    except Exception:
        return None

def sma_weekly(api_key,symbol):
    try:
        sma = TechIndicators(api_key).get_sma(symbol,'weekly')
        return sma
    except Exception:
        return None

def sma_monthly(api_key,symbol):
    try:
        sma = TechIndicators(api_key).get_sma(symbol,'monthly')
        return sma
    except Exception:
        return None

def ema_daily(api_key,symbol):
    try:
        ema = TechIndicators(api_key).get_ema(symbol,'daily')
        return ema
    except Exception:
        return None

def ema_weekly(api_key,symbol):
    try:
        ema = TechIndicators(api_key).get_ema(symbol,'weekly')
        return ema
    except Exception:
        return None

def ema_monthly(api_key,symbol):
    try:
        ema = TechIndicators(api_key).get_ema(symbol,'monthly')
        return ema
    except Exception:
        return None

def bbands_daily(api_key,symbol):
    try:
        bbands = TechIndicators(api_key).get_bbands(symbol,'daily')
        return bbands
    except Exception:
        return None

def bbands_weekly(api_key, symbol):
    try:
        bbands = TechIndicators(api_key).get_bbands(symbol, 'weekly')
        return bbands
    except Exception:
        return None

def bbands_monthly(api_key, symbol):
    try:
        bbands = TechIndicators(api_key).get_bbands(symbol, 'monthly')
        return bbands
    except Exception:
        return None

# News ----------------------------------------------------------------

def news(api_key,tickers=None,topics=None,time_from=None,time_to=None,sort=None,limit=None):
    try:
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
        feed = json['feed']
        return feed
    except Exception as e:
        return None

# Quote Endpoints
def quote_endpoint(api_key,symbol):
    try:
        quote = TimeSeries(api_key).get_quote_endpoint(symbol)
        return quote
    except Exception:
        return None
