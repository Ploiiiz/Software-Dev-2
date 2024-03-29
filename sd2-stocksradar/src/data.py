import yahoo_fin.stock_info as si
import yfinance as yf
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries
import requests
from datetime import datetime
import pandas_ta as ta
import os
import db_utils
from dotenv import load_dotenv
import spacy
import pandas as pd
import geopandas as gpd 
import geopy 
from geopy.extra.rate_limiter import RateLimiter
# sys.path.append('..')
# from src import data_crypto

load_dotenv()
av_key = os.getenv('AV_API_KEY')
finage_key = os.getenv('FINAGE_API_KEY')
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
    df = df.apply(lambda x: round(x,6) if x.dtype == 'float64' else x)
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
        df = df.apply(lambda x: round(x,6) if x.dtype == 'float64' else x)
        return df,table_name
    except:
        try:
            symbol = symbol + '.BK'
            table_name = symbol+'_daily_price_history'
            df = si.get_data(symbol)
            sma50 = df.ta.sma(length=50, append=True)
            ema200 = df.ta.ema(length=200, append=True)
            df = df.apply(lambda x: round(x,6) if x.dtype == 'float64' else x)
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
        df = df.apply(lambda x: round(x,6) if x.dtype == 'float64' else x)
        return df,table_name
    except:
        try:
            symbol = symbol + '.BK'
            table_name = symbol+'_weekly_price_history'
            df = si.get_data(symbol,interval='1wk')
            sma50 = df.ta.sma(length=50, append=True)
            ema200 = df.ta.ema(length=200, append=True)
            df = df.apply(lambda x: round(x,6) if x.dtype == 'float64' else x)
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
        df = df.apply(lambda x: round(x,6) if x.dtype == 'float64' else x)
        return df,table_name
    except:
        try:
            symbol = symbol + '.BK'
            table_name = symbol+'_monthly_price_history'
            df = si.get_data(symbol, interval='1mo')
            sma50 = df.ta.sma(length=50, append=True)
            ema200 = df.ta.ema(length=200, append=True)
            df = df.apply(lambda x: round(x,6) if x.dtype == 'float64' else x)
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
    table_name_suffix = ['_hourly_price_history','_daily_price_history','_weekly_price_history','_monthly_price_history'
                         ,'_news','_company_overview',
                         '_cash_flow','_balance_sheet','_income_statement']
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
        exchange, fullname = quote2['exchange'],quote2['longName']
        try:
            quote_info, meta = ts.get_quote_endpoint(symbol)
            if exchange == 'NMS':
                exchange = 'NASDAQ'
            b = list(quote_info.values())
            opn,high,low,prevclose,price,change,changeper,vol = b[1],b[2],b[3],b[7],b[4],b[8],b[9],b[5]
            return fullname,exchange,opn,high,low,prevclose,price,change,changeper,vol
        except:
            return fullname,exchange,None,None,None,None,None,None,None,None
    except:
        return None,None,None,None,None,None,None,None,None,None

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

def extract_news_info(news_data):
    headline = news_data['title']
    url = news_data['url']
    source = news_data['source']
    timestamp = news_data['time_published']
    timestamp = datetime.strptime(timestamp, '%Y%m%dT%H%M%S')
    tags = [topic['topic'] for topic in news_data['topics']]
    tickers = [ticker_sentiment['ticker'] for ticker_sentiment in news_data['ticker_sentiment']]
    summary = news_data['summary']
    sentiment_score = news_data['overall_sentiment_score']
    sentiment_label = news_data['overall_sentiment_label']
    return headline, url, source, timestamp, summary, sentiment_score, sentiment_label

def extract_news_feed(news_feed):
    news_list = []
    for i in news_feed:
        news_list.append(tuple(extract_news_info(i)))
    return news_list

def fetch_news(ticker,limit=200):
    try:
        data = db_utils.read_table(ticker+'_news')
        data = data.reset_index()
        data = data.reindex(columns=['headline', 'url', 'source', 'timestamp', 'summary', 'sentiment_score', 'sentiment_label'])
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data_list = data.values.tolist()
        if 'not found' in data: 
            raise Exception
        return data_list,data
    except Exception as e:
        # print(e)
        data = news(api_key=av_key,
                    tickers=ticker,
                    limit=limit)
    if data is not None:
        feed = extract_news_feed(data)
        try:
            df = pd.DataFrame(feed, columns=['headline', 'url', 'source', 'timestamp', 'summary', 'sentiment_score', 'sentiment_label'])
            df = df.set_index('timestamp')
            db_utils.store_table(df,ticker+'_news')
            print('fetch news')
            return feed,df
        except Exception as e:
            print(e)
            return None
    else:
        return None
    
def clean(item):
    if item == 'U.S.':
        return 'America'
    else:
        return item
def add_coord(df):
    locations = []
    try:
        nlp_wk = spacy.load('en_core_web_lg')
        for body in df['summary']:
            doc = nlp_wk(body)
            locations.extend([[body, ent.text] for ent in doc.ents if (ent.label_ in ['LOC'] or ent.label_ in ['GPE'])])
        locations_df = pd.DataFrame(locations, columns=['File', 'Location'])
        locations_df['Location']= locations_df['Location'].apply(clean) 
        locator = geopy.geocoders.Nominatim(user_agent='mygeocoder')
        geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
        locations_df['address'] = locations_df['Location'].apply(geocode)
        locations_df['coordinates'] = locations_df['address'].apply(lambda loc: tuple(loc.point) if loc else None)
        locations_df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(locations_df['coordinates'].tolist(), index=locations_df.index)
        locations_df.latitude.isnull().sum()
        locations_df = locations_df[pd.notnull(locations_df['latitude'])]
        return locations_df
    except OSError:
        print('python -m spacy download xx_ent_wiki_sm')
    
def time_since(datetime_obj):
    now = datetime.now(datetime_obj.tzinfo)
    delta = now - datetime_obj
    days = delta.days
    seconds = delta.seconds
    minutes = seconds // 60
    hours = minutes // 60
    
    if days > 0:
        if days == 1:
            return "1 day ago"
        else:
            return f"{days} days ago"
    elif hours > 0:
        if hours == 1:
            return "1 hour ago"
        else:
            return f"{hours} hours ago"
    elif minutes > 0:
        if minutes == 1:
            return "1 minute ago"
        else:
            return f"{minutes} minutes ago"
    else:
        return "just now"

def load_overview(symbol):
    try:
        table_name = symbol+'_company_overview'
        df = db_utils.read_table(table_name)
        if type(df) != pd.DataFrame:
            raise Exception
        return df
    except Exception:
        ov_tuple = overview(symbol)
        if ov_tuple != None:
            df,table_name = ov_tuple
            db_utils.store_table(df,table_name)
            return df
        else:
            return None
        
def overview(symbol):
    try:
        data, meta = fd.get_company_overview(symbol)
        data = pd.DataFrame.from_dict(data, orient='index').T.set_index('Symbol')
        table_name = symbol + '_company_overview'
        return data,table_name
    except Exception as e:
        return None
    
def color_alpha(color,value):
    old_min, old_max = abs(value).min(), abs(value).max()
    col = []
    for i in range(len(color)):
        new_value = (value[i] - old_min) / (old_max - old_min) * 1
        if color[i] == 'red':
            col.append('rgba(255,0,0,%.2f)'%abs(new_value))
        else:
            col.append('rgba(0,255,0,%.2f)'%abs(new_value))
    return col

def colored_sector_df(df):
    df['change_percentage'] = [float(i[:-1]) for i in df['change_percentage']]
    df['cp'] = abs(df['change_percentage'])
    df['sign'] = df['change_percentage'].apply(lambda x: '-' if x < 0 else '+')
    df['color'] = df['sign'].apply(lambda x: 'red' if x == '-' else 'green')
    df['color'] = color_alpha(df['color'],df['change_percentage'])
    df['parents'] = 'all'
    df.loc[len(df.index)] = ['all', 0, 0,'','',''] 
    return df

def get_sector():
    try:
        table_name = 'sectors_performance'
        df = db_utils.read_table(table_name)
        if 'not found' not in df:
            return df
        else:
            raise Exception
    except:
        try:
            url = 'https://api.finage.co.uk/market-information/us/sector-performance'
            params = {    
            "apikey"    :   finage_key,
            }
            response = requests.request("GET",url,params=params)
            json = response.json()
            df = pd.DataFrame(json)
            db_utils.store_table(df,'sectors_performance')
            return df
        except Exception as e:
            return None

def get_balance_sheet(symbol):
    try:
        table_name = symbol+'_balance_sheet'
        bal = db_utils.read_table(table_name)
        if 'not found' not in bal:
            return bal
        else:
            raise Exception
    except:
        try:
            full_bal, meta = fd.get_balance_sheet_quarterly(symbol)
            crucial_bal = full_bal[['fiscalDateEnding','totalAssets','totalLiabilities','totalShareholderEquity','reportedCurrency']]
            db_utils.store_table(crucial_bal,symbol+'_balance_sheet')
            return crucial_bal
        except:
            return None
        
def get_income_statement(symbol):
    try:
        table_name = symbol+'_income_statement'
        income = db_utils.read_table(table_name)
        if 'not found' not in income:
            return income
        else:
            raise Exception
    except:
        try:
            full_income, meta = fd.get_income_statement_quarterly(symbol)
            crucial_income = full_income[['fiscalDateEnding','reportedCurrency','grossProfit', 'totalRevenue', 'costOfRevenue','operatingIncome','netIncome']]
            db_utils.store_table(crucial_income,symbol+'_income_statement')
            return crucial_income
        except:
            return None

def get_cash_flow(symbol):
    try:
        table_name = symbol+'_cash_flow'
        cash = db_utils.read_table(table_name)
        if 'not found' not in cash:
            return cash
        else:
            raise Exception
    except:
        try:
            full_cash, meta = fd.get_cash_flow_quarterly(symbol)
            crucial_cash = full_cash[['fiscalDateEnding','reportedCurrency','operatingCashflow','cashflowFromInvestment', 'cashflowFromFinancing','changeInCashAndCashEquivalents', 'netIncome']]
            db_utils.store_table(crucial_cash,symbol+'_cash_flow')
            return crucial_cash
        except:
            return None
        