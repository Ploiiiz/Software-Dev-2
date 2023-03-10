import requests
import header
import pandas as pd
import sqlite3
import json

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=COIN&apikey=' + header.api_AV

# response = requests.get(url)
# if response.status_code != 200:
#     print("Error: Could not retrieve data from Coinranking API")
#     exit()
# conn = sqlite3.connect("coinranking.db")
# cursor = conn.cursor()
# json = response.json()
# items = json['items']

# rows = []
# for item in items:
#     row = {
#         'date': item['date'],
#         'source': item['source'],
#         'title': item['title'],
#         'url': item['url'],
#         'summary': item['summary'],
#         'sentiment': item['sentiment'],
#     }
#     rows.append(row)

# df = pd.DataFrame(rows)
# df.to_sql("News", conn, if_exists="replace")
# conn.close()
# print(df)


# class NewsSentiment:
#     def __init__(self) -> None:
#         self.api_key = header.api_AV
#         self.url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&CRYPTO:BTC&apikey=' + header.api_AV
#         self.conn = sqlite3.connect("coinranking.db")
#         self.cursor = self.conn.cursor()

#     def news(self,tickers=None,topics=None,time_from=None,time_to=None,sort=None,limit=None):
#         params = {
#         "function"  :   "NEWS_SENTIMENT",
#         "apikey"    :   self.api_key,
#         "tickers"   :   tickers,
#         "topics"    :   topics,
#         "time_from" :   time_from,
#         "time_to"   :   time_to,
#         "sort"      :   sort,
#         "limit"     :   limit
#         }
#         response = requests.request("GET",self.url,params=params)
#         json = response.json()

#         items = json['items']
#         feed = json['feed']
#         newsfeed = self._format(feed)
#         self.feed = feed
#         return (items,newsfeed)

#     def _format(self,content):
#         data = pd.DataFrame.from_dict(content)
#         return data

#     def filter_sentiments(self,feed,sentiment_label):
#         return feed[feed['overall_sentiment_label']==sentiment_label]

#     def save_to_database(self,content): 
#         # df = self.news()
#         # data = self._format(df)
#         content.to_sql("News" , self.conn, if_exists="replace")  
#         self.conn.close() 

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
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

# news = NewsSentiment()
# items,info = news.news()
# news.filter_sentiments(info,'Somewhat-Bullish')
# news.save_to_database()