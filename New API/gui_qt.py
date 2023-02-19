import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

width = 2600
height = 1400

styleSheet = '''
*{
    font-size: 16px;
    background-color: transparent;
}
QMainWindow {
    background-color: #001F2D;
    }
QLabel {
    color: white;
    }   
QPushButton, QComboBox {
    border: none;
    }
QTabWidget::tab-bar {
    left: 0;
    top: 20;
    background-color: transparent;
}
QTabWidget::pane {
    left: 0;
    background-color: transparent;
}
QTabWidget{
    background-color: transparent;
}

QTabBar::tab {
    font-size: 25pt;
    font-weight: bold;
    color: rgba(255,255,255,0.4);
    background-color: transparent;
    }

QScrollBar {
    width: 6px;
}

QScrollBar::handle:vertical {
    background: rgb(22,58,87);
    border-radius: 3px;
}

QListWidget{
    border: none;
}

QListWidget::item:selected{
    background-color: rgb(22,58,88);
}

}
'''

class StockViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(styleSheet)
        # Create the main splitter
        splitter = QSplitter()
        self.setGeometry(0,0,width,height)
        # Create the first part (stock/crypto symbols)
        symbols_widget = QWidget()
        symbols_widget.setStyleSheet('''
        QWidget{
            background-color: #002234;
        }
        ''')
        symbols_layout = QVBoxLayout()
        symbols_widget.setLayout(symbols_layout)

        # switch_label = QLabel("Switch:")
        # currency_label = QLabel("Currency:")
        switches_layout = QHBoxLayout()
        switch_stock = QLabel("$")
        switch_toggler = QPushButton("<->")
        switch_coin = QLabel("C")
        currencies = QComboBox()
        currencies.addItem("USD")
        currencies.addItem("THB")
        switches_layout.addWidget(switch_stock)
        switches_layout.addWidget(switch_toggler)
        switches_layout.addWidget(switch_coin)
        switches_layout.addWidget(currencies)
        
        #Symbol Header and +
        symbol_name_layout = QHBoxLayout()
        symbol_label_head = QLabel("Symbols")
        symbol_label_head.setStyleSheet("font-size: 40pt; font-weight: bold")
        plus_button = QPushButton("+")
        plus_button.setStyleSheet("font-size: 40pt")
        symbol_name_layout.addWidget(symbol_label_head)
        symbol_name_layout.addWidget(plus_button)
        
        search_edit = QLineEdit()
        search_edit.setStyleSheet('''background: rgb(6,24,37);
        border: 1px solid rgb(6,24,37);
        border-radius: 12px;
        padding: 4px 30px;''')

        main_list = QListWidget()
        stocks = ['AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT']

        # Add each stock to the list widget
        for stock in stocks:
            # Create a custom widget for the stock symbol with a sub-layout
            widgetitem = QWidget()
            layout = QHBoxLayout()
            widgetitem.setLayout(layout)

            first_column_layout = QVBoxLayout()

            first_column_layout.addWidget(QLabel(stock))
            first_column_layout.addWidget(QLabel(stock+"stock"))

            # Create the second column with 3 rows
            second_column_layout = QVBoxLayout()
            second_column_layout.addWidget(QLabel("131.13"))
            second_column_layout.addWidget(QLabel("+13% (0.13)"))
            second_column_layout.addWidget(QLabel("131.31T"))

            # Add the two columns to the main layout
            layout.addLayout(first_column_layout)
            layout.addLayout(second_column_layout)

            
            item = QListWidgetItem()
            item.setSizeHint(QSize(1,77))
            main_list.addItem(item)
            main_list.setItemWidget(item,widgetitem)



        symbols_layout.addLayout(switches_layout)
        symbols_layout.addLayout(symbol_name_layout)
        symbols_layout.addWidget(search_edit)
        symbols_layout.addWidget(main_list)

        # Create the second part (stock information)
        stock_widget = QWidget()
        stock_layout = QVBoxLayout()
        stock_widget.setLayout(stock_layout)

        info_layout = QHBoxLayout()
        symbol_label = QLabel("AAPL")
        name_label = QLabel("Apple Inc.")
        market_label = QLabel("NASDAQ")
        price_label = QLabel("$127.14")
        change_label = QLabel("+0.28%")
        marketcap_label = QLabel("$2.12T")

        info_layout.addWidget(symbol_label)
        info_layout.addWidget(name_label)
        info_layout.addWidget(market_label)
        info_layout.addStretch(1)
        info_layout.addWidget(price_label)
        info_layout.addWidget(change_label)
        info_layout.addWidget(marketcap_label)

        tab_widget = QTabWidget()
        tab_widget.setStyleSheet('''
        QTabBar::tab:selected {
        color: #75FBFD;
        text-decoration: underline;
    }
        ''')
        graph_widget = QWidget()
        graph_widget.setStyleSheet("background-color: #001F2D")
        news_widget = QWidget()
        news_widget.setStyleSheet("background-color: #001F2D")
        company_widget = QWidget()
        company_widget.setStyleSheet("background-color: #001F2D")

        graph_layout = QVBoxLayout()
        graph_widget.setLayout(graph_layout)

        news_layout = QVBoxLayout()
        news_widget.setLayout(news_layout)

        company_layout = QVBoxLayout()
        company_widget.setLayout(company_layout)

        tab_widget.addTab(graph_widget, "Graph")
        tab_widget.addTab(news_widget, "News")
        tab_widget.addTab(company_widget, "Company Information")

        stock_layout.addLayout(info_layout)
        stock_layout.addWidget(tab_widget)

        # Add the two parts to the splitter
        splitter.addWidget(symbols_widget)
        splitter.addWidget(stock_widget)
        splitter.setSizes([int(0.28*width),int(0.72*width)])

        # Set the splitter as the central widget of the main window
        self.setCentralWidget(splitter)
        self.setWindowTitle("Stock Viewer")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = StockViewer()
    viewer.show()
    sys.exit(app.exec())
