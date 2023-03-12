import sqlite3
import pandas as pd
import datetime

conn = sqlite3.connect('testdb.db')
c = conn.cursor()
today = datetime.datetime.now().date

def connect_to_database():
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    return conn, c

def create_price_history_table(table_name):
    query = '''
CREATE TABLE IF NOT EXISTS {} (
    timestamp DATE PRIMARY KEY,
    open DECIMAL(10,3) NOT NULL,
    high DECIMAL(10,3) NOT NULL,
    low DECIMAL(10,3) NOT NULL,
    close DECIMAL(10,3) NOT NULL,
    adjusted_close DECIMAL(10,3) NOT NULL,
    volume INTEGER NOT NULL,
    dividend_amount DECIMAL(10,3)
);
'''.format(table_name)

    c.execute(query)
    conn.commit()
  

def store_data(dataframe, table_name):
    dataframe.to_sql(table_name, conn, if_exists='replace', index=True, index_label=dataframe.index.name)







def create_tech_table(symbol, tech, interval):
    table_name = symbol+'_'+tech+'_'+interval
    query = '''
CREATE TABLE IF NOT EXISTS {} (
    timestamp DATE PRIMARY KEY,
    {} DECIMAL(10,4) NOT NULL
);
'''.format(table_name,tech)
    c.execute(query)
    conn.commit()

def store_tech_table(dataframe, meta):
    symbol = meta[0]
    tech = meta[1]
    interval = meta[2]
    create_tech_table(symbol, tech, interval)

    table_name = symbol+'_'+tech+'_'+interval
    dataframe.to_sql(table_name, conn, if_exists='append', index=True)


def table_exists(table_name):
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = c.fetchone()
    return result is not None

def load_table(table_name):
    query = "SELECT * FROM {}".format(table_name)
    df = pd.read_sql_query(query, conn)
    return df

def hastofetch(table_name):
    query = "SELECT * FROM {} ORDER BY timestamp DESC LIMIT 1;".format(table_name)
    c.execute(query)
    latest = c.fetchone()
    if datetime.datetime.strptime(latest[0],'%Y-%m-%d %H:%M:%S').date() < today.date():
        return True
    return False