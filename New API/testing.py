import pandas
from av_getdata import *
from database import DatabaseConnection
from plotting import Plotter
from top50_us import stocks
from pprint import pprint
import sys

con = DatabaseConnection()
con.usa_stocks()

# for i in stocks:
#     con.new_entry(i)

# randomstocks = stocks[23]

# stocks_data = StocksData()
# stocks_23,metadata = stocks_data.daily_adjusted(randomstocks,'full')

# con.push_data(randomstocks,stocks_23)

# print(randomstocks)
KO_data = con.get_data('KO')
# IBM_data = con.get_data('IBM')

# pprint(KO_data)
# pprint(IBM_data)

plot = Plotter(KO_data)
plot.timeseries_fig().show()