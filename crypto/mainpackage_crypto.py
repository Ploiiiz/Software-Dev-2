import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import header
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import sqlite3
import time
import plotly.io as pio
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy.stats import linregress


class CoinRankingOHLC:

    def __init__(self, uuid, symbol, name,interval,fiatsym):
        self.uuid = uuid
        self.name = name
        self.interval = interval
        self.symbol = symbol
        self.fiat = fiatsym
        
        self.headers = header.headers
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        self.limit = None
        self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(
            self.uuid) + "/ohlc"
        self.params = {
            "referenceCurrencyUuid": searchfiat(fiatsym),
            "interval": self.interval,
            "limit": None
        }

    def get_lastest_val(self):
        self.retrieve_data()
        query = f"SELECT startingAt,open,high,low,close,price FROM ohlc{self.symbol}_{self.interval}_{self.fiat} ORDER BY startingAt DESC LIMIT 1;"
        data = pd.read_sql_query(query,self.conn) 
        data = pd.DataFrame(data.values, columns=data.columns, index=[self.symbol])
        return data
    
        
        


    def check_table(self):
        table_name = "ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat
        query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    startingAt TIMESTAMP,
                    endingAt TIMESTAMP,
                    open TEXT,
                    high TEXT,
                    low TEXT,
                    close TEXT,
                    avg TEXT,
                    price REAL,
                    SMA10 REAL,
                    SMA50 REAL,
                    EMA10 REAL,
                    EMA50 REAL,
                    WMA10 REAL,
                    WMA50 REAL
                );'''

        self.cursor.execute(query)
        self.conn.commit()

    def get_latest_timestamp(self):
        query = f"SELECT MAX(startingAt) FROM ohlc{self.symbol}_{self.interval}_{self.fiat}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        if result is not None:
            return datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
        else:

            if self.interval == 'hour':
                month = datetime.timedelta(days=180) #=6month

            elif self.interval == 'day' or 'week' or 'month':
                month = datetime.timedelta(days=730) #=2y

            
            now = datetime.datetime.now()
            target = now - month

            formatted_target = target.strftime('%Y-%m-%d %H:%M:%S')
            return datetime.datetime.strptime(formatted_target,
                                              '%Y-%m-%d %H:%M:%S')

    def set_limit(self):
        now = datetime.datetime.now()
        self.latest_timestamp = self.get_latest_timestamp()
        print(self.latest_timestamp)
        if self.latest_timestamp < now:
            #max 5000
            # limit = 5000 
            # self.limit = (now - self.latest_timestamp).total_seconds() // (3600)
            # print(self.limit)
  
            if self.interval == 'hour':
                self.limit = (now - self.latest_timestamp).total_seconds() // (3600)
                print(self.limit)

            elif self.interval == 'day':
                self.limit = (now - self.latest_timestamp).total_seconds() // (86400)
                print(self.limit)

            elif self.interval == 'week':
                self.limit = (now - self.latest_timestamp).total_seconds() // (86400*7)
                print(self.limit)
            
            elif self.interval == 'month':
                self.limit = (now - self.latest_timestamp).total_seconds() // (86400*31)
                print(self.limit)  


            if self.limit == 1:
                return None

            else:
                self.params['limit'] = int(self.limit) - 1

            print(
                self.params['limit']
            )  # set the limit based on the time difference between the latest timestamp and now

        else:
            self.params['limit'] = 1  # set limit to 1 if the latest timestamp is in the future

    def retrieve_data(self):
        self.check_table()
        self.set_limit()
        self.cursor.execute(
            f"SELECT MAX(endingAt) FROM ohlc{self.symbol}_{self.interval}_{self.fiat}")
        result = self.cursor.fetchone()
        response = requests.get(self.url,
                                params=self.params,
                                headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
        data = json.loads(response.text)
        new_data = pd.DataFrame(data["data"]["ohlc"])
        new_data["startingAt"] = new_data["startingAt"].apply(
            lambda x: datetime.datetime.fromtimestamp(x))
        new_data["endingAt"] = new_data["endingAt"].apply(
            lambda x: datetime.datetime.fromtimestamp(x))

        if self.limit == 1:
            return None

        else:
            # append the new data to the database
            new_data.to_sql(f"ohlc{self.symbol}_{self.interval}_{self.fiat}",
                            self.conn,
                            if_exists="append",
                            index=False)
            self.cursor.execute(
                f"SELECT * FROM ohlc{self.symbol}_{self.interval}_{self.fiat} ORDER BY startingAt DESC;"
            )
            self.conn.commit()

        self.cursor.execute(
            f"SELECT COUNT(*) FROM ohlc{self.symbol}_{self.interval}_{self.fiat}")
        result = self.cursor.fetchone()
        print(
            f"Added {len(new_data)} new records to ohlc{self.symbol}_{self.interval}_{self.fiat}. Total records: {result[0]}")
        self.SMA()
        self.EMA()
        self.WMA()
        cr = CoinPriceHistory(self.uuid, self.symbol,self.name,self.interval,self.fiat)
        cr.retrieve_data()


          
    def pandas_data(self):
        response = requests.get(self.url,
                                params=self.params,
                                headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
        data = json.loads(response.text)
        self.df = pd.DataFrame(data["data"]["ohlc"])

        return self.df


    
        
    def SMA(self):
        self.add_column()        
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat +  " ORDER BY startingAt ASC;"
        db = pd.read_sql_query(query, self.conn)
        sma10 = db['close'].rolling(window=240).mean() #10days = 240 datas
        sma50 = db['close'].rolling(window=1200).mean() #50days = 1200 datas
        query = "UPDATE ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat + " SET SMA10=?,SMA50=? WHERE startingAt=?"
        data = [(sma10[i],sma50[i], db['startingAt'][i]) for i in range(len(sma10))]

        self.cursor.executemany(query, data)
        self.conn.commit()

    def EMA(self):
        self.add_column()
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat +  " ORDER BY startingAt ASC;"
        db = pd.read_sql_query(query, self.conn)

        ema10 = db['close'].ewm(span=240, adjust=False).mean()
        ema50 = db['close'].ewm(span=1200, adjust=False).mean()
        query = "UPDATE ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat + " SET EMA10=?,EMA50=? WHERE startingAt=?"
        data = [(ema10[i],ema50[i], db['startingAt'][i]) for i in range(len(ema10))]

        self.cursor.executemany(query, data)
        self.conn.commit()

    def WMA(self):
        self.add_column()
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat + " ORDER BY startingAt ASC;"
        db = pd.read_sql_query(query, self.conn)

        periods_10d = 240  # Choose the number of periods to use for WMA
        weights_10d = np.arange(1, periods_10d+1)
        wma10 = db['close'].rolling(window=periods_10d, min_periods=periods_10d).apply(lambda prices: (prices * weights_10d).sum() / weights_10d.sum(), raw=True)

        periods_50d = 1200  # Choose the number of periods to use for WMA
        weights_50d = np.arange(1, periods_50d+1)
        wma50 = db['close'].rolling(window=periods_50d, min_periods=periods_50d).apply(lambda prices: (prices * weights_50d).sum() / weights_50d.sum(), raw=True)

        query = "UPDATE ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat + " SET WMA10=?,WMA50=? WHERE startingAt=?"
        data = [(wma10[i],wma50[i], db['startingAt'][i]) for i in range(len(wma10))]

        self.cursor.executemany(query, data)
        self.conn.commit()

       


    def show_candlestick(self):
        self.retrieve_data()
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat + " ORDER BY startingAt ASC;"
        db = pd.read_sql_query(query, self.conn)
        candlestick = go.Candlestick(
            x=db["startingAt"],
            open=db["open"],
            high=db["high"],
            low=db["low"],
            close=db["close"],
        )

        can = go.Figure(candlestick)

        can.update_layout(
            title=self.name + " " + "(" + self.symbol + ")",
            # paper_bgcolor="#001f2e",
            # plot_bgcolor='#003951',
            title_font_color='white',
            xaxis=dict(rangeselector=dict(buttons=list([
                dict(count=1, label='1D', step='day', stepmode='backward'),
                dict(count=7, label='7D', step='day', stepmode='backward'),
                dict(count=1, label='1M', step='month', stepmode='backward'),
                dict(count=6, label='6M', step='month', stepmode='backward'),
                dict(count=1, label='1Y', step='year', stepmode='backward'),
                dict(step='all')
            ], ), ),
                       rangeslider=dict(visible=True),
                       type='date'),
        )

        js = '''document.body.style.backgroundColor = "#001f2e"; '''

        can.update_yaxes(
            showgrid=False,
            # color='white',
            fixedrange=False,
        )
        can.update_xaxes(showgrid=False, color='white')        
        # can.show(renderer="browser",post_script=[js])
        # can_html = pio.to_html(can, include_plotlyjs='cdn', post_script=[js])
        # can.show()

        return can
    

    def show_candlestick_with_SMA(self):
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat + " ORDER BY startingAt ASC;"
        db = pd.read_sql_query(query, self.conn)
        candlestick = go.Candlestick(
            x=db["startingAt"],
            open=db["open"],
            high=db["high"],
            low=db["low"],
            close=db["close"],
        )

        can = go.Figure(candlestick)

        can.update_layout(
            title=self.name + " " + "(" + self.symbol + ")",
            # paper_bgcolor="#001f2e",
            # plot_bgcolor='#003951',
            title_font_color='white',
            xaxis=dict(rangeselector=dict(buttons=list([
                dict(count=1, label='1D', step='day', stepmode='backward'),
                dict(count=7, label='7D', step='day', stepmode='backward'),
                dict(count=1, label='1M', step='month', stepmode='backward'),
                dict(count=6, label='6M', step='month', stepmode='backward'),
                dict(count=1, label='1Y', step='year', stepmode='backward'),
                dict(step='all')
            ], ), ),
                       rangeslider=dict(visible=True),
                       type='date'),
        )

        js = '''document.body.style.backgroundColor = "#001f2e"; '''

        can.update_yaxes(
            showgrid=False,
            # color='white',
            fixedrange=False,
        )
        can.update_xaxes(showgrid=False, color='white')
        can.add_trace(go.Scatter(x=db["startingAt"],
                         y=db['SMA10'],
                         opacity=0.7,
                         line=dict(color='blue', width=2),
                         name='SMA10'))
        can.add_trace(go.Scatter(x=db["startingAt"],
                                y=db['SMA50'],
                                opacity=0.7,
                                line=dict(color='orange', width=2),
                                name='SMA50'))

        # can.show(renderer="browser",post_script=[js])
        # can_html = pio.to_html(can, include_plotlyjs='cdn', post_script=[js])
        # can.show()

        return can
    

    def show_candlestick_with_EMA(self):
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat +  " ORDER BY startingAt ASC;"
        db = pd.read_sql_query(query, self.conn)
        candlestick = go.Candlestick(
            x=db["startingAt"],
            open=db["open"],
            high=db["high"],
            low=db["low"],
            close=db["close"],
        )

        can = go.Figure(candlestick)

        can.update_layout(
            title=self.name + " " + "(" + self.symbol + ")",
            # paper_bgcolor="#001f2e",
            # plot_bgcolor='#003951',
            title_font_color='white',
            xaxis=dict(rangeselector=dict(buttons=list([
                dict(count=1, label='1D', step='day', stepmode='backward'),
                dict(count=7, label='7D', step='day', stepmode='backward'),
                dict(count=1, label='1M', step='month', stepmode='backward'),
                dict(count=6, label='6M', step='month', stepmode='backward'),
                dict(count=1, label='1Y', step='year', stepmode='backward'),
                dict(step='all')
            ], ), ),
                       rangeslider=dict(visible=True),
                       type='date'),
        )

        js = '''document.body.style.backgroundColor = "#001f2e"; '''

        can.update_yaxes(
            showgrid=False,
            # color='white',
            fixedrange=False,
        )
        can.update_xaxes(showgrid=False, color='white')
        can.add_trace(go.Scatter(x=db["startingAt"],
                         y=db['EMA10'],
                         opacity=0.7,
                         line=dict(color='blue', width=2),
                         name='EMA10'))
        can.add_trace(go.Scatter(x=db["startingAt"],
                                y=db['EMA50'],
                                opacity=0.7,
                                line=dict(color='orange', width=2),
                                name='EMA50'))

        # can.show(renderer="browser",post_script=[js])
        # can_html = pio.to_html(can, include_plotlyjs='cdn', post_script=[js])
        # can.show()

        return can
    

    def show_candlestick_with_WMA(self):
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat + " ORDER BY startingAt ASC;"
        db = pd.read_sql_query(query, self.conn)
        candlestick = go.Candlestick(
            x=db["startingAt"],
            open=db["open"],
            high=db["high"],
            low=db["low"],
            close=db["close"],
        )

        can = go.Figure(candlestick)

        can.update_layout(
            title=self.name + " " + "(" + self.symbol + ")",
            # paper_bgcolor="#001f2e",
            # plot_bgcolor='#003951',
            title_font_color='white',
            xaxis=dict(rangeselector=dict(buttons=list([
                dict(count=1, label='1D', step='day', stepmode='backward'),
                dict(count=7, label='7D', step='day', stepmode='backward'),
                dict(count=1, label='1M', step='month', stepmode='backward'),
                dict(count=6, label='6M', step='month', stepmode='backward'),
                dict(count=1, label='1Y', step='year', stepmode='backward'),
                dict(step='all')
            ], ), ),
                       rangeslider=dict(visible=True),
                       type='date'),
        )

        js = '''document.body.style.backgroundColor = "#001f2e"; '''

        can.update_yaxes(
            showgrid=False,
            # color='white',
            fixedrange=False,
        )
        can.update_xaxes(showgrid=False, color='white')
        can.add_trace(go.Scatter(x=db["startingAt"],
                         y=db['WMA10'],
                         opacity=0.7,
                         line=dict(color='blue', width=2),
                         name='WMA10'))
        can.add_trace(go.Scatter(x=db["startingAt"],
                                y=db['WMA50'],
                                opacity=0.7,
                                line=dict(color='orange', width=2),
                                name='WMA50'))

        # can.show(renderer="browser",post_script=[js])
        # can_html = pio.to_html(can, include_plotlyjs='cdn', post_script=[js])
        # can.show()

        return can
    
    def add_column(self):
        table_name = "ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat

        # Check if 'SMA10' column exists in the table
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()
        SMA10_exists = False
        for column in columns:
            if column[1] == 'SMA10':
                SMA10_exists = True
                break

        # If 'SMA10' column does not exist, add it
        if not SMA10_exists:
            query = f'''ALTER TABLE {table_name} ADD COLUMN SMA10 REAL;'''
            self.cursor.execute(query)


        # Check if 'SMA50' column exists in the table
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()
        SMA50_exists = False
        for column in columns:
            if column[1] == 'SMA50':
                SMA50_exists = True
                break

        # If 'SMA50' column does not exist, add it
        if not SMA50_exists:
            query = f'''ALTER TABLE {table_name} ADD COLUMN SMA50 REAL;'''
            self.cursor.execute(query)     


        # Check if 'EMA10' column exists in the table
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()
        EMA10_exists = False
        for column in columns:
            if column[1] == 'EMA10':
                EMA10_exists = True
                break

        # If 'EMA10' column does not exist, add it
        if not EMA10_exists:
            query = f'''ALTER TABLE {table_name} ADD COLUMN EMA10 REAL;'''
            self.cursor.execute(query)


        # Check if 'EMA50' column exists in the table
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()
        EMA50_exists = False
        for column in columns:
            if column[1] == 'EMA50':
                EMA50_exists = True
                break

        # If 'EMA50' column does not exist, add it
        if not EMA50_exists:
            query = f'''ALTER TABLE {table_name} ADD COLUMN EMA50 REAL;'''
            self.cursor.execute(query)    


        # Check if 'WMA10' column exists in the table
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()
        WMA10_exists = False
        for column in columns:
            if column[1] == 'WMA10':
                WMA10_exists = True
                break

        # If 'WMA10' column does not exist, add it
        if not WMA10_exists:
            query = f'''ALTER TABLE {table_name} ADD COLUMN WMA10 REAL;'''
            self.cursor.execute(query)   


        # Check if 'WMA50' column exists in the table
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()
        WMA50_exists = False
        for column in columns:
            if column[1] == 'WMA50':
                WMA50_exists = True
                break

        # If 'WMA50' column does not exist, add it
        if not WMA50_exists:
            query = f'''ALTER TABLE {table_name} ADD COLUMN WMA50 REAL;'''
            self.cursor.execute(query)         


          
        

        self.conn.commit()

    


    def show_candlestick_and_linechart(self):
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat + " ORDER BY startingAt ASC;"
        db = pd.read_sql_query(query, self.conn)
        
        # Create the candlestick chart
        candlestick = go.Candlestick(
            x=db["startingAt"],
            open=db["open"],
            high=db["high"],
            low=db["low"],
            close=db["close"],
        )
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
        fig.add_trace(candlestick, row=1, col=1)

        # Create the line chart
        line_chart = go.Scatter(
            x=db['startingAt'],
            y=db['price'],
            mode='lines',
            name='Price',
            line=dict(color='green')
        )
        fig.add_trace(line_chart, row=2, col=1)
        
        
        js = '''document.body.style.backgroundColor = "#001f2e"; '''
        fig.update_layout(  title=self.name + " " + "(" + self.symbol + ")",paper_bgcolor="#001f2e",
            plot_bgcolor='#003951',
            title_font_color='white',)

        fig.update_yaxes(
            showgrid=False,
            color='white',
            fixedrange=False,
            row=1, col=1
        )
        fig.update_yaxes(
            showgrid=False,
            color='white',
            fixedrange=False,
            row=2, col=1
        )
        fig.update_xaxes(showgrid=False, color='white', row=2, col=1)
        fig.update_xaxes(showgrid=False, color='white', row=1, col=1)
        # Update the layout of the figure
        fig.update_layout(            
            
            xaxis=dict(rangeselector=dict(buttons=list([
                dict(count=1, label='1D', step='day', stepmode='backward'),
                dict(count=7, label='7D', step='day', stepmode='backward'),
                dict(count=1, label='1M', step='month', stepmode='backward'),
                dict(count=6, label='6M', step='month', stepmode='backward'),
                dict(count=1, label='1Y', step='year', stepmode='backward'),
                dict(step='all')
            ], ), ),
                    rangeslider=dict(visible=False),
                    type='date'),
                   
        )
        
        # fig.show()
        fig_html = pio.to_html(fig, include_plotlyjs='cdn', post_script=[js])
        return fig_html

     

    def close_connection(self):
        self.conn.close()

class Data:
    def __init__(self):
        self.conn = sqlite3.connect("coinranking.db")
        self.df = None
        self.headers = header.headers
        self.url = "https://api.coinranking.com/v2/coins"
        self.params = {"limit": 100,"timePeriod":"1h"}

    def retrieve_data(self):
        
        response = requests.get(self.url, params=self.params, headers=self.headers)

        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()

        data = json.loads(response.text)

        self.df = pd.DataFrame(data['data']['coins'])
        # print(self.df)

        self.df.to_excel('coinranking.xlsx', sheet_name='dataCoin', index=True)

        cryt = pd.read_excel('coinranking.xlsx')


        cryt.to_sql("coinrankingdata", self.conn, if_exists="replace")

        # self.conn.commit()
        # self.conn.close()

    def pandas_data(self):
        response = requests.get(self.url, params=self.params, headers=self.headers)

        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()

        data = json.loads(response.text)

        self.df = pd.DataFrame(data['data']['coins'])
        return self.df

    def get_list_symbol(self):
        list_symbol = list(self.df['symbol'])
        return list_symbol
    
    def get_list_uuid(self):
        list_uuid = list(self.df['uuid'])
        return list_uuid
    
    def get_list_name(self):
        list_name = list(self.df['name'])
        return list_name

    def get_list_price(self):
        price = list(self.df['price'])
        list_price = [float(number) for number in price]
        list_price = [format(number, ",.5g") for number in list_price]

        return list_price

    def get_list_change(self):
        self.df['change'] = pd.to_numeric(self.df['change'], errors='coerce')
        list_change = []
        change = list(self.df['change'])
        for c in change:
            if c >= 0:
                ch = '+' + '{:.2f}'.format(c) + '%'
            else:
                ch = '{:.2f}'.format(c) + '%'
            
            list_change.append(ch)

        # print(list_change)
        return list_change
    
    def get_list_change_color(self):
        self.df['change'] = pd.to_numeric(self.df['change'], errors='coerce')
        list_change_color = []
        change_color = list(self.df['change'])
        for c in change_color:
            if c >= 0:
                color = "#19fd53"
            else:
                color = "#fa0104"
            
            list_change_color.append(color)

        # print(list_change)
        return  list_change_color

    def get_list_marketcap(self):
        marketcap = list(self.df['marketCap'])
        list_marketcap = [float(number) for number in marketcap]
        list_marketcap = [format(num / 1000000, ',.0f') + ' M' for num in list_marketcap]
        return list_marketcap



    def close_connection(self):
        self.conn.close()


class CoinPriceHistory:
    def __init__(self, uuid, symbol,name,interval,fiat):
        self.uuid = uuid
        self.name = name
        self.interval = interval
        if self.interval == 'hour':
            self.timePeriod = "30d"   
        elif self.interval == 'day' or "week" or "month":
            self.timePeriod = "3y"         
        self.symbol = symbol
        self.headers = header.headers        
        self.fiat = fiat
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(self.uuid) + "/history"
        self.params = {"referenceCurrencyUuid":searchfiat(fiat),"timePeriod":self.timePeriod}

    
    def retrieve_data(self):
        self.add_column()
        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
        data = json.loads(response.text)
        # print(data["data"]["history"])
        self.df = pd.DataFrame(data["data"]["history"])        
        # self.df["price"] = pd.to_numeric(self.df["price"])
        # self.df['timestamp']= self.df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x)) 
        # print(self.df)

        
         # Insert the data into the 'ohlc' table
        for i in range(len(self.df)):
            timestamp = int(self.df['timestamp'][i])
            timestamp = datetime.datetime.fromtimestamp(timestamp)
            price = self.df['price'][i]
                
            query = f"UPDATE ohlc{self.symbol}_{self.interval}_{self.fiat} SET price = ? WHERE endingAt = ?"
            self.cursor.execute(query, (price,timestamp))
            self.cursor.execute(
                f"SELECT * FROM ohlc{self.symbol}_{self.interval}_{self.fiat} ORDER BY endingAt DESC;"
            )
            
            self.conn.commit()
        self.conn.close()

    def pandas_data(self):
        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
        data = json.loads(response.text)
        # print(data["data"]["history"])
        self.df = pd.DataFrame(data["data"]["history"]) 
        self.df["price"] = pd.to_numeric(self.df["price"])
        self.df['timestamp']= self.df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x)) 
        return self.df
     
    def add_column(self):
        table_name = "ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat 

        # Check if 'price' column exists in the table
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()
        price_exists = False
        for column in columns:
            if column[1] == 'price':
                price_exists = True
                break

        # If 'price' column does not exist, add it
        if not price_exists:
            query = f'''ALTER TABLE {table_name} ADD COLUMN price REAL;'''
            self.cursor.execute(query)

        self.conn.commit()



    def save_to_database(self):        
        self.df.to_sql("price" + self.symbol + "_" + self.timePeriod, self.conn, if_exists="replace")   
 
        
            
    def save_to_excel(self):
        self.df.to_excel('coinrankingline.xlsx', sheet_name= self.symbol + "_" + self.timePeriod , index=True)
        
    def show_linechart(self,):        
        # df = pd.read_sql_query("SELECT * from price" + self.symbol + "_" + self.timePeriod, self.conn)

        # line_chart = px.line(data_frame=df, x="timestamp", y="price")
        # line_chart.show()
        query = "SELECT price,startingAt FROM ohlc" + self.symbol + "_" + self.interval + "_" + self.fiat + " ORDER BY startingAt DESC;"
        
        db = pd.read_sql_query(query, self.conn)
        
    
        fig = px.line(db, x='startingAt', y="price",title=self.name + " " + "(" + self.symbol + ")")
        
        fig.show()
        
        
    def close_connection(self):
        self.conn.close()

class CoinRankingSearch:
    def __init__(self, find):
        self.find = find
        self.uuid = None
        self.name = None
        self.price = None
        self.change = None
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        
    def data(self):
        Data().retrieve_data()
        query = f'''
        SELECT symbol,name,uuid,change,[24hVolume] FROM coinrankingdata WHERE symbol = '{self.find}'
        '''
        data = pd.read_sql_query(query,self.conn)
        data = data.set_index('symbol')       

        return data
    
    def get_uuid(self):

        query = '''
        SELECT uuid FROM coinrankingdata WHERE symbol = ?
        '''
        # Execute the SELECT statement
        self.cursor.execute(query, (self.find,))
        row = self.cursor.fetchone()
        if row:
            self.uuid = row[0]
            # self.conn.commit()
            # self.cursor.close()
            return self.uuid
        else:
            return None
        
        
        

    def get_name(self):
        query = '''
        SELECT name FROM coinrankingdata WHERE symbol = ?
        '''
        # Execute the SELECT statement
        self.cursor.execute(query, (self.find,))
        row = self.cursor.fetchone()
        if row:
            self.name = row[0]
            # self.conn.commit()
            # self.cursor.close()
            return self.name
        else:
            return None

    def get_price(self):
        return self.price
    
    def get_change(self):
        return self.change
    
    def get_24Vol(self):
        query = '''
        SELECT [24hVolume] FROM coinrankingdata WHERE symbol = ?
        '''
        # Execute the SELECT statement
        self.cursor.execute(query, (self.find,))
        row = self.cursor.fetchone()
        if row:
            self.vol = row[0]
            # self.conn.commit()
            # self.cursor.close()
            return self.vol
        else:
            return None
        

    def insert_data(self):
        
        self.cursor.execute("""
            INSERT INTO coinrankingdata (name, symbol, price, uuid, change)
            VALUES (?, ?, ?, ?, ?)
        """, (self.name, self.find, self.price, self.uuid, self.change))
        self.conn.commit()
        self.cursor.close()


    def delete_data(self):

        self.cursor.execute("""
            DELETE FROM coinrankingdata WHERE symbol = ?
        """, (self.find,))
        self.conn.commit()
        


    def update_data(self):
        set_clause = ''
        if self.name:
            set_clause += 'name = "{}",'.format(self.name)
        if self.price:
            set_clause += 'price = {},'.format(self.price)
        if self.uuid:
            set_clause += 'uuid = "{}",'.format(self.uuid)
        if self.change:
            set_clause += 'change = {},'.format(self.change)

        set_clause = set_clause[:-1]  # remove the last comma

        query = '''
            UPDATE coinrankingdata SET {}
            WHERE symbol = ?
        '''.format(set_clause)

        self.cursor.execute(query, (self.find,))
        self.conn.commit()
        self.cursor.close()
        
def fiat():
    conn = sqlite3.connect("coinranking.db")
    headers = header.headers        
    url = "https://coinranking1.p.rapidapi.com/reference-currencies"
    querystring = {"limit":"50","offset":"0"}

    

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != 200:
                print("Error: Could not retrieve data from Coinranking API")
                exit()
    data = json.loads(response.text)
    new_data = pd.DataFrame(data['data']["currencies"])
    new_data.to_sql('fiat',conn, if_exists="replace")
    conn.commit()
    conn.close()


def searchfiat(symbol):
    fiat()
    conn = sqlite3.connect("coinranking.db")
    query = f'''
    SELECT uuid FROM fiat WHERE symbol = '{symbol}'
    '''
    data = pd.read_sql_query(query,conn)     
    data = data.loc[0, 'uuid']

    return data

def sentiment_news(symbol):
    search = CoinRankingSearch(symbol)
    data = search.data()
    uuid = data.loc[symbol, 'uuid']
    name = data.loc[symbol, 'name']
    headers = header.headers
    url = "https://coinranking1.p.rapidapi.com/coin/" + uuid + "/history"
    params = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":'24h'}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print("Error: Could not retrieve data from Alpha Vantage API")
        exit()
    data = json.loads(response.text)
    # print(data["data"]["history"])
    df = pd.DataFrame(data["data"]["history"]) 
    df["price"] = pd.to_numeric(df["price"])
    df['timestamp']= df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x)) 
    df_price = df
    # print(df_price)


    url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol=" + symbol + "&apikey=" + header.api_AV
    response = requests.get(url)
    data = json.loads(response.text)
    new_data = pd.DataFrame(data)

    feed_data = pd.DataFrame(data['feed'])
    for i in range (len(feed_data['time_published'])):
        dt_obj = datetime.datetime.strptime(feed_data['time_published'][i], '%Y%m%dT%H%M%S')
        feed_data['time_published'][i] = dt_obj.strftime( '%Y-%m-%d %H:%M:%S')

    # Create the figure
    fig = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.02)

    # Add the price data as a trace and set title for price graph
    fig.add_trace(
        go.Scatter(x=df_price['timestamp'], y=df_price['price'], name="Price"),
        row=1, col=1
    )

    # Convert Timestamp object to integer
    x = df_price['timestamp'].astype(np.int64) // 10**9

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(x, df_price['price'])

    # Calculate regression line
    regression_line = slope * x + intercept

    # Plot regression line
    fig.add_trace(
        go.Scatter(x=df_price['timestamp'], y=regression_line, name="Regression Line"),
        row=1, col=1
    )

    
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_layout(title_text="Price and Sentiment Analysis for "+ name + "(" + symbol + ")")
    fig.update_xaxes(range=[feed_data['time_published'].iloc[-1], feed_data['time_published'].iloc[0]], row=1, col=1)

  



    # Add the sentiment scores as a trace and set title for sentiment score graph
    fig.add_trace(
        go.Scatter(x=feed_data['time_published'], y=feed_data['overall_sentiment_score'], name="Sentiment Score"),
        row=2, col=1
    )
    # Convert Timestamp object to integer
    x = pd.to_datetime(feed_data['time_published']).astype(np.int64) // 10**9


    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(x, feed_data['overall_sentiment_score'])

    # Calculate regression line
    regression_line = slope * x + intercept

    # Plot regression line
    fig.add_trace(
        go.Scatter(x=feed_data['time_published'], y=regression_line, name="Regression Line"),
        row=2, col=1
    )

    fig.update_yaxes(title_text="Sentiment Score", row=2, col=1)
    

    # Update the layout of the figure
    fig.update_layout(
        xaxis_title="Date",
        legend=dict(
            x=0,
            y=1,
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0)'
        ),
        plot_bgcolor='rgb(230, 230, 230)',
        height=800
    )
    return fig






def load_data(symbol,sym_fiat,interval):
    search = CoinRankingSearch(symbol)
    coin_data = search.data()
    uuid = coin_data.loc[symbol, 'uuid']
    name = coin_data.loc[symbol, 'name']
    can = CoinRankingOHLC(uuid,symbol,name,interval,sym_fiat)    
    lastest_val_data = can.get_lastest_val()    
    combined_data = pd.concat([coin_data,lastest_val_data], axis=1)
    return combined_data


def load_all_prices(symbol,sym_fiat):   
    hourly = load_data(symbol,sym_fiat,'hour')
    daily = load_data(symbol,sym_fiat,'day')
    weekly = load_data(symbol,sym_fiat,'week')
    monthly = load_data(symbol,sym_fiat,'month')

    return hourly,daily,weekly,monthly



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









    
print(load_all_prices('BTC','EUR'))

