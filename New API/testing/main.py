import credentials
import av_caller
import transformer
import db
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pl
from datetime import datetime
from sqlite3 import IntegrityError
import time

key = credentials.av_api_key

TEST_SYMBOL = 'IBM'

def load_data(symbol,type='price',interval='daily',tech='ema'):
    if type == 'price':
        table_name = symbol+'_'+interval+'_price_history'
        if db.table_exists(table_name):# and not db.hastofetch(table_name):
            df = db.load_table(table_name)
            return df
        else:
            fetch_and_store_prices(symbol, interval)
            return load_data(symbol, type, interval)
    elif type == 'news':
        pass
    elif type == 'ti':
        table_name = symbol+'_'+tech.upper()+'_'+interval
        if db.table_exists(table_name):# and not db.hastofetch
            df = db.load_table(table_name)
            return df
        else:
            fetch_and_store_tech(symbol, tech, interval)
            return load_data(symbol, type, interval)
    elif type == 'fd':
        pass

def fetch_and_store_prices(symbol, interval):
    if interval == 'daily':
        data, meta = av_caller.daily(key, symbol)
    elif interval == 'weekly':   
        data, meta = av_caller.weekly(key, symbol) 
    elif interval == 'monthly':  
        data, meta = av_caller.monthly(key, symbol)
    
    data, meta = transformer.prettify_price(data, meta)
    try:
        db.store_data(data, meta)
    except IntegrityError:
        pass   
        # print('stored data')

def fetch_and_store_tech(symbol, type, interval):

    if type.lower() == 'sma':
        if interval == 'daily':
            data, meta = av_caller.sma_daily(key, symbol)
        elif interval == 'weekly':   
            data, meta = av_caller.sma_weekly(key, symbol) 
        elif interval == 'monthly':  
            data, meta = av_caller.sma_monthly(key, symbol)
    elif type.lower() == 'ema':
        if interval == 'daily':
            data, meta = av_caller.ema_daily(key, symbol)
        elif interval == 'weekly':
            data, meta = av_caller.ema_weekly(key, symbol)
        elif interval =='monthly':
            data, meta = av_caller.ema_monthly(key, symbol)
    elif type.lower() == 'bbands':
        if interval == 'daily':
            data, meta = av_caller.bbands_daily(key, symbol)
        elif interval == 'weekly':
            data, meta = av_caller.bbands_weekly(key, symbol)
        elif interval =='monthly':
            data, meta = av_caller.bbands_monthly(key, symbol)
    
    data, meta = transformer.prettify_tech(data, meta)
    try:
        db.store_tech_table(data,meta)
    except IntegrityError:
        pass
        # print('stored data')
    
def plotting(symbol,full=False):

    daily = load_data(symbol,interval='daily')
    weekly = load_data(symbol,interval='weekly')
    monthly = load_data(symbol,interval='monthly')
    if not full:
        daily = load_data(symbol,interval='daily').iloc[:(len(daily))//2]
        weekly = load_data(symbol,interval='weekly').iloc[:(len(weekly))//2]
        monthly = load_data(symbol,interval='monthly').iloc[:(len(monthly))//2]


    layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,42,61,1)',
    )
    fig = go.Figure(data=[go.Candlestick(x=daily['timestamp'],
                    open=daily['open'],
                    high=daily['high'],
                    low=daily['low'],
                    close=daily['close'])],
                    layout=layout)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(
    font=dict(color='white'),
    updatemenus=[
        dict(
            type = "buttons",
            direction = "left",
            buttons=[
            {'label': '1D',
             'method': 'update',
             'args': [{'x': [daily['timestamp']],
                       'open': [daily['open']],
                       'high': [daily['high']],
                       'low': [daily['low']],
                       'close': [daily['close']]}]},
            {'label': '1W',
             'method': 'update',
             'args': [{'x': [weekly['timestamp']],
                       'open': [weekly['open']],
                       'high': [weekly['high']],
                       'low': [weekly['low']],
                       'close': [weekly['close']]}]},
            {'label': '1M',
             'method': 'update',
             'args': [{'x': [monthly['timestamp']],
                       'open': [monthly['open']],
                       'high': [monthly['high']],
                       'low': [monthly['low']],
                       'close': [monthly['close']]}]},           
        ],
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.04,
            xanchor="left",
            y=1.3,
            yanchor="top"
        ),
    ]
)
    # fig.show()
    return fig

def stock_list():
    selected = credentials.selected_top50[:10]
    stocks = []
    for i in selected:
        data = av_caller.quote_endpoint(key,i)
        time.sleep(3)
        data = transformer.minimal_parse(data)
        stocks.append(data)
    return stocks

def html_plot(symbol):
    html = pl.to_html(plotting(symbol), include_plotlyjs='cdn')
    return html