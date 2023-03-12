# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\simplegui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView

import mainpackage as main

with open(r'New API\testing\stocks.txt','r') as stocks:
    stockslist = []
    for stock in stocks:
        stock = stock.strip()
        stockslist.append(stock)

import pandas as pd
statuses = pd.read_csv('listing_status.csv').set_index('symbol')

class Ui_MainWindow(object):
    def __init__(self,stocklist,coinlist):
        self.current_symbol = None
        self.checked = False
        self.mode = 'Stocks'
        self.currency = 'USD'
        self.stocks = stocklist
        self.coins = coinlist

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(994, 669)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        MainWindow.setFont(font)
        self.MainWidget = QtWidgets.QWidget(MainWindow)
        self.MainWidget.setObjectName("MainWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.MainWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.MainLayout = QtWidgets.QFrame(self.MainWidget)
        self.MainLayout.setObjectName("MainLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.MainLayout)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ListingsArea = QtWidgets.QVBoxLayout()
        self.ListingsArea.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.ListingsArea.setContentsMargins(15, 15, 15, 15)
        self.ListingsArea.setSpacing(10)
        self.ListingsArea.setObjectName("ListingsArea")
        self.SwitchandCurrency = QtWidgets.QHBoxLayout()
        self.SwitchandCurrency.setObjectName("SwitchandCurrency")
        self.Stocks = QtWidgets.QLabel(self.MainLayout)
        self.Stocks.setObjectName("Stocks")
        self.SwitchandCurrency.addWidget(self.Stocks)
        self.Switch = QtWidgets.QCheckBox(self.MainLayout)
        self.Switch.setText("")
        self.Switch.setObjectName("Switch")
        self.SwitchandCurrency.addWidget(self.Switch)
        self.Coins = QtWidgets.QLabel(self.MainLayout)
        self.Coins.setObjectName("Coins")
        self.SwitchandCurrency.addWidget(self.Coins)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.SwitchandCurrency.addItem(spacerItem)
        self.currencyBox = QtWidgets.QComboBox(self.MainLayout)
        self.currencyBox.setObjectName("comboBox")
        self.currencyBox.addItem("")
        self.currencyBox.addItem("")
        self.SwitchandCurrency.addWidget(self.currencyBox)
        self.SwitchandCurrency.setStretch(0, 2)
        self.SwitchandCurrency.setStretch(1, 1)
        self.SwitchandCurrency.setStretch(2, 2)
        self.SwitchandCurrency.setStretch(3, 7)
        self.SwitchandCurrency.setStretch(4, 1)
        self.ListingsArea.addLayout(self.SwitchandCurrency)
        self.SymbolandRefresh = QtWidgets.QHBoxLayout()
        self.SymbolandRefresh.setObjectName("SymbolandRefresh")
        self.SymbolText = QtWidgets.QLabel(self.MainLayout)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.SymbolText.setFont(font)
        self.SymbolText.setObjectName("SymbolText")
        self.SymbolandRefresh.addWidget(self.SymbolText)
        self.refreshButton = QtWidgets.QPushButton(self.MainLayout)
        self.refreshButton.setObjectName("pushButton")
        self.SymbolandRefresh.addWidget(self.refreshButton)
        self.SymbolandRefresh.setStretch(0, 4)
        self.SymbolandRefresh.setStretch(1, 1)
        self.ListingsArea.addLayout(self.SymbolandRefresh)
        self.Search = QtWidgets.QHBoxLayout()
        self.Search.setObjectName("Search")
        self.SearchBar = QtWidgets.QLineEdit(self.MainLayout)
        self.SearchBar.setObjectName("SearchBar")
        self.Search.addWidget(self.SearchBar)
        self.AddSymbolButton = QtWidgets.QPushButton(self.MainLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddSymbolButton.sizePolicy().hasHeightForWidth())
        self.AddSymbolButton.setSizePolicy(sizePolicy)
        self.AddSymbolButton.setObjectName("AddSymbolButton")
        self.Search.addWidget(self.AddSymbolButton)
        self.Search.setStretch(0, 5)
        self.Search.setStretch(1, 1)
        self.ListingsArea.addLayout(self.Search)
        self.SymbolList = QtWidgets.QListWidget(self.MainLayout)
        self.SymbolList.setObjectName("SymbolList")
        self.ListingsArea.addWidget(self.SymbolList)
        self.ListingsArea.setStretch(0, 1)
        self.ListingsArea.setStretch(1, 1)
        self.ListingsArea.setStretch(2, 1)
        self.ListingsArea.setStretch(3, 13)
        self.horizontalLayout.addLayout(self.ListingsArea)
        self.DisplayArea = QtWidgets.QVBoxLayout()
        self.DisplayArea.setContentsMargins(5, 5, 5, 5)
        self.DisplayArea.setSpacing(5)
        self.DisplayArea.setObjectName("DisplayArea")
        self.SymbolandPrice = QtWidgets.QHBoxLayout()
        self.SymbolandPrice.setContentsMargins(5, 5, 5, 5)
        self.SymbolandPrice.setObjectName("SymbolandPrice")
        self.SymandName = QtWidgets.QVBoxLayout()
        self.SymandName.setObjectName("SymandName")
        self.SymbolTitle = QtWidgets.QLabel(self.MainLayout)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.SymbolTitle.setFont(font)
        self.SymbolTitle.setObjectName("SymbolTitle")
        self.SymandName.addWidget(self.SymbolTitle)
        self.FullName = QtWidgets.QLabel(self.MainLayout)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.FullName.setFont(font)
        self.FullName.setObjectName("FullName")
        self.SymandName.addWidget(self.FullName)
        self.SymandName.setStretch(0, 2)
        self.SymbolandPrice.addLayout(self.SymandName)
        self.Prices = QtWidgets.QVBoxLayout()
        self.Prices.setObjectName("Prices")
        self.CurrentPrice = QtWidgets.QLabel(self.MainLayout)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.CurrentPrice.setFont(font)
        self.CurrentPrice.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.CurrentPrice.setObjectName("CurrentPrice")
        self.Prices.addWidget(self.CurrentPrice)
        self.Change = QtWidgets.QLabel(self.MainLayout)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Change.setFont(font)
        self.Change.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Change.setObjectName("Change")
        self.Prices.addWidget(self.Change)
        self.Vol = QtWidgets.QLabel(self.MainLayout)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Vol.setFont(font)
        self.Vol.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Vol.setObjectName("Vol")
        self.Prices.addWidget(self.Vol)
        self.Prices.setStretch(0, 2)
        self.Prices.setStretch(1, 1)
        self.Prices.setStretch(2, 1)
        self.SymbolandPrice.addLayout(self.Prices)
        self.SymbolandPrice.setStretch(0, 2)
        self.SymbolandPrice.setStretch(1, 1)
        self.DisplayArea.addLayout(self.SymbolandPrice)
        self.Tabs = QtWidgets.QTabWidget(self.MainLayout)
        self.Tabs.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.Tabs.setElideMode(QtCore.Qt.ElideNone)
        self.Tabs.setObjectName("Tabs")
        self.Price = QtWidgets.QWidget()
        self.Price.setObjectName("Price")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Price)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.GraphArea = QtWidgets.QFrame(self.Price)
        self.GraphArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.GraphArea.setFrameShadow(QtWidgets.QFrame.Raised)
        self.GraphArea.setObjectName("GraphArea")
        
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.GraphArea)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.thismf = QtWidgets.QVBoxLayout()
        self.thismf.setObjectName("thismf")
        self.horizontalLayout_4.addLayout(self.thismf)
        
        self.verticalLayout_2.addWidget(self.GraphArea)
        self.PriceInfoArea = QtWidgets.QHBoxLayout()
        self.PriceInfoArea.setContentsMargins(1, 1, 1, 1)
        self.PriceInfoArea.setSpacing(3)
        self.PriceInfoArea.setObjectName("PriceInfoArea")
        self.OpenLabel = QtWidgets.QHBoxLayout()
        self.OpenLabel.setObjectName("OpenLabel")
        self.OpenText = QtWidgets.QLabel(self.Price)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.OpenText.setFont(font)
        self.OpenText.setAlignment(QtCore.Qt.AlignCenter)
        self.OpenText.setObjectName("OpenText")
        self.OpenLabel.addWidget(self.OpenText)
        self.OpenPrice = QtWidgets.QLabel(self.Price)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.OpenPrice.setFont(font)
        self.OpenPrice.setObjectName("OpenPrice")
        self.OpenLabel.addWidget(self.OpenPrice)
        self.PriceInfoArea.addLayout(self.OpenLabel)
        self.HighLabel = QtWidgets.QHBoxLayout()
        self.HighLabel.setObjectName("HighLabel")
        self.HighText = QtWidgets.QLabel(self.Price)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.HighText.setFont(font)
        self.HighText.setAlignment(QtCore.Qt.AlignCenter)
        self.HighText.setObjectName("HighText")
        self.HighLabel.addWidget(self.HighText)
        self.HighPrice = QtWidgets.QLabel(self.Price)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.HighPrice.setFont(font)
        self.HighPrice.setObjectName("HighPrice")
        self.HighLabel.addWidget(self.HighPrice)
        self.PriceInfoArea.addLayout(self.HighLabel)
        self.LowText_2 = QtWidgets.QHBoxLayout()
        self.LowText_2.setObjectName("LowText_2")
        self.LowText = QtWidgets.QLabel(self.Price)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.LowText.setFont(font)
        self.LowText.setAlignment(QtCore.Qt.AlignCenter)
        self.LowText.setObjectName("LowText")
        self.LowText_2.addWidget(self.LowText)
        self.LowPrice = QtWidgets.QLabel(self.Price)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.LowPrice.setFont(font)
        self.LowPrice.setObjectName("LowPrice")
        self.LowText_2.addWidget(self.LowPrice)
        self.PriceInfoArea.addLayout(self.LowText_2)
        self.CloseText = QtWidgets.QHBoxLayout()
        self.CloseText.setObjectName("CloseText")
        self.PrevCloseText = QtWidgets.QLabel(self.Price)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PrevCloseText.setFont(font)
        self.PrevCloseText.setAlignment(QtCore.Qt.AlignCenter)
        self.PrevCloseText.setWordWrap(True)
        self.PrevCloseText.setObjectName("PrevCloseText")
        self.CloseText.addWidget(self.PrevCloseText)
        self.PrevClosePrice = QtWidgets.QLabel(self.Price)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PrevClosePrice.setFont(font)
        self.PrevClosePrice.setObjectName("PrevClosePrice")
        self.CloseText.addWidget(self.PrevClosePrice)
        self.CloseText.setStretch(0, 1)
        self.CloseText.setStretch(1, 1)
        self.PriceInfoArea.addLayout(self.CloseText)
        self.PriceInfoArea.setStretch(0, 1)
        self.PriceInfoArea.setStretch(1, 1)
        self.PriceInfoArea.setStretch(2, 1)
        self.PriceInfoArea.setStretch(3, 1)
        self.verticalLayout_2.addLayout(self.PriceInfoArea)
        self.verticalLayout_2.setStretch(0, 7)
        self.verticalLayout_2.setStretch(1, 1)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.Tabs.addTab(self.Price, "")
        self.News = QtWidgets.QWidget()
        self.News.setObjectName("News")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.News)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.listWidget = QtWidgets.QListWidget(self.News)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.gridLayout_3.addWidget(self.listWidget, 0, 0, 1, 1)
        self.Tabs.addTab(self.News, "")
        self.Spatial = QtWidgets.QWidget()
        self.Spatial.setObjectName("Spatial")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.Spatial)
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_4.setHorizontalSpacing(2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.SpatialFrame = QtWidgets.QFrame(self.Spatial)
        self.SpatialFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SpatialFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SpatialFrame.setObjectName("SpatialFrame")
        self.gridLayout_4.addWidget(self.SpatialFrame, 0, 0, 1, 1)
        self.Tabs.addTab(self.Spatial, "")
        self.Overview = QtWidgets.QWidget()
        self.Overview.setObjectName("Overview")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.Overview)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.scrollArea = QtWidgets.QScrollArea(self.Overview)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 709, 2018))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame.setMinimumSize(QtCore.QSize(0, 2000))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_25 = QtWidgets.QLabel(self.frame)
        self.label_25.setObjectName("label_25")
        self.gridLayout_9.addWidget(self.label_25, 1, 1, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.frame)
        self.label_24.setObjectName("label_24")
        self.gridLayout_9.addWidget(self.label_24, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_9.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_9.addWidget(self.label_5, 2, 1, 1, 1)
        self.Desc = QtWidgets.QLabel(self.frame)
        self.Desc.setObjectName("Desc")
        self.gridLayout_9.addWidget(self.Desc, 0, 0, 1, 2)
        self.gridLayout_10.addLayout(self.gridLayout_9, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_5.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.Tabs.addTab(self.Overview, "")
        self.IncomeStatement = QtWidgets.QWidget()
        self.IncomeStatement.setObjectName("IncomeStatement")
        self.Tabs.addTab(self.IncomeStatement, "")
        self.BalanceSheet = QtWidgets.QWidget()
        self.BalanceSheet.setObjectName("BalanceSheet")
        self.Tabs.addTab(self.BalanceSheet, "")
        self.CashFlow = QtWidgets.QWidget()
        self.CashFlow.setObjectName("CashFlow")
        self.Tabs.addTab(self.CashFlow, "")
        self.DisplayArea.addWidget(self.Tabs)
        self.DisplayArea.setStretch(0, 1)
        self.DisplayArea.setStretch(1, 4)
        self.horizontalLayout.addLayout(self.DisplayArea)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.gridLayout.addWidget(self.MainLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.MainWidget)

        self.retranslateUi(MainWindow)
        self.Tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # self.Stocks.setText( "Stocks")
        # self.Coins.setText("Coins")

        #----------------------------------------------------------------
        self.Switch.stateChanged.connect(self.check_box_state_changed)
        self.currencyBox.currentIndexChanged.connect(self.combo_box_index_changed)
        self.AddSymbolButton.clicked.connect(self.add_button_clicked)
        
        for stock in self.stocks:
            item = QtWidgets.QListWidgetItem(stock)
            self.SymbolList.addItem(item)

        self.SymbolList.itemClicked.connect(self.symbol_clicked)
        self.candlestick_graph = QWebEngineView(self.GraphArea)
        self.candlestick_graph.setParent(self.GraphArea)
   
    def check_box_state_changed(self):
        # Get the state of the checkbox and print it
        self.checked = self.Switch.isChecked()
        self.setMode()
    
    def setMode(self):
        if self.checked == True:
            self.mode = 'Crypto'
            self.Coins.setText('Crypto')
            self.Stocks.setText('     ')
        else:
            self.mode = 'Stocks'
            self.Coins.setText('     ')
            self.Stocks.setText('Stocks')
    
    def combo_box_index_changed(self):
        self.currency = self.currencyBox.currentText()
        print(self.currency)
    
    def add_button_clicked(self):
        
        searchsymbol = self.SearchBar.text()
        if searchsymbol in statuses.index:
            with open(r'New API\testing\stocks.txt', 'a') as f:
                f.write(searchsymbol + '\n')
                f.close()
            item = QtWidgets.QListWidgetItem(searchsymbol)
            name = statuses.loc[searchsymbol, 'name']
            self.SymbolList.addItem(item)

    def symbol_clicked(self):
        current = self.SymbolList.currentItem().text()
        self.current_symbol = current
        self.update_current_title(current)
        self.plot(current)
    
    def update_current_title(self,symbol):
        df = main.load_quote(symbol).astype(str)
        name = statuses.loc[symbol, 'name']
        exchange = statuses.loc[symbol, 'exchange']
        fullname = name+' | '+exchange
        self.SymbolTitle.setText(symbol)
        self.FullName.setText(fullname)
        self.CurrentPrice.setText(df['Price'][0])
        changetext = '{}({})'.format(df['Change'][0],df['Change Percent'][0])
        self.Change.setText(changetext)
        self.Vol.setText(df['Volume'][0])
        self.OpenPrice.setText(df['Open'][0])
        self.HighPrice.setText(df['High'][0])
        self.LowPrice.setText(df['Low'][0])
        self.PrevClosePrice.setText(df['Previous Close'][0])

    def plot(self,symbol):
        plot_obj = main.html_plot(symbol)
        self.candlestick_graph.setHtml(plot_obj)
        self.thismf.addWidget(self.candlestick_graph)




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.currencyBox.setItemText(0, _translate("MainWindow", "USD"))
        self.currencyBox.setItemText(1, _translate("MainWindow", "THB"))
        self.SymbolText.setText(_translate("MainWindow", "Symbols"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        self.AddSymbolButton.setText(_translate("MainWindow", "Add"))
        __sortingEnabled = self.SymbolList.isSortingEnabled()
        self.SymbolList.setSortingEnabled(False)
        self.SymbolList.setSortingEnabled(__sortingEnabled)
        
        self.OpenText.setText(_translate("MainWindow", "Open"))
        
        self.HighText.setText(_translate("MainWindow", "High"))
        
        self.LowText.setText(_translate("MainWindow", "Low"))
        
        self.PrevCloseText.setText(_translate("MainWindow", "Previous Close"))
        
        self.Tabs.setTabText(self.Tabs.indexOf(self.Price), _translate("MainWindow", "Price"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "New1"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.Tabs.setTabText(self.Tabs.indexOf(self.News), _translate("MainWindow", "News"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Spatial), _translate("MainWindow", "Spatial"))
        self.label_25.setText(_translate("MainWindow", "TextLabel"))
        self.label_24.setText(_translate("MainWindow", "TextLabel"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "TextLabel"))
        self.Desc.setText(_translate("MainWindow", "Desc"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Overview), _translate("MainWindow", "Overview"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.IncomeStatement), _translate("MainWindow", "Income Statement"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.BalanceSheet), _translate("MainWindow", "Balance Sheet"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.CashFlow), _translate("MainWindow", "Cash Flow"))
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(stockslist,None)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
