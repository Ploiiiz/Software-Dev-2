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
            open=self.data['open'],
            high=self.data['high'],
            low=self.data['low'],
            close=self.data['close'])])
        return fig