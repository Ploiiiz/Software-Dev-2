import sys
sys.path.append('..')
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from gui import Ui_MainWindow
import data,utils,db_utils
import os
import webbrowser

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

data_folder = db_utils.data_folder

stockslist = data.txt_to_list(data_folder,'stocks.txt')
cryptolist = data.txt_to_list(data_folder,'crypto.txt')

loadinghtml = '''
    <html>
<head>
<style>
    .center {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    }
    .loading-text {
    font-size: 3em;
    font-weight: bold;
    font-family: sans-serif;
    }
</style>
</head>
<body>
<div class="center">
    <div class="loading-text">Loading...</div>
</div>
</body>
</html>'''

ui = Ui_MainWindow(stockslist,cryptolist)
ui.setupUi(MainWindow)

# Graph
GraphLayout = QtWidgets.QVBoxLayout()
GraphLayout.addWidget(ui.candle_widget)
ui.GraphWidget.setLayout(GraphLayout)

# Spatial
SpatialLayout = QtWidgets.QVBoxLayout()
SpatialLayout.addWidget(ui.spatial_widget)
ui.SpatialGraphWidget.setLayout(SpatialLayout)

def setMode():
    ui.checked = ui.Switch.isChecked()
    if ui.checked == True:
        ui.mode = 'Crypto'
        ui.Coins.setText('Crypto')
        ui.Stocks.setText('     ')
        ui.SymbolList.clear()
        ui.SymbolList.addItems(cryptolist)
    else:
        ui.mode = 'Stocks'
        ui.Coins.setText('     ')
        ui.Stocks.setText('Stocks')
        ui.SymbolList.clear()
        ui.SymbolList.addItems(stockslist)
ui.Switch.stateChanged.connect(setMode)

def symbol_clicked():
    current = ui.SymbolList.currentItem().text()
    print(current)
    ui.candle_widget.setHtml(loadinghtml)
    ui.spatial_widget.setHtml(loadinghtml)
    update_current_title(['' for i in range(10)])
    ui.current_symbol = current
    ui.SymbolTitle.setText(current)

    ui.quote_thread = LoadQuoteThread(current)
    ui.graph_thread = PlottingThread(current)
    ui.news_thread = NewsThread(current)
    ui.spatial_thread = SpatialThread(current)
    # ui.overview_thread = OverviewThread(current)
    # ui.balancesheet_thread = PlotBalanceSheetThread(current)

    ui.quote_thread.finished.connect(handle_load_quote_thread_finished)
    ui.graph_thread.finished.connect(update_graph)
    ui.news_thread.finished.connect(set_news)
    ui.spatial_thread.finished.connect(set_spatial)
    # ui.overview_thread.finished.connect(ui.handle_load_overview_finished)
    # ui.balancesheet_thread.finished.connect(ui.handle_load_balance_sheet_finished)

    ui.quote_thread.start()
    ui.graph_thread.start()
    ui.news_thread.start()
    ui.spatial_thread.start()
    # ui.overview_thread.start()
ui.SymbolList.itemClicked.connect(symbol_clicked)

def add_button_clicked():
    searchsymbol = ui.SearchBar.text()
    if ui.mode.lower() == 'stocks' and searchsymbol not in ui.stocks and searchsymbol+'.BK' not in ui.stocks:
        available = data.check_available(searchsymbol)
        if available != None:
            data.append_one(data_folder,'stocks.txt',available)
            ui.stocks.append(available)
            ui.SymbolList.addItem(available)
    elif ui.mode.lower() == 'crypto' and searchsymbol+'-USD' not in ui.coins:
        available = data.check_available(searchsymbol+'-USD')
        if available != None:
            data.append_one(data_folder,'crypto.txt',available)
            ui.coins.append(available)
            ui.SymbolList.addItem(available)
ui.AddSymbolButton.clicked.connect(add_button_clicked)

def del_button_clicked():
    current = ui.SymbolList.currentItem()
    if ui.mode.lower() == 'stocks':
        data.delete_one(data_folder,'stocks.txt',current.text())
        data.delete_all_table(current.text())
        ui.stocks.remove(current.text())
        ui.candle_widget.setHtml('')
        ui.SymbolList.clear()
        ui.SymbolList.addItems(stockslist)
    elif ui.mode.lower() == 'crypto':
        data.delete_one(data_folder,'crypto.txt',current.text())
        data.delete_all_table(current.text())
        ui.coins.remove(current.text())
        ui.candle_widget.setHtml('')
        ui.SymbolList.clear()
        ui.SymbolList.addItems(cryptolist)
ui.DelSymbolButton.clicked.connect(del_button_clicked)

def update_graph(html):
    ui.candle_widget.setHtml(html)

def update_current_title(quote):
        fullname,exchange,opn,high,low,prevclose,price,change,changeper,vol = quote
        name = fullname
        exchange = exchange
        if name != '':
            fullname = name+' | '+exchange
        else:
            fullname = ''
        ui.SymbolTitle.setText(ui.current_symbol)
        ui.FullName.setText(fullname)
        ui.CurrentPrice.setText(price)
        if change != '' and vol != '':
            changetext = '{}({})'.format(change,changeper)
            ui.Change.setText(changetext)
            ui.Vol.setText('Vol. ' + vol)
            ui.OpenText.setText('Open')
            ui.LowText.setText('Low')
            ui.PrevCloseText.setText('Previous Close')
            ui.HighText.setText('High')
        else:
            ui.OpenText.setText('')
            ui.LowText.setText('')
            ui.PrevCloseText.setText('')
            ui.HighText.setText('')
            ui.Change.setText('')
            ui.Vol.setText('')
        ui.OpenPrice.setText(opn[:-1])
        ui.HighPrice.setText(high[:-1])
        ui.LowPrice.setText(low[:-1])
        ui.PrevClosePrice.setText(prevclose[:-1])

def handle_load_quote_thread_finished(quote):
        # Update the UI with the results from the worker thread
        update_current_title(quote)

class News(QtWidgets.QWidget):
    def __init__(self,news):
        headline, url, source, timestamp, tags, tickers, summary, sentiment_score, sentiment_label = news
        self.url = url
        super().__init__()
        self.cont_layout = QtWidgets.QGridLayout(self) # Widget Layout
        self.cont_layout.setHorizontalSpacing(25)
        self.cont_layout.setVerticalSpacing(15)
        self.Time = QtWidgets.QLabel(parent=self)
        self.Time.setText(data.time_since(timestamp))
        self.cont_layout.addWidget(self.Time, 1, 1, 1, 1)

        self.Headline = QtWidgets.QLabel(parent=self)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Headline.setFont(font)
        self.Headline.setText(headline)
        self.Headline.setWordWrap(True)
        self.cont_layout.addWidget(self.Headline, 0, 0, 1, 3)

        self.Source = QtWidgets.QLabel(parent=self)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Source.setFont(font)
        self.Source.setText(source)
        self.cont_layout.addWidget(self.Source, 1, 0, 1, 1)

        self.SentimentLabel = QtWidgets.QLabel(parent=self)
        self.SentimentLabel.setText(sentiment_label)
        self.cont_layout.addWidget(self.SentimentLabel, 1, 2, 1, 1)

        self.Summary = QtWidgets.QLabel(parent=self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Summary.setFont(font)
        self.Summary.setText(summary)
        self.Summary.setWordWrap(True)
        self.cont_layout.addWidget(self.Summary, 2, 0, 1, 3)

        self.cont_layout.setColumnStretch(0, 1)
        self.cont_layout.setColumnStretch(1, 1)
        self.cont_layout.setColumnStretch(2, 11)
        self.cont_layout.setRowStretch(0, 3)
        self.cont_layout.setRowStretch(1, 2)
        self.cont_layout.setRowStretch(2, 6)

    def open_url(self):
        # Use the webbrowser module to open the URL in the default browser
        webbrowser.open(self.url)

ui.NewsListWidget.setItemDelegate(QtWidgets.QStyledItemDelegate())
def set_news(news_list):
    ui.NewsListWidget.clear()
    for i in news_list:
        news_obj = News(i)
        item = QtWidgets.QListWidgetItem()
        item_size = QtCore.QSize(250,150)  # set the height to 120 pixels
        item.setSizeHint(item_size)
        ui.NewsListWidget.addItem(item)
        ui.NewsListWidget.setItemWidget(item,news_obj)
class NewsThread(QThread):
    finished = pyqtSignal(list)
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        self.mode = ui.mode.lower()
    
    def run(self):
        if self.mode == 'stocks':
            try:
                newsfeed = data.fetch_news(self.symbol,50)[0]
                self.finished.emit(newsfeed)
            except Exception as e:
                print(e)
                self.finished.emit([])
        else:
            try:
                symbol = self.symbol[:-4]
                newsfeed = data.fetch_news('CRYPTO:'+symbol,50)[0]
                self.finished.emit(newsfeed)
            except Exception as e:
                print(e)
                self.finished.emit([])

def set_spatial(html):
    ui.spatial_widget.setHtml(html)
class SpatialThread(QThread):
    finished = pyqtSignal(str)
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        self.mode = ui.mode.lower()

    def run(self):
        if self.mode == 'stocks':
            try:
                newsfeed = data.fetch_news(self.symbol,50)[1]
                to_plot = data.add_coord(newsfeed)
                html = utils.spatial(to_plot)[1]
                self.finished.emit(html)
            except:
                html = '''
                    <html>
        <head>
            <style>
            .center {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .loading-text {
                font-size: 3em;
                font-weight: bold;
                font-family: sans-serif;
            }
            </style>
        </head>
        <body>
            <div class="center">
            <div class="loading-text">No Data :(</div>
            </div>
        </body>
        </html>'''
                self.finished.emit(html)
        else:
            try:
                symbol = self.symbol[:-4]
                newsfeed = data.fetch_news('CRYPTO:'+symbol,50)[1]
                to_plot = data.add_coord(newsfeed)
                html = utils.spatial(to_plot)[1]
                self.finished.emit(html)
            except:
                html = '''
                    <html>
        <head>
            <style>
            .center {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .loading-text {
                font-size: 3em;
                font-weight: bold;
                font-family: sans-serif;
            }
            </style>
        </head>
        <body>
            <div class="center">
            <div class="loading-text">No Data :(</div>
            </div>
        </body>
        </html>'''
                self.finished.emit(html)
class LoadQuoteThread(QThread):
    finished = pyqtSignal(tuple)

    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol

    def run(self):
        # Call the slow function in the worker thread
        quote = data.quote(self.symbol)
        if None not in quote:
            self.finished.emit(quote)
        elif quote[1] != None and quote[2] == None:
            self.finished.emit((quote[0],quote[1],'','','','','','','',''))
        else:
            self.finished.emit(('','','','','','','','','',''))

class OverviewThread(QThread):
    #TODO: Overview thread
    pass
class PlottingThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, symbol) :
        super().__init__()
        self.symbol = symbol
        self.mode = ui.mode.lower()
    
    def price_history(self):
        if self.symbol != None:
            table_name_suffix = ['_hourly_price_history','_daily_price_history','_weekly_price_history','_monthly_price_history']
            try:
                hour,day,week,month = data.read_all(self.symbol)
                if 'not found' not in hour and 'not found' not in day and 'not found' not in week and 'not found' not in month:
                    return hour,day,week,month
                else:
                    raise Exception
            except:
                dfh, hname = data.get_hourly_data(self.symbol)
                dfd, dname = data.get_daily_data(self.symbol)
                dfw, wname = data.get_weekly_data(self.symbol)
                dfm, mname = data.get_monthly_data(self.symbol)
                db_utils.store_table(dfh,hname)
                db_utils.store_table(dfd,dname)
                db_utils.store_table(dfw,wname)
                db_utils.store_table(dfm,mname)
                return (db_utils.read_table(hname),db_utils.read_table(dname),db_utils.read_table(wname),db_utils.read_table(mname))
        else:
            return None
    
    def run(self):
        if self.mode == 'stocks':
            h,d,w,m = self.price_history()
            if 'not found' not in h:
                html = utils.plot(h,d,w,m)[1]
                self.finished.emit(html)
            else:
                html = '''
                <html>
    <head>
        <style>
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .loading-text {
            font-size: 3em;
            font-weight: bold;
            font-family: sans-serif;
        }
        </style>
    </head>
    <body>
        <div class="center">
        <div class="loading-text">No Data :(</div>
        </div>
    </body>
    </html>'''
                self.finished.emit(html)
        elif self.mode == 'crypto':
            h,d,w,m = self.price_history()
            if 'not found' not in h:
                html = utils.plot(h,d,w,m)[1]
                self.finished.emit(html)
            else:
                html = '''
                <html>
    <head>
        <style>
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .loading-text {
            font-size: 3em;
            font-weight: bold;
            font-family: sans-serif;
        }
        </style>
    </head>
    <body>
        <div class="center">
        <div class="loading-text">No Data :(</div>
        </div>
    </body>
    </html>'''
                self.finished.emit(html)
        


if __name__ == "__main__":
    ui.SymbolList.addItems(stockslist)
    MainWindow.show()
    sys.exit(app.exec())
