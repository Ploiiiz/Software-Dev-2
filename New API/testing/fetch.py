import credentials
import requests
import pandas
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances

class NewsSentiment:
    def __init__(self,api_key) -> None:
        self.api_key = credentials.av_api_key
        self.url = credentials.av_url

    def news(self,tickers=None,topics=None,time_from=None,time_to=None,sort=None,limit=None):
        params = {
        "function"  :   "NEWS_SENTIMENT",
        "apikey"    :   self.api_key,
        "tickers"   :   tickers,
        "topics"    :   topics,
        "time_from" :   time_from,
        "time_to"   :   time_to,
        "sort"      :   sort,
        "limit"     :   limit
        }
        response = requests.request("GET",self.url,params=params)
        json = response.json()

        items = json['items']
        feed = json['feed']
        newsfeed = self._format(feed)
        return (newsfeed,items)

    def _format(self,content):
        return pandas.DataFrame.from_dict(content)



api_key = credentials.av_api_key
timeseries = TimeSeries(api_key,output_format='pandas')
news = NewsSentiment(api_key)
fundamentals = FundamentalData(api_key)
indicators = TechIndicators(api_key,output_format='pandas')
sector_performances = SectorPerformances(api_key)

def cut_and_rename_col(df):
    df = df.drop(["7. dividend amount", "8. split coefficient"],axis=1)
    df = df.rename(columns={"1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. adjusted close": "adjusted close",
            "6. volume": "volume",})
    return df

def sort_date_asc(df):
    df = df.sort_index()
    return df

def to_dataframe(data):
    if type(data) != pandas.DataFrame:
        df = pandas.DataFrame.from_dict(data, orient='index')
        return df
    return data
