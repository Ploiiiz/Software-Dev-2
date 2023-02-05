import plotly.graph_objects as go
import matplotlib.pyplot as plt
import mplfinance

class Plotter:
    def __init__(self,dataframe) -> None:
        self.data = dataframe
        self.fig = self.timeseries_fig()
    def timeseries_fig(self):
        fig = go.Figure(data=[go.Candlestick(
            x=self.data.index,
            open=self.data['1. open'],
            high=self.data['2. high'],
            low=self.data['3. low'],
            close=self.data['4. close'])])
        return fig