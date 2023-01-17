import pandas
from av_getdata import *
from pprint import pprint
import sys

news = NewsSentiment()
items,info = news.news('AAPL','Technology')



pprint(info)