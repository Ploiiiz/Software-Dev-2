import credentials
import av_caller
import transformer
import db
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pl
from plotly.subplots import make_subplots
from datetime import datetime
from sqlite3 import IntegrityError
import time
from prettified import *

key = credentials.av_api_key

def load_quote(symbol):
    table_name = symbol + '_quotes'
    try:
        print('loading',table_name)
        df = db.read_table(table_name)
        return df
    except Exception:
        print('pull')
        data, table_name = prettified_quote_endpoint(symbol)
        db.store_data(data, table_name)
        df = db.read_table(table_name)
        return df

def load_all_prices(symbol):

    try:
        daily_df = db.read_table(symbol+'_daily_price_history')
        weekly_df = db.read_table(symbol+'_weekly_price_history')
        monthly_df = db.read_table(symbol+'_monthly_price_history')

        return daily_df, weekly_df, monthly_df

    except Exception:
        daily, daily_table = prettified_daily(symbol)
        weekly, weekly_table = prettified_weekly(symbol)
        monthly, monthly_table = prettified_monthly(symbol)
        db.store_data(daily, daily_table)
        db.store_data(weekly, weekly_table)
        db.store_data(monthly, monthly_table)        
        return daily, weekly, monthly

def plot_figure(symbol):
    
    daily_data, weekly_data, monthly_data = load_all_prices(symbol)
    
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], shared_xaxes=True, vertical_spacing=0.1)
   
    layout = go.Layout(
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)',
    showlegend=False,
    )

    candlestick = go.Candlestick(x=daily_data.index,
                    open=daily_data['open'],
                    high=daily_data['high'],
                    low=daily_data['low'],
                    close=daily_data['close'],
                    name='Candlestick')
    volume = go.Bar(x=daily_data.index, y=daily_data['volume'], name='volume')


    updatemenus=[
        dict(
            type = "buttons",
            direction = "left",
            buttons=[
            {'label': '1D',
             'method': 'update',
             'args': [{'x': [daily_data.index],
                       'open': [daily_data['open']],
                       'high': [daily_data['high']],
                       'low': [daily_data['low']],
                       'close': [daily_data['close']]}]},
            {'label': '1W',
             'method': 'update',
             'args': [{'x': [weekly_data.index],
                       'open': [weekly_data['open']],
                       'high': [weekly_data['high']],
                       'low': [weekly_data['low']],
                       'close': [weekly_data['close']]}]},
            {'label': '1M',
             'method': 'update',
             'args': [{'x': [monthly_data.index],
                       'open': [monthly_data['open']],
                       'high': [monthly_data['high']],
                       'low': [monthly_data['low']],
                       'close': [monthly_data['close']]}]},           
        ],
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0,
            xanchor="left",
            y=1.3,
            yanchor="top"
        ),
    ]
    fig.add_trace(candlestick,row=1,col=1)
    fig.add_trace(volume,row=2,col=1)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    
    fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]), #hide weekends
        dict(values=["2015-12-25", "2016-01-01"])  # hide Christmas and New Year's
    ]
)

    fig.update_layout(layout, updatemenus=updatemenus)
    fig.update_layout(
            xaxis=dict(rangeselector=dict(buttons=list([
                # dict(count=1, label='1D', step='day', stepmode='backward'),
                dict(count=7, label='1W', step='day', stepmode='backward'),
                dict(count=1, label='1M', step='month', stepmode='backward'),
                dict(count=3, label='3M', step='month', stepmode='backward'),
                dict(count=6, label='6M', step='month', stepmode='backward'),
                dict(count=9, label='9M', step='month', stepmode='backward'),
                dict(count=1, label='1Y', step='year', stepmode='backward'),
                dict(count=3, label='3Y', step='year', stepmode='backward'),
                dict(count=5, label='5Y', step='year', stepmode='backward'),
                dict(step='all')
            ], ), ),
                    rangeslider=dict(visible=False),
                    type='date'),

        )
    return fig

def plot_html(symbol):
    html = pl.to_html(plot_figure(symbol), include_plotlyjs='cdn')
    return html

def load_overview(symbol):
    try:
        table_name = symbol+'_company_overview'
        df = db.read_table(table_name)
        return df
    except Exception:
        
        ov_tuple = prettified_overview(symbol)
        if ov_tuple != 'Invalid symbol':
            df,table_name = ov_tuple
            db.store_data(df,table_name)
            return df
        else:
            return 'Overview Not Available'
    
def plot_balance_sheet(symbol):
    df = load_balance_sheet(symbol)
    traces = []
    i = 0
    for col in df.columns:
        visible = [True if col == df.columns[0] else False for col in df.columns]
        trace = go.Bar(x=df.index, y=df[col], name=col, visible=visible[i])
        traces.append(trace)
        i+=1
    
    layout = go.Layout(title='Balance Sheet',
                   xaxis=dict(title='Fiscal Ending Date'),
                   yaxis=dict(title='Value'),
                   barmode='group',
                   updatemenus=[{'buttons': [{'args': [{'visible': [True if col == df.columns[0] else False for col in df.columns]},
                                                        {'title': df.columns[0]}],
                                             'label': df.columns[0],
                                             'method': 'update'},
                                            {'args': [{'visible': [True if col == df.columns[1] else False for col in df.columns]},
                                                      {'title': df.columns[1]}],
                                             'label': df.columns[1],
                                             'method': 'update'},
                                            {'args': [{'visible': [True if col == df.columns[2] else False for col in df.columns]},
                                                      {'title': df.columns[2]}],
                                             'label': df.columns[2],
                                             'method': 'update'},
                                            {'args': [{'visible': [True if col == df.columns[3] else False for col in df.columns]},
                                                      {'title': df.columns[3]}],
                                             'label': df.columns[3],
                                             'method': 'update'},
                                            {'args': [{'visible': [True if col == df.columns[4] else False for col in df.columns]},
                                                      {'title': df.columns[4]}],
                                             'label': df.columns[4],
                                             'method': 'update'},
                                            {'args': [{'visible': [True if col == df.columns[5] else False for col in df.columns]},
                                                      {'title': df.columns[5]}],
                                             'label': df.columns[5],
                                             'method': 'update'},
                                            {'args': [{'visible': [True if col == df.columns[6] else False for col in df.columns]},
                                                      {'title': df.columns[6]}],
                                             'label': df.columns[6],
                                             'method': 'update'},
                                            {'args': [{'visible': [True if col == df.columns[7] else False for col in df.columns]},
                                                      {'title': df.columns[7]}],
                                             'label': df.columns[7],
                                             'method': 'update'},
                                            {'args': [{'visible': [True if col == df.columns[8] else False for col in df.columns]},
                                                      {'title': df.columns[8]}],
                                             'label': df.columns[8],
                                             'method': 'update'},
                                            {'args': [{'visible': [True if col == df.columns[9] else False for col in df.columns]},
                                                      {'title': df.columns[9]}],
                                             'label': df.columns[9],
                                             'method': 'update'}],
                                 'direction': 'left',
                                 'showactive': True,
                                 'type': 'buttons'}])
    fig = go.Figure(data=traces, layout=layout)
    return fig

def load_balance_sheet(symbol):
    try:
        table_name = symbol+'_quarterly_balance_sheet'
        df = db.read_table(table_name)
        return df
    except Exception:
        df,table_name = prettified_quarterly_balance_sheet(symbol)
        db.store_data(df,table_name)
        return df

def plot_bs_html(symbol):
    html = pl.to_html(plot_balance_sheet(symbol), include_plotlyjs='cdn')
    return html
