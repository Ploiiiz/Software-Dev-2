import plotly.graph_objects as go
import plotly.io as pl
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import numpy as np

def daybreak(dfd):
    dates = pd.date_range(start=dfd.index[0],
                   end=dfd.index[-1],
                   freq='D')
    avail_dates = dfd.index
    daybreaks = [d for d in dates if d not in avail_dates]
    return daybreaks

def hourbreak(dfh):
    hours = pd.date_range(start=dfh.index[0],
                   end=dfh.index[-1],
                   freq='H')
    avail_hours = dfh.index
    hourbreaks = [d for d in hours if d not in avail_hours]
    return hourbreaks

def plot_html(fig):
    html = pl.to_html(fig, include_plotlyjs='cdn')
    return html

def plot(dfh,dfd,dfw,dfm):

    dfh, dfd, dfw, dfm = dfh[-60:], dfd[-365:], dfw, dfm
    daybreaks = daybreak(dfd)
    hourbreaks = hourbreak(dfh)

    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], shared_xaxes=True, vertical_spacing=0.1)
    y1dom = fig.layout.yaxis.domain 
    y2dom = fig.layout.yaxis2.domain 

    hour = go.Candlestick(x=dfh.index,
                        open=dfh['open'],
                        high=dfh['high'],
                        low=dfh['low'],
                        close=dfh['close'],
                        name='Candlestick',
                        visible=False)
    if 'SMA_50' in dfh.columns:
        sma_h = go.Scatter(x=dfh.index, y=dfh['SMA_50'],mode='lines',name='SMA50',visible=False,line=dict(color='dodgerblue'))
    else:
        sma_h = go.Scatter(x=None, y=None)
    volume_h = go.Bar(x=dfh.index, y=dfh['volume'], name='volume',visible=False)

    day = go.Candlestick(x=dfd.index,
                        open=dfd['open'],
                        high=dfd['high'],
                        low=dfd['low'],
                        close=dfd['close'],
                        name='Candlestick',
                        visible=False)
    if 'EMA_200' in dfd.columns:
        ema_d = go.Scatter(x=dfd.index, y=dfd['EMA_200'],mode='lines',name='EMA200',visible=False,line=dict(color='hotpink'))
    else:
        ema_d = go.Scatter(x=None, y=None)
    if 'SMA_50' in dfd.columns:
        sma_d = go.Scatter(x=dfd.index, y=dfd['SMA_50'],mode='lines',name='SMA50',visible=False,line=dict(color='dodgerblue'))
    else:
        sma_d = go.Scatter(x=None, y=None)
    volume_d = go.Bar(x=dfd.index, y=dfd['volume'], name='volume',visible=False)


    week = go.Candlestick(x=dfw.index,
                        open=dfw['open'],
                        high=dfw['high'],
                        low=dfw['low'],
                        close=dfw['close'],
                        name='Candlestick',
                        visible=False)
    if 'EMA_200' in dfw.columns:
        ema_w = go.Scatter(x=dfw.index, y=dfw['EMA_200'],mode='lines',name='EMA200',visible=False,line=dict(color='hotpink'))
    else:
        ema_w = go.Scatter(x=None, y=None)
    if 'SMA_50' in dfw.columns:    
        sma_w = go.Scatter(x=dfw.index, y=dfw['SMA_50'],mode='lines',name='SMA50',visible=False,line=dict(color='dodgerblue'))
    else:
        sma_w = go.Scatter(x=None, y=None)
    volume_w = go.Bar(x=dfw.index, y=dfw['volume'], name='volume',visible=False)

    month = go.Candlestick(x=dfm.index,
                        open=dfm['open'],
                        high=dfm['high'],
                        low=dfm['low'],
                        close=dfm['close'],
                        name='Candlestick',
                        visible=True)
    if 'EMA_200' in dfm.columns:
        ema_m = go.Scatter(x=dfm.index, y=dfm['EMA_200'],mode='lines',name='EMA200',visible=True,line=dict(color='hotpink'))
    else:
        ema_m = go.Scatter(x=None, y=None)
    if 'SMA_50' in dfm.columns:
        sma_m = go.Scatter(x=dfm.index, y=dfm['SMA_50'],mode='lines',name='SMA50',visible=True,line=dict(color='dodgerblue'))
    else:
        sma_m = go.Scatter(x=None, y=None)
    volume_m = go.Bar(x=dfm.index, y=dfm['volume'], name='volume',visible=True)

    # Define the updatemenus button
    dvalue = 60 * 60 * 1000  # 30min * 60sec/min * 1000msec/sec

    h_7d = -30 if len(dfh) >= 30 else -len(dfh)
    d_1m = -21 if len(dfd) >= 21 else -len(dfd)
    d_3m = -63 if len(dfd) >= 30 else -len(dfd)
    d_6m = -125 if len(dfd) >= 125 else -len(dfd)
    d_1y= -253 if len(dfd) >= 253 else -len(dfd)
    w_3y= -156 if len(dfw) >= 156 else -len(dfw)
    m_5y= -60 if len(dfm) >= 60 else -len(dfm)

    updatemenus = [{
        'active':8,
        'direction':'left',
        'y':1.2,
        'yanchor':'top',
        'xanchor':'left',
        'type': 'buttons',
        'buttons': [dict(label='7D',
                            method='update',
                            args=[dict(visible = [True,True,True, # Hour
                                                  False,False,False,False, # Day
                                                  False,False,False,False, # Week
                                                  False,False,False,False #Month
                                                  ]),
                                {'xaxis': {'range': [dfh.index[h_7d], dfh.index[-1]],
                                        'rangebreaks': [dict(values=hourbreaks,dvalue=dvalue)],
                                        'rangeslider': dict(visible=False),
                                        'type':'date'},
                            'xaxis2': {'range':[dfh.index[h_7d],dfh.index[-1]],'rangebreaks': [dict(values=hourbreaks,dvalue=dvalue)]},
                                'yaxis': {'range':[dfh[-30:].low.min()*0.97, dfh[-30:].high.max()*1.03],'domain':y1dom},
                                'yaxis2': {'range':[dfh[-30:].volume.min(), dfh[-30:].volume.max()*1.1],'domain':y2dom} },
                                ]),
                        dict(label='1M',
                            method='update',
                            args=[dict(visible = [False,False,False, # Hour
                                                  True,True,True,True, # Day
                                                  False,False,False,False, # Week
                                                  False,False,False,False #Month
                                                  ]),
                                {'xaxis': {'range': [dfd.index[d_1m], dfd.index[-1]],
                                            'rangebreaks': [dict(values=daybreaks)],
                                            'rangeslider': dict(visible=False),
                                            'type':'date'},
                                'xaxis2': {'range':[dfd.index[d_1m],dfd.index[-1]],'rangebreaks': [dict(values=daybreaks)]},
                                'yaxis': {'range':[dfd[-21:].low.min()*0.97, dfd[-21:].high.max()*1.03],'domain':y1dom},
                                'yaxis2': {'range':[dfd[-21:].volume.min(), dfd[-21:].volume.max()*1.1],'domain':y2dom} },
                                ]),
                        dict(label='3M',
                            method='update',
                            args=[dict(visible = [False,False,False, # Hour
                                                  True,True,True,True, # Day
                                                  False,False,False,False, # Week
                                                  False,False,False,False #Month
                                                  ]),
                                {'xaxis': {'range': [dfd.index[d_3m], dfd.index[-1]],
                                            'rangebreaks': [dict(values=daybreaks)],
                                            'rangeslider': dict(visible=False)},
                                'xaxis2': {'range':[dfd.index[d_3m],dfd.index[-1]],'rangebreaks': [dict(values=daybreaks)]},
                                'yaxis': {'range':[dfd[-63:].low.min()*0.97, dfd[-63:].high.max()*1.03],'domain':y1dom},
                                'yaxis2': {'range':[dfd[-63:].volume.min(), dfd[-63:].volume.max()*1.1],'domain':y2dom} },
                                ]),
                        dict(label='6M',
                            method='update',
                            args=[dict(visible = [False,False,False, # Hour
                                                  True,True,True,True, # Day
                                                  False,False,False,False, # Week
                                                  False,False,False,False #Month
                                                  ]),
                                {'xaxis': {'range': [dfd.index[d_6m], dfd.index[-1]],
                                            'rangebreaks': [dict(values=daybreaks)],
                                            'rangeslider': dict(visible=False)},
                                'xaxis2': {'range':[dfd.index[d_6m],dfd.index[-1]],'rangebreaks': [dict(values=daybreaks)]},
                                'yaxis': {'range':[dfd[-125:].low.min()*0.97, dfd[-125:].high.max()*1.03],'domain':y1dom},
                                'yaxis2': {'range':[dfd[-125:].volume.min(), dfd[-125:].volume.max()*1.1],'domain':y2dom} },         
                                ]),
                        dict(label='1Y',
                            method='update',
                            args=[dict(visible = [False,False,False, # Hour
                                                  True,True,True,True, # Day
                                                  False,False,False,False, # Week
                                                  False,False,False,False #Month
                                                  ]),
                                {'xaxis': {'range': [dfd.index[d_1y], dfd.index[-1]],
                                            'rangebreaks': [dict(values=daybreaks)],
                                            'rangeslider': dict(visible=False)},
                                'xaxis2': {'range':[dfd.index[d_1y],dfd.index[-1]],'rangebreaks': [dict(values=daybreaks)]},
                                'yaxis': {'range':[dfd[-253:].low.min()*0.97, dfd[-253:].high.max()*1.03],'domain':y1dom},
                                'yaxis2': {'range':[dfd[-253:].volume.min(), dfd[-253:].volume.max()*1.1],'domain':y2dom} }, 
                                            ]),
                        dict(label='3Y',
                            method='update',
                            args=[dict(visible = [False,False,False, # Hour
                                                  False,False,False,False, # Day
                                                  True,True,True,True, # Week
                                                  False,False,False,False #Month
                                                  ]),
                                {'xaxis': {'range': [dfw.index[w_3y], dfw.index[-1]],
                                            'rangeslider': dict(visible=False)},
                                'xaxis2': {'range':[dfw.index[w_3y],dfw.index[-1]]},
                                    'yaxis': {'range':[dfw[-156:].low.min()*0.97, dfw[-156:].high.max()*1.03],'domain':y1dom},
                                'yaxis2': {'range':[dfw[-156:].volume.min(), dfw[-156:].volume.max()],'domain':y2dom} },
                                    ]), 
                        dict(label='5Y',
                            method='update',
                            args=[dict(visible = [False,False,False, # Hour
                                                  False,False,False,False, # Day
                                                  True,True,True,True, # Week
                                                  False,False,False,False #Month
                                                  ]),
                                {'xaxis': {'range': [dfm.index[m_5y], dfm.index[-1]],
                                            'rangeslider': dict(visible=False)},
                                'xaxis2': {'range':[dfm.index[m_5y],dfd.index[-1]]},
                                    'yaxis': {'range':[dfm[-60:].low.min()*0.97, dfm[-60:].high.max()*1.03],'domain':y1dom},
                                'yaxis2': {'range':[dfm[-60:].volume.min(), dfm[-60:].volume.max()],'domain':y2dom} },
                                    ]),
                        dict(label='All',
                            method='update',
                            args=[dict(visible = [False,False,False, # Hour
                                                  False,False,False,False, # Day
                                                  True,True,True,True, # Week
                                                  False,False,False,False #Month
                                                  ]),
                                {'xaxis': {'range': [dfm.index[0], dfd.index[-1]],
                                            'rangeslider': dict(visible=False)},
                                'xaxis2': {'range':[dfm.index[0],dfd.index[-1]]},
                                'yaxis': {'range':[dfm.low.min()*0.97, dfm.high.max()*1.03],'domain':y1dom},
                                'yaxis2': {'range':[dfm.volume.min(), dfm.volume.max()],'domain':y2dom} },
                                    ])

                                ]

    }]
    layout = dict(showlegend=False,
                xaxis=dict(rangeslider=dict(visible=False),type='date'),
                updatemenus=updatemenus)
    # Add the updatemenus button to the layout
    fig.add_traces(data=[hour,sma_h,volume_h,day,ema_d,sma_d,volume_d,week,ema_w,sma_w,volume_w,month,ema_m,sma_m,volume_m],
                cols = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                rows=[1,1,2,1,1,1,2,1,1,1,2,1,1,1,2])

    fig.update_layout(layout,margin=dict(b=0,l=0,r=0,t=10))
    # Show the plot
    
    return fig, plot_html(fig)

def spatial(locations_df):
    fig = px.density_mapbox(locations_df,
                     lat=locations_df['latitude'],
                     lon=locations_df['longitude'],
                     hover_name=locations_df['Location'],
                     zoom=0.6,
                     radius=15,
                     center=dict(lat=0,lon=0),
                     mapbox_style='carto-positron',
                     )
    fig.update_layout(margin=dict(l=0,
                                r=0,
                                b=10,
                                t=10),
                    )
    return fig, plot_html(fig)

def sector(colored_df):
    df = colored_df
    fig = go.Figure(go.Treemap(labels=df['sector'], values=df['cp'], parents=df['parents'], marker_colors=df['color'],
                customdata=np.stack((df['sector'],df['sign']),axis=1),
                hovertemplate='<b>%{customdata[0]} </b> <br> Change: %{customdata[1]}%{value}%<br>',name=''))

    # update the layout of the treemap
    fig.update_layout(
        margin=dict(l=0,
                    r=0,
                    b=10,
                    t=10),
    )

    return fig, plot_html(fig)

def balance_sheet(balance_sheet_df):
        
    data=[
        go.Bar(name='Total Assets', x=balance_sheet_df['fiscalDateEnding'], y=balance_sheet_df['totalAssets'],visible=True,marker_color='forestgreen'),
        go.Bar(name='Total Liabilities', x=balance_sheet_df['fiscalDateEnding'], y=balance_sheet_df['totalLiabilities'],visible=False,marker_color='darksalmon'),
        go.Bar(name='Total Shareholder Equity', x=balance_sheet_df['fiscalDateEnding'], y=balance_sheet_df['totalShareholderEquity'],visible=False,marker_color='darkturquoise'),
    ]
    updatemenus = [{
        'active':0,
        'direction':'left',
        'y':1.15,
        'yanchor':'top',
        'xanchor':'left',
        'type': 'buttons',
        'buttons': [
        dict(label='Total Assets',
            method='update',
            args=[dict(visible=[True,False,False]
            )]),
        dict(label='Total Liabilities',
            method='update',
            args=[dict(visible=[False,True,False])]),
        dict(label='Total Shareholder Equity',
            method='update',
            args=[dict(visible=[False,False,True])]),
        dict(label='All',
            method='update',
            args=[dict(visible=[True,True,True])]),
        ]
    }]
    fig = go.Figure(data=data)
    fig.update_layout(barmode='group',
                    yaxis=dict(type='linear'),
                    updatemenus=updatemenus,
                    title_text='Balance Sheet (USD)',
                    margin=dict(l=0,r=0,t=110,b=20))
    return fig,plot_html(fig)


def cash_flow(cash_flow_df):
        
    data=[
        go.Bar(name='Operating', x=cash_flow_df['fiscalDateEnding'], y=cash_flow_df['operatingCashflow'],visible=True,marker_color='#1B065E'),
        go.Bar(name='Investment', x=cash_flow_df['fiscalDateEnding'], y=cash_flow_df['cashflowFromInvestment'],visible=False,marker_color='#FF47DA'),
        go.Bar(name='Financing', x=cash_flow_df['fiscalDateEnding'], y=cash_flow_df['cashflowFromFinancing'],visible=False,marker_color='#C44900'),
        go.Bar(name='Change In Cash and Equivalents', x=cash_flow_df['fiscalDateEnding'], y=cash_flow_df['changeInCashAndCashEquivalents'],visible=False,marker_color='#426B69'),
    ]
    updatemenus = [{
        'active':0,
        'direction':'left',
        'y':1.15,
        'yanchor':'top',
        'xanchor':'left',
        'type': 'buttons',
        'buttons': [
        dict(label='Operating Cash Flow',
            method='update',
            args=[dict(visible=[True,False,False,False]
            )]),
        dict(label='Investment Cash Flow',
            method='update',
            args=[dict(visible=[False,True,False,False])]),
        dict(label='Financing Cash Flow',
            method='update',
            args=[dict(visible=[False,False,True,False])]),
        dict(label='Change In Cash and Equivalents',
            method='update',
            args=[dict(visible=[False,False,False,True])]),
        dict(label='All',
            method='update',
            args=[dict(visible=[True,True,True,True])]),
        ]
    }]
    fig = go.Figure(data=data)
    fig.update_layout(barmode='group',
                    yaxis=dict(type='linear'),
                    updatemenus=updatemenus,
                    title_text='Cash Flow (USD)',
                    margin=dict(l=0,r=0,t=110,b=20))
    return fig,plot_html(fig)

def income_statement(income_statement_df):
        
    data=[
        go.Bar(name='Gross Profit', x=income_statement_df['fiscalDateEnding'], y=income_statement_df['grossProfit'],visible=True,marker_color='#87C38F'),
        go.Bar(name='Total Revenue', x=income_statement_df['fiscalDateEnding'], y=income_statement_df['totalRevenue'],visible=False,marker_color='#226F54'),
        go.Bar(name='Cost of Revenue', x=income_statement_df['fiscalDateEnding'], y=income_statement_df['costOfRevenue'],visible=False,marker_color='#DA2C38'),
        go.Bar(name='Operating Income', x=income_statement_df['fiscalDateEnding'], y=income_statement_df['operatingIncome'],visible=False,marker_color='#6369D1'),
        go.Bar(name='Net Income', x=income_statement_df['fiscalDateEnding'], y=income_statement_df['netIncome'],visible=False,marker_color='#0A2342'),
    ]
    updatemenus = [{
        'active':0,
        'direction':'left',
        'y':1.15,
        'yanchor':'top',
        'xanchor':'left',
        'type': 'buttons',
        'buttons': [
        dict(label='Gross Profit',
            method='update',
            args=[dict(visible=[True,False,False,False,False]
            )]),
        dict(label='Total Revenue',
            method='update',
            args=[dict(visible=[False,True,False,False,False])]),
        dict(label='Cost of Revenue',
            method='update',
            args=[dict(visible=[False,False,True,False,False])]),
        dict(label='Operating Income',
            method='update',
            args=[dict(visible=[False,False,False,True,False])]),
        dict(label='Net Income',
            method='update',
            args=[dict(visible=[False,False,False,False,True])]),
        dict(label='All',
            method='update',
            args=[dict(visible=[True,True,True,True,True])]),
        ]
    }]
    fig = go.Figure(data=data)
    fig.update_layout(barmode='group',
                    yaxis=dict(type='linear'),
                    updatemenus=updatemenus,
                    title_text='Income Statement (USD)',
                    margin=dict(l=0,r=0,t=110,b=20))
    return fig,plot_html(fig)

