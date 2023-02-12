import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import header
import sqlite3


# def data():
#     # Connect to the database
#     conn = sqlite3.connect("coinranking.db")

#     # Create a cursor
#     # cursor = conn.cursor()




#     # coindata
#     # Set the API key in the request header

   
#     headers = header.headers

#     # Make a request to the Coinranking API
#     url = "https://api.coinranking.com/v2/coins"
#     params = {"limit": 100,"timePeriod":"1h"}
#     response = requests.get(url, params=params, headers=headers)

#     # Check the status code of the response
#     if response.status_code != 200:
#         print("Error: Could not retrieve data from Coinranking API")
#         exit()

#     # Print the coin data
#     data = json.loads(response.text)

#     df = pd.DataFrame(data['data']['coins'])
    
#     print(df)

#     df.to_excel('coinranking.xlsx', sheet_name='dataCoin', index=True)

#     cryt = pd.read_excel('coinranking.xlsx')
#     # print(response.json())


#     # Save the DataFrame to a table in the database
#     cryt.to_sql("coinrankingdata", conn, if_exists="replace")

#     # Commit the changes to the database
#     conn.commit()

#     # Close the connection
#     conn.close()

  
# data()


class Data:
    def __init__(self):
        self.conn = sqlite3.connect("coinranking.db")

    def retrieve_data(self):
        headers = header.headers
        url = "https://api.coinranking.com/v2/coins"
        params = {"limit": 100,"timePeriod":"1h"}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            print("Error: Could not retrieve data from Coinranking API")
            exit()

        data = json.loads(response.text)

        df = pd.DataFrame(data['data']['coins'])
        # print(df)

        df.to_excel('coinranking.xlsx', sheet_name='dataCoin', index=True)

        cryt = pd.read_excel('coinranking.xlsx')

        cryt.to_sql("coinrankingdata", self.conn, if_exists="replace")

        self.conn.commit()

    def close_connection(self):
        self.conn.close()


data = Data()
data.retrieve_data()
data.close_connection()





