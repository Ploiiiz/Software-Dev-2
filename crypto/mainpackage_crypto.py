from coinrankcandle import* 
from searchdata import *
from coinranking import *
import pandas as pd


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
    
print(load_data('BNB'))

