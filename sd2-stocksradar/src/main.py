import sys
sys.path.append('..')
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from gui import Ui_MainWindow
import data,utils,db_utils
import os

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

data_folder = db_utils.data_folder

stockslist = data.txt_to_list(data_folder,'stocks.txt')
cryptolist = data.txt_to_list(data_folder,'crypto.txt')

ui = Ui_MainWindow(stockslist,cryptolist)
ui.setupUi(MainWindow)

# Graph
GraphLayout = QtWidgets.QVBoxLayout()
GraphLayout.addWidget(ui.candle_widget)
ui.GraphWidget.setLayout(GraphLayout)

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
        ui.candle_widget.setHtml('''
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
</html>''')
        ui.current_symbol = current
        ui.SymbolTitle.setText(current)

        # ui.quote_thread = LoadQuoteThread(current)
        ui.graph_thread = PlottingThread(current)
        # ui.overview_thread = OverviewThread(current)
        # ui.balancesheet_thread = PlotBalanceSheetThread(current)

        # ui.quote_thread.finished.connect(ui.handle_load_quote_thread_finished)
        ui.graph_thread.finished.connect(update_graph)
        # ui.overview_thread.finished.connect(ui.handle_load_overview_finished)
        # ui.balancesheet_thread.finished.connect(ui.handle_load_balance_sheet_finished)

        # ui.quote_thread.start()
        ui.graph_thread.start()
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
        #TODO: Remove Item from database
        data.delete_one(data_folder,'crypto.txt',current.text())
        data.delete_all_table(current.text())
        ui.coins.remove(current.text())
        ui.candle_widget.setHtml('')
        ui.SymbolList.clear()
        ui.SymbolList.addItems(cryptolist)
ui.DelSymbolButton.clicked.connect(del_button_clicked)

def update_graph(html):
    ui.candle_widget.setHtml(html)
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
