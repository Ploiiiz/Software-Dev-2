from coinrankcandle import* 
from searchdata import *
from coinranking import *
import pandas as pd
from sentiment_news import *


def load_data(symbol):
    search = CoinRankingSearch(symbol)
    data = search.data()
    uuid = data.loc[symbol, 'uuid']
    name = data.loc[symbol, 'name']
    can = CoinRankingOHLC(uuid,symbol,name)
    lastest_val_data = can.get_lastest_val()
    coin_data = search.data()
    combined_data = pd.concat([coin_data,lastest_val_data], axis=1)
    return combined_data


def plot_candle(symbol):
    search = CoinRankingSearch(symbol)
    data = search.data()
    uuid = data.loc[symbol, 'uuid']
    name = data.loc[symbol, 'name']
    can = CoinRankingOHLC(uuid,symbol,name)
    can = can.show_candlestick()
    return can


def plot_candle_html(symbol):
    js = '''document.body.style.backgroundColor = "#001f2e"; '''   
    can_html = pio.to_html(plot_candle(symbol), include_plotlyjs='cdn', post_script=[js])
    return can_html


def plot_SMA(symbol):
    search = CoinRankingSearch(symbol)
    data = search.data()
    uuid = data.loc[symbol, 'uuid']
    name = data.loc[symbol, 'name']
    can = CoinRankingOHLC(uuid,symbol,name)
    can = can.show_candlestick_with_SMA()
    return can

def plot_SMA_html(symbol):
    js = '''document.body.style.backgroundColor = "#001f2e"; '''   
    can_html = pio.to_html(plot_SMA(symbol), include_plotlyjs='cdn', post_script=[js])
    return can_html

def plot_EMA(symbol):
    search = CoinRankingSearch(symbol)
    data = search.data()
    uuid = data.loc[symbol, 'uuid']
    name = data.loc[symbol, 'name']
    can = CoinRankingOHLC(uuid,symbol,name)
    can = can.show_candlestick_with_EMA()
    return can

def plot_EMA_html(symbol):
    js = '''document.body.style.backgroundColor = "#001f2e"; '''   
    can_html = pio.to_html(plot_EMA(symbol), include_plotlyjs='cdn', post_script=[js])
    return can_html

def plot_WMA(symbol):
    search = CoinRankingSearch(symbol)
    data = search.data()
    uuid = data.loc[symbol, 'uuid']
    name = data.loc[symbol, 'name']
    can = CoinRankingOHLC(uuid,symbol,name)
    can = can.show_candlestick_with_WMA()
    return can

def plot_WMA_html(symbol):
    js = '''document.body.style.backgroundColor = "#001f2e"; '''   
    can_html = pio.to_html(plot_WMA(symbol), include_plotlyjs='cdn', post_script=[js])
    return can_html


def plot_sentiment_news(symbol):
    search = CoinRankingSearch(symbol)
    data = search.data()
    uuid = data.loc[symbol, 'uuid']
    name = data.loc[symbol, 'name']
    fig = sentiment_news(symbol)
    return fig

def plot_sentiment_news_html(symbol):
    js = '''document.body.style.backgroundColor = "#001f2e"; '''   
    fig_html = pio.to_html(plot_sentiment_news(symbol), include_plotlyjs='cdn', post_script=[js])
    return fig_html







    
print(plot_sentiment_news_html('BNB'))

