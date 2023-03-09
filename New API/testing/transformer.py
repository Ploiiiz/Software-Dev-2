from datetime import datetime
import pandas as pd

def rename_price_columns(dataframe):
    df = dataframe
    df.index.names = ['timestamp']
    df.columns = [i[3:].replace(' ','_') for i in df.columns]
    if 'split_coefficient' in df.columns:
        df = df.drop('split_coefficient', axis=1)
    return df

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
    return headline, url, source, timestamp, tags, tickers, summary, sentiment_score, sentiment_label

def extract_news_feed(news_feed,item):
    news_list = []
    for i in news_feed:
        news_list.append(tuple(extract_news_info(i)))
    return news_list

def extract_price_metadata(metadata):
    interval = metadata['1. Information'].split(' ')[0]
    symbol = metadata['2. Symbol']
    last_refreshed = metadata['3. Last Refreshed']
    return (symbol.upper(), interval.lower(), last_refreshed)

def prettify_price(dataframe, metadata):
    data = rename_price_columns(dataframe)
    meta = extract_price_metadata(metadata)
    return data, meta

def parse_quote(stock_data):
    symbol = stock_data['01. symbol']
    open_price = stock_data['02. open']
    high_price = stock_data['03. high']
    low_price = stock_data['04. low']
    current_price = stock_data['05. price']
    volume = stock_data['06. volume']
    trading_day = stock_data['07. latest trading day']
    previous_close = stock_data['08. previous close']
    change = stock_data['09. change']
    change_percent = stock_data['10. change percent']
    return (symbol, open_price, high_price, low_price, current_price, volume, trading_day, previous_close, change, change_percent)

def minimal_parse(stock_data):
    symbol = stock_data['01. symbol']
    current_price = stock_data['05. price'][:-2]
    volume = 'Vol'+stock_data['06. volume'][:-2]
    previous_close = stock_data['08. previous close'][:-2]

    if float(current_price) > float(previous_close):
        sign = '+'
    else:
        sign = '-'   

    change = stock_data['09. change'][:-2]
    change_percent = sign+stock_data['10. change percent'][:-2]
    totalchange = change_percent+'%'+'('+change+')' 

    return (symbol, symbol, '$'+current_price, totalchange, volume)

def prettify_tech(data,meta):
    data = pd.DataFrame.from_dict(data, 'index')
    data.index.names = ['timestamp']    
    meta = pd.DataFrame.from_dict(meta,'index')
    meta.index = [i[2:] for i in meta.index]
    symbol = meta[0][0]
    indicator = meta[0][1].split(" ")[-1].strip('(').strip(')').lower()
    interval = meta[0][3]
    metadata = (symbol,indicator, interval)
    return data,metadata