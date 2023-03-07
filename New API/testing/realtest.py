import credentials
import av_caller
import transformer
import bson

key = credentials.av_api_key
sym = 'AAPL'

def daily_data(api_key, symbol):
    data,meta = av_caller.daily(api_key,symbol)
    data = transformer.rename_price(data)
    return data,meta

def weekly_data(api_key, symbol):
    data,meta = av_caller.weekly(api_key,symbol)
    data = transformer.rename_price(data)
    return data,meta

def monthly_data(api_key, symbol):
    data,meta = av_caller.monthly(api_key,symbol)
    data = transformer.rename_price(data)
    return data,meta

def validDate(df):
    date = list(df.index)[0]
    return type(date) == bson.datetime.datetime