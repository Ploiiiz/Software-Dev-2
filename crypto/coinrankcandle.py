import requests
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
import datetime
import header
import sqlite3
import time
import plotly.io as pio
import coinrankingLine as cl
import pandas as pd
import numpy as np




# from searchdata import CoinRankingSearch


class CoinRankingOHLC:

    def __init__(self, uuid, symbol, name):
        self.uuid = uuid
        self.name = name
        self.interval = "hour"
        self.symbol = symbol
        self.headers = header.headers
        self.conn = sqlite3.connect("coinranking.db")
        self.cursor = self.conn.cursor()
        self.limit = None
        self.url = "https://coinranking1.p.rapidapi.com/coin/" + str(
            self.uuid) + "/ohlc"
        self.params = {
            "referenceCurrencyUuid": "yhjMzLPhuIDl",
            "interval": self.interval,
            "limit": None
        }

    def get_lastest_val(self):
        self.retrieve_data2()
        query = f"SELECT startingAt,open,high,low,close,price FROM ohlc{self.symbol}_{self.interval} ORDER BY startingAt DESC LIMIT 1;"
        data = pd.read_sql_query(query,self.conn) 
        data = pd.DataFrame(data.values, columns=data.columns, index=[self.symbol])
        return data
    
        
        


    def check_table(self):
        table_name = "ohlc" + self.symbol + "_" + self.interval
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
        query = f"SELECT MAX(startingAt) FROM ohlc{self.symbol}_{self.interval}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        if result is not None:
            return datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
        else:
            month = datetime.timedelta(days=180)  #=6month
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
            self.limit = (now -
                          self.latest_timestamp).total_seconds() // (3600)
            print(self.limit)

            if self.limit == 1:
                return None

            else:
                self.params['limit'] = int(self.limit) - 1

            print(
                self.params['limit']
            )  # set the limit based on the time difference between the latest timestamp and now

        else:
            self.params[
                'limit'] = 1  # set limit to 1 if the latest timestamp is in the future

    def retrieve_data2(self):
        self.check_table()
        self.set_limit()
        self.cursor.execute(
            f"SELECT MAX(endingAt) FROM ohlc{self.symbol}_{self.interval}")
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
            new_data.to_sql(f"ohlc{self.symbol}_{self.interval}",
                            self.conn,
                            if_exists="append",
                            index=False)
            self.cursor.execute(
                f"SELECT * FROM ohlc{self.symbol}_{self.interval} ORDER BY startingAt DESC;"
            )
            self.conn.commit()

        self.cursor.execute(
            f"SELECT COUNT(*) FROM ohlc{self.symbol}_{self.interval}")
        result = self.cursor.fetchone()
        print(
            f"Added {len(new_data)} new records to ohlc{self.symbol}_{self.interval}. Total records: {result[0]}")
        self.SMA()
        self.EMA()
        self.WMA()
        cr = cl.CoinPriceHistory(self.uuid, self.symbol,self.name)
        cr.retrieve_data()


    def retrieve_data(self):
        response = requests.get(self.url,
                                params=self.params,
                                headers=self.headers)
        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()
        data = json.loads(response.text)
        self.df = pd.DataFrame(data["data"]["ohlc"])
        self.df["startingAt"] = self.df["startingAt"].apply(
            lambda x: datetime.datetime.fromtimestamp(x))
        self.df["endingAt"] = self.df["endingAt"].apply(
            lambda x: datetime.datetime.fromtimestamp(x))
        
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


    def save_to_excel(self):
        self.df.to_excel('coinrankingohlc.xlsx',
                         sheet_name=self.symbol + "_" + self.interval,
                         index=True)

    def save_to_database(self):
        self.df.to_sql("ohlc" + self.symbol + "_" + self.interval,
                       self.conn,
                       if_exists="replace")
        
    def SMA(self):
        self.add_column()        
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval +  " ORDER BY startingAt ASC;"
        db = pd.read_sql_query(query, self.conn)
        sma10 = db['close'].rolling(window=240).mean() #10days = 240 datas
        sma50 = db['close'].rolling(window=1200).mean() #50days = 1200 datas
        query = "UPDATE ohlc" + self.symbol + "_" + self.interval + " SET SMA10=?,SMA50=? WHERE startingAt=?"
        data = [(sma10[i],sma50[i], db['startingAt'][i]) for i in range(len(sma10))]

        self.cursor.executemany(query, data)
        self.conn.commit()

    def EMA(self):
        self.add_column()
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval +  " ORDER BY startingAt ASC;"
        db = pd.read_sql_query(query, self.conn)

        ema10 = db['close'].ewm(span=240, adjust=False).mean()
        ema50 = db['close'].ewm(span=1200, adjust=False).mean()
        query = "UPDATE ohlc" + self.symbol + "_" + self.interval + " SET EMA10=?,EMA50=? WHERE startingAt=?"
        data = [(ema10[i],ema50[i], db['startingAt'][i]) for i in range(len(ema10))]

        self.cursor.executemany(query, data)
        self.conn.commit()

    def WMA(self):
        self.add_column()
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + " ORDER BY startingAt ASC;"
        db = pd.read_sql_query(query, self.conn)

        periods_10d = 240  # Choose the number of periods to use for WMA
        weights_10d = np.arange(1, periods_10d+1)
        wma10 = db['close'].rolling(window=periods_10d, min_periods=periods_10d).apply(lambda prices: (prices * weights_10d).sum() / weights_10d.sum(), raw=True)

        periods_50d = 1200  # Choose the number of periods to use for WMA
        weights_50d = np.arange(1, periods_50d+1)
        wma50 = db['close'].rolling(window=periods_50d, min_periods=periods_50d).apply(lambda prices: (prices * weights_50d).sum() / weights_50d.sum(), raw=True)

        query = "UPDATE ohlc" + self.symbol + "_" + self.interval + " SET WMA10=?,WMA50=? WHERE startingAt=?"
        data = [(wma10[i],wma50[i], db['startingAt'][i]) for i in range(len(wma10))]

        self.cursor.executemany(query, data)
        self.conn.commit()

       


    def show_candlestick(self):
        self.retrieve_data2()
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + " ORDER BY startingAt ASC;"
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
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + " ORDER BY startingAt ASC;"
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
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + " ORDER BY startingAt ASC;"
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
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + " ORDER BY startingAt ASC;"
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
        table_name = "ohlc" + self.symbol + "_" + self.interval

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
        query = "SELECT * FROM ohlc" + self.symbol + "_" + self.interval + " ORDER BY startingAt ASC;"
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


if __name__ == "__main__":
    cr = CoinRankingOHLC("razxDUgYGNAdQ", "ETH", "Ethereum")
    # print(cr.get_lastest_val())
    # cr = CoinRankingOHLC("Qwsogvtv82FCd","BTC","Bitcoin")
    # print(cr.pandas_data())
    # cr = CoinRankingOHLC("xz24e0BjL", "minute","SHIB","Shiba Inu")
    # cr.get_symbol()
    # cr = CoinRankingOHLC(uuid, interval, limit)
    # cr.retrieve_data()
    # cr.save_to_database()
    # cr.retrieve_data2()
    #     # cr.save_to_excel()
    cr.show_candlestick()
    # cr.show_candlestick_with_SMA()
    # cr.show_candlestick_with_EMA()
    # cr.EMA()
    # cr.show_candlestick_and_linechart()
    # cr.show_candlestick_with_WMA()

    # cr.SMA()
    # cr.WMA()

#     # cr.close_connection()
