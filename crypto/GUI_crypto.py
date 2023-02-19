import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
import coinranking
import coinrankcandle as cd



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

class CryptoViewer(QMainWindow):
    def __init__(self):        
        super().__init__()
        self.candle_widget = QWebEngineView(self)
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
        switch_crypto = QLabel("$")
        switch_toggler = QPushButton("<->")
        switch_coin = QLabel("C")
        currencies = QComboBox()
        currencies.addItem("USD")
        currencies.addItem("THB")
        switches_layout.addWidget(switch_crypto)
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
        padding: 4px 30px;
        color: rgb(255,255,255)''')

        
        main_list = QListWidget()

        data = coinranking.Data()
        data.retrieve_data()
        crypto_sym = data.get_list_symbol()
        crypto_name = data.get_list_name()
        crypto_price = data.get_list_price()
        crypto_change = data.get_list_change()
        crypto_change_color = data.get_list_change_color()
        crypto_marketcap = data.get_list_marketcap()
        crypto_uuid = data.get_list_uuid()
        crypto = list(zip(crypto_sym,crypto_name,crypto_price,crypto_change,crypto_change_color,crypto_marketcap,crypto_uuid))
        # print(crypto)
        data.close_connection()
        

        # Add each stock to the list widget
        for crypto in crypto:
            # Create a custom widget for the stock symbol with a sub-layout
            widgetitem = QWidget()
            layout = QHBoxLayout()
            widgetitem.setLayout(layout)

            # Add a bottom border to the layout
            

            first_column_layout = QVBoxLayout()

            #symbol
            symbol_label = QLabel(crypto[0])
            symbol_label.setStyleSheet("font-size: 18pt; font-weight: bold; border-bottom: None;")
            first_column_layout.addWidget(symbol_label)
            
            #name
            name_label = QLabel(crypto[1])
            name_label.setStyleSheet("border-bottom: None;")
            first_column_layout.addWidget(name_label) 

            # Create the second column with 3 rows
            second_column_layout = QVBoxLayout()

            #price
            price_label = QLabel("$"+crypto[2])
            price_label.setStyleSheet("border-bottom: None;")
            price_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            second_column_layout.addWidget(price_label)
            

            #change
            change_label = QLabel(crypto[3])
            change_label.setStyleSheet("color: " + str(crypto[4]) + "; border-bottom: None;")
            change_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            # change_label.setContentsMargins(0,5,0,5)
            second_column_layout.addWidget(change_label) 


            #marketCap
            marketCap_label = QLabel("$"+crypto[5])
            marketCap_label.setStyleSheet("border-bottom: None;")
            marketCap_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            second_column_layout.addWidget(marketCap_label)
            
            

            second_column_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            second_column_layout.setContentsMargins(0,0,20,0)
            second_column_layout.setSpacing(2)

            # # Add a button to the coin widget
            # button = QPushButton(widgetitem)
            # button.setProperty("crypto", crypto[0])
            # # cr = cd.CoinRankingOHLC(crypto[6], "minute",crypto[0],crypto[1])
            # # button.clicked.connect(cr)
            # layout.addWidget(button)
                    
            


            # Add the two columns to the main layout
            layout.addLayout(first_column_layout)
            layout.addLayout(second_column_layout)

            

            
            item = QListWidgetItem()
            item.setSizeHint(QSize(1,77))
                 
            main_list.addItem(item)
            main_list.setItemWidget(item,widgetitem)
            main_list.setStyleSheet("border-bottom: 2px solid #123c4c; ")  



        symbols_layout.addLayout(switches_layout)
        symbols_layout.addLayout(symbol_name_layout)
        symbols_layout.addWidget(search_edit)
        symbols_layout.addWidget(main_list)
        


        # Create the second part (stock information)
        crypto_widget = QWidget()
        crypto_layout = QVBoxLayout()        
        crypto_widget.setLayout(crypto_layout)

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

        # Display the plot in the figure widget
        cr = cd.CoinRankingOHLC("Qwsogvtv82FCd", "minute","BTC","Bitcoin")
        self.candle_widget.setHtml(cr.show_candlestick())

        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.candle_widget)
        
        graph_widget.setLayout(graph_layout)

        
        


        news_layout = QVBoxLayout()
        news_widget.setLayout(news_layout)

        company_layout = QVBoxLayout()
        company_widget.setLayout(company_layout)

        tab_widget.addTab(graph_widget, "Graph")
        tab_widget.addTab(news_widget, "News")
        tab_widget.addTab(company_widget, "Company Information")

        crypto_layout.addLayout(info_layout)
        crypto_layout.addWidget(tab_widget)

        # Add the two parts to the splitter
        splitter.addWidget(symbols_widget)
        splitter.addWidget(crypto_widget)
        splitter.setSizes([int(0.28*width),int(0.72*width)])

        # Set the splitter as the central widget of the main window
        self.setCentralWidget(splitter)
        self.setWindowTitle("Crypto Viewer")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CryptoViewer()
    viewer.show()
    sys.exit(app.exec())
