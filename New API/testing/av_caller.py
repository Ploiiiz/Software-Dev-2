from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators


def daily(api_key,symbol,output_format='pandas',outputsize='full'):
    daily = TimeSeries(api_key,output_format).get_daily_adjusted(symbol,outputsize)
    return daily

def weekly(api_key,symbol,output_format='pandas'):
    weekly = TimeSeries(api_key,output_format).get_weekly_adjusted(symbol)
    return weekly

def monthly(api_key,symbol,output_format='pandas'):
    monthly = TimeSeries(api_key,output_format).get_monthly_adjusted(symbol)
    return monthly

def macd_daily(api_key,symbol):
    macd = TechIndicators(api_key).get_macd(symbol,'daily')
    return macd

def macd_weekly(api_key,symbol):
    macd = TechIndicators(api_key).get_macd(symbol,'weekly')
    return macd

def macd_monthly(api_key,symbol):
    macd = TechIndicators(api_key).get_macd(symbol,'monthly')
    return macd

def sma(api_key,symbol,interval):
    sma = TechIndicators(api_key).get_sma(symbol,interval)
    return sma

def bbands(api_key,symbol,interval,series_type='close'):
    bbands = TechIndicators(api_key).get_bbands(symbol,interval,period,series_type)
    return bbands