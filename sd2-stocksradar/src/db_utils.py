import sqlite3
import pandas as pd
import os

DATABASE_NAME = "data.db"
data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
database_file = os.path.join(data_folder, DATABASE_NAME)

def create_connection():
    """
    Creates a connection to the SQLite database.
    """
    try:
        conn = sqlite3.connect(database_file)
        return conn
    except sqlite3.Error as e:
        print(e)

def store_table(dataframe, table_name):
    if dataframe is not None:
        with create_connection() as conn:
            # print('Storing data in', table_name, 'table')
            if 'timestamp' not in dataframe and 'AssetType' not in dataframe:
                dataframe.to_sql(table_name, conn, if_exists='replace', index=True, index_label='date',chunksize=25)
            elif 'timestamp' in dataframe:
                dataframe.to_sql(table_name, conn, if_exists='append', index=True, index_label='timestamp',chunksize=25)
            elif 'AssetType' in dataframe:
                dataframe.to_sql(table_name, conn, if_exists='replace')
            elif 'Technology' in dataframe:
                dataframe.to_sql(table_name, conn, if_exists='replace')
            elif 'fiscalDateEnding' in dataframe:
                dataframe.to_sql(table_name, conn, if_exists='replace', index=True, index_label='fiscalDateEnding',chunksize=3)
            # print('Stored data in {}'.format(table_name))
    else:
        return 'Data is None'

def read_table(table_name):
    try:
        with create_connection() as conn:
            # print('Reading data from', table_name, 'table')
            query = 'SELECT * FROM "{}"'.format(table_name)
            df = pd.read_sql(query, conn)
            df = df.set_index(df.columns[0])
            if 'price' in table_name:
                df.index = pd.to_datetime(df.index)
            
            return df
    except Exception as e:
        # print(e)
        return '{} not found'.format(table_name)

def delete_table(table_name):
    try:
        with create_connection() as conn:
            # print('Deleting', table_name, 'table')
            c = conn.cursor()
            c.execute('DROP TABLE IF EXISTS "{}"'.format(table_name))
            print('Deleted {}'.format(table_name))
    except Exception as e:
        return e