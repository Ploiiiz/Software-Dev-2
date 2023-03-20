import yahoo_fin.stock_info as si
import yfinance as yf
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries
import pandas
from datetime import datetime
import pandas_ta as ta
import os
import db_utils
from dotenv import load_dotenv
# sys.path.append('..')
# from src import data_crypto

load_dotenv()
av_key = os.getenv('AV_API_KEY')
fd = FundamentalData(av_key)
ts = TimeSeries(av_key)

def check_available(symbol):
    try:
        # df = si.get_data(symbol)
        df2 = yf.Ticker(symbol).history(interval='1h')
        if not df2.empty:
            return symbol.upper()
        else:
            raise Exception
    except:
        print('Trying thai symbol')
        try:
            symbol = symbol+'.BK'
            # df = si.get_data(symbol)
            df2 = yf.Ticker(symbol).history(interval='1h')
            if not df2.empty:
                return symbol.upper()
            else:
                raise Exception
        except:
            return None

def get_hourly_data(symbol):
    '''
        Returns a dataframe of a symbol with ema200 and sma50
        Also table name for saving (later)
    '''
    symbol = symbol.upper()
    table_name = symbol+'_hourly_price_history'
    ticker = yf.Ticker(symbol)
    df = ticker.history(interval='1h')
    if df.empty: # Maybe a Thai stock?
        symbol = symbol+'.BK'
        ticker = yf.Ticker(symbol)
        df = ticker.history(interval='1h')
        if df.empty: # Not even Thai
            return None,table_name
    sma50 = df.ta.sma(length=50, append=True)
    # ema200 = df.ta.ema(length=200, append=True)
    df = df.apply(lambda x: round(x, 3) if x.dtype == 'float64' else x)
    df.columns = [i.lower() for i in df.columns]
    df = df.rename(columns={'sma_50':'SMA_50'})
    df.index = df.index.tz_localize(None)
    return df,table_name

def get_daily_data(symbol):
    '''
        Returns a dataframe of a symbol with ema200 and sma50
        Also table name for saving (later)
    '''
    symbol = symbol.upper()
    table_name = symbol+'_daily_price_history'
    try:
        df = si.get_data(symbol)
        sma50 = df.ta.sma(length=50, append=True)
        ema200 = df.ta.ema(length=200, append=True)
        df = df.apply(lambda x: round(x, 3) if x.dtype == 'float64' else x)
        return df,table_name
    except:
        try:
            symbol = symbol + '.BK'
            table_name = symbol+'_daily_price_history'
            df = si.get_data(symbol)
            sma50 = df.ta.sma(length=50, append=True)
            ema200 = df.ta.ema(length=200, append=True)
            df = df.apply(lambda x: round(x, 3) if x.dtype == 'float64' else x)
            return df,table_name
        except:
            return None,table_name

def get_weekly_data(symbol):
    '''
        Returns a dataframe of a symbol with ema200 and sma50
        Also table name for saving (later)
    '''
    symbol = symbol.upper()
    table_name = symbol+'_weekly_price_history'
    try:
        df = si.get_data(symbol,interval='1wk')
        sma50 = df.ta.sma(length=50, append=True)
        ema200 = df.ta.ema(length=200, append=True)
        df = df.apply(lambda x: round(x, 3) if x.dtype == 'float64' else x)
        return df,table_name
    except:
        try:
            symbol = symbol + '.BK'
            table_name = symbol+'_weekly_price_history'
            df = si.get_data(symbol,interval='1wk')
            sma50 = df.ta.sma(length=50, append=True)
            ema200 = df.ta.ema(length=200, append=True)
            df = df.apply(lambda x: round(x, 3) if x.dtype == 'float64' else x)
            return df,table_name
        except:
            return None,table_name
  

def get_monthly_data(symbol):
    '''
        Returns a dataframe of a symbol with ema200 and sma50
        Also table name for saving (later)
    '''
    symbol = symbol.upper()
    table_name = symbol+'_monthly_price_history'
    try:
        df = si.get_data(symbol, interval='1mo')
        sma50 = df.ta.sma(length=50, append=True)
        ema200 = df.ta.ema(length=200, append=True)
        df = df.apply(lambda x: round(x, 3) if x.dtype == 'float64' else x)
        return df,table_name
    except:
        try:
            symbol = symbol + '.BK'
            table_name = symbol+'_monthly_price_history'
            df = si.get_data(symbol, interval='1mo')
            sma50 = df.ta.sma(length=50, append=True)
            ema200 = df.ta.ema(length=200, append=True)
            df = df.apply(lambda x: round(x, 3) if x.dtype == 'float64' else x)
            return df,table_name
        except:
            return None,table_name
        
def txt_to_list(path,filename):
    with open(os.path.join(path,filename),'r') as file:
        items = []
        for line in file:
            line = line.strip()
            items.append(line)
        return items

def append_one(path,filename,item):
    with open(os.path.join(path,filename),'a') as f:
        f.write(item + '\n')
        f.close()

def delete_one(path,filename,item):
    with open(os.path.join(path,filename),'r') as f:
        content = f.readlines()
        content.remove(item+'\n')

    with open(os.path.join(path,filename),'w') as f:
        for i in content:
            f.write(i)    

def delete_all_table(symbol):
    table_name_suffix = ['_hourly_price_history','_daily_price_history','_weekly_price_history','_monthly_price_history']
    for i in table_name_suffix:
        db_utils.delete_table(symbol+i)

def read_all(symbol):
    table_name_suffix = ['_hourly_price_history','_daily_price_history','_weekly_price_history','_monthly_price_history']
    all_data = []
    for i in table_name_suffix:
        all_data.append(db_utils.read_table(symbol+i))
    return all_data

def quote(symbol):
    ts = TimeSeries(av_key)
    quote2 = si.get_quote_data(symbol)
    try:
        quote_info, meta = ts.get_quote_endpoint('AAPL')
        exchange, fullname = quote2['exchange'],quote2['longName']
        if exchange == 'NMS':
            exchange = 'NASDAQ'
        b = list(quote_info.values())
        opn,high,low,prevclose,price,change,changeper,vol = b[1],b[2],b[3],b[7],b[4],b[8],b[9],b[5]
        return fullname,exchange,opn,high,low,prevclose,price,change,changeper,vol
    except:
        return None
