import av_caller as av
import credentials
import transformer as tr
import pandas as pd

api_key = credentials.av_api_key

def prettified_daily(symbol):
    '''
        Prettifies the daily data for a given symbol
        :param symbol: The symbol to get the daily data for
        :return: The daily dataframe and table name
    '''
    try:
        data, meta = av.daily(api_key, symbol)
        data = tr.rename_price_columns(data)
        data = data.apply(lambda x: round(x, 3) if x.dtype == 'float64' else x)
        table_name = symbol + '_daily_price_history'
        return data,table_name
    except Exception:
        return 'Invalid symbol'
def prettified_weekly(symbol):
    '''
        Prettifies the weekly data for a given symbol
        :param symbol: The symbol to get the weekly data for
        :return: The weekly dataframe and table name
    '''
    try:
        data, meta = av.weekly(api_key, symbol)
        data = tr.rename_price_columns(data)
        data = data.apply(lambda x: round(x, 3) if x.dtype == 'float64' else x)
        table_name = symbol + '_weekly_price_history'
        return data,table_name
    except Exception:
        return 'Invalid symbol'

def prettified_monthly(symbol):
    '''
        Prettifies the monthly data for a given symbol
        :param symbol: The symbol to get the monthly data for
        :return: The monthly dataframe and table name
    '''
    try:
        data, meta = av.monthly(api_key, symbol)
        data = tr.rename_price_columns(data)
        data = data.apply(lambda x: round(x, 3) if x.dtype == 'float64' else x)
        table_name = symbol + '_monthly_price_history'
        return data,table_name
    except Exception:
        return 'Invalid symbol'

def prettified_overview(symbol):
    '''
        Prettifies the overview data for a given symbol
        :param symbol: The symbol to get the overview data for
        :return: The overview dataframe and table name
    '''
    try:
        data, meta = av.company_overview(api_key, symbol)
        data = pd.DataFrame.from_dict(data, orient='index').T.set_index('Symbol')
        table_name = symbol + '_company_overview'
        return data,table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_quarterly_income_statement(symbol):
    '''
        Prettifies the quarterly income statement for a given symbol
        :param symbol: The symbol to get the quarterly income statement for
        :return: The quarterly income statement dataframe and table name
    '''
    try:
        data, meta = av.income_statement_quarterly(api_key, symbol)
        data = data.set_index('fiscalDateEnding')
        table_name = symbol + '_quarterly_income_statement'
        return data,table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_annual_income_statement(symbol):
    '''
        Prettifies the annual income statement for a given symbol
        :param symbol: The symbol to get the annual income statement for
        :return: The annual income statement dataframe and table name
    '''
    try:
        data, meta = av.income_statement_annual(api_key, symbol)
        data = data.set_index('fiscalDateEnding')
        table_name = symbol + '_annual_income_statement'
        return data,table_name
    except Exception:
        return 'Invalid symbol'
def prettified_quarterly_balance_sheet(symbol):
    '''
        Prettifies the quarterly income statement for a given symbol
        :param symbol: The symbol to get the quarterly income statement for
        :return: The quarterly income statement dataframe and table name
    '''
    try:
        data, meta = av.balance_sheet_quarterly(api_key, symbol)
        data = data.set_index('fiscalDateEnding')
        table_name = symbol + '_quarterly_balance_sheet'
        return data,table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_annual_balance_sheet(symbol):
    '''
        Prettifies the annual income statement for a given symbol
        :param symbol: The symbol to get the annual income statement for
        :return: The annual income statement dataframe and table name
    '''
    try:
        data, meta = av.balance_sheet_annual(api_key, symbol)
        data = data.set_index('fiscalDateEnding')
        table_name = symbol + '_annual_balance_sheet'
        return data,table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_quarterly_cash_flow(symbol):
    '''
        Prettifies the quarterly income statement for a given symbol
        :param symbol: The symbol to get the quarterly income statement for
        :return: The quarterly income statement dataframe and table name
    '''
    try:
        data, meta = av.cash_flow_quarterly(api_key, symbol)
        data = data.set_index('fiscalDateEnding')
        table_name = symbol + '_quarterly_cash_flow'
        return data,table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_annual_cash_flow(symbol):
    '''
        Prettifies the annual income statement for a given symbol
        :param symbol: The symbol to get the annual income statement for
        :return: The annual income statement dataframe and table name
    '''
    try:
        data, meta = av.cash_flow_annual(api_key, symbol)
        data = data.set_index('fiscalDateEnding')
        table_name = symbol + '_annual_cash_flow'
        return data,table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_daily_SMA(symbol):
    '''
        Prettifies the SMA for a given symbol
        :param symbol: The symbol to get the SMA for
        :return: The SMA dataframe and table name
    '''
    try:
        data, meta = av.sma_daily(api_key, symbol)
        data = tr.tech_to_dataframe(data)
        table_name = symbol + '_daily_SMA'
        return data,table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_weekly_SMA(symbol):
    '''
        Prettifies the weekly SMA for a given symbol
        :param symbol: The symbol to get the weekly SMA for
        :return: The weekly SMA dataframe and table name
    '''
    try:
        data, meta = av.sma_weekly(api_key, symbol)
        data = tr.tech_to_dataframe(data)
        table_name = symbol + '_weekly_SMA'
        return data, table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_monthly_SMA(symbol):
    '''
        Prettifies the monthly SMA for a given symbol
        :param symbol: The symbol to get the monthly SMA for
        :return: The monthly SMA dataframe and table name
    '''
    try:
        data, meta = av.sma_monthly(api_key, symbol)
        data = tr.tech_to_dataframe(data)
        table_name = symbol + '_monthly_SMA'
        return data, table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_daily_EMA(symbol):
    '''
        Prettifies the daily EMA for a given symbol
        :param symbol: The symbol to get the daily EMA for
        :return: The daily EMA dataframe and table name
    '''
    try:
        data, meta = av.ema_daily(api_key, symbol)
        data = tr.tech_to_dataframe(data)
        table_name = symbol + '_daily_EMA'
        return data, table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_weekly_EMA(symbol):
    '''
        Prettifies the weekly EMA for a given symbol
        :param symbol: The symbol to get the weekly EMA for
        :return: The weekly EMA dataframe and table name
    '''
    try:
        data, meta = av.ema_weekly(api_key, symbol)
        data = tr.tech_to_dataframe(data)
        table_name = symbol + '_weekly_EMA'
        return data, table_name
    except Exception:
        return 'Invalid symbol'

def prettified_monthly_EMA(symbol):
    '''
        Prettifies the monthly EMA for a given symbol
        :param symbol: The symbol to get the monthly EMA for
        :return: The monthly EMA dataframe and table name
    '''
    try:
        data, meta = av.ema_monthly(api_key, symbol)
        data = tr.tech_to_dataframe(data)
        table_name = symbol + '_monthly_EMA'
        return data, table_name
    except Exception:
        return 'Invalid symbol'

def prettified_daily_MACD(symbol):
    '''
        Prettifies the daily MACD for a given symbol
        :param symbol: The symbol to get the daily MACD for
        :return: The daily MACD dataframe and table name
    '''
    try:
        data, meta = av.macd_daily(api_key, symbol)
        data = tr.tech_to_dataframe(data)
        table_name = symbol + '_daily_MACD'
        return data, table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_weekly_MACD(symbol):
    '''
        Prettifies the weekly MACD for a given symbol
        :param symbol: The symbol to get the weekly MACD for
        :return: The weekly MACD dataframe and table name
    '''
    try:
        data, meta = av.macd_weekly(symbol)
        data = tr.tech_to_dataframe(data)
        table_name = symbol + '_weekly_MACD'
        return data, table_name
    except Exception:
        return 'Invalid symbol'
    
def prettified_monthly_MACD(symbol):
    '''
        Prettifies the monthly MACD for a given symbol
        :param symbol: The symbol to get the monthly MACD for
        :return: The monthly MACD dataframe and table name
    '''
    try:
        data, meta = av.macd_monthly(api_key, symbol)
        data = tr.tech_to_dataframe(data)
        table_name = symbol + '_monthly_MACD'
        return data, table_name 
    except Exception:
        return 'Invalid symbol'
    
def prettified_news(ticker):
    '''
        Prettifies the news by for a given symbol
        :param symbol: The symbol to get the news by for
        :return: The news by dataframe and table name
    '''
    data = av.news(api_key=api_key,
                         tickers=ticker)
    if data is not None:
        feed = tr.extract_news_feed(data)
        return feed
    else:
        return 'Invalid symbol'
    
