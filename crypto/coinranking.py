import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd

import sqlite3


def data():
    # Connect to the database
    conn = sqlite3.connect("coinranking.db")

    # Create a cursor
    # cursor = conn.cursor()




    # coindata
    # Set the API key in the request header
    headers = {"X-Coinranking-Key": "coinranking0578439e8d10089a1dc50684541a792aea4744f43bcd736e"}

    # Make a request to the Coinranking API
    url = "https://api.coinranking.com/v2/coins"
    params = {"limit": 100,"timePeriod":"1y"}
    response = requests.get(url, params=params, headers=headers)

    # Check the status code of the response
    if response.status_code != 200:
        print("Error: Could not retrieve data from Coinranking API")
        exit()

    # Print the coin data
    data = json.loads(response.text)

    df = pd.DataFrame(data['data']['coins'])
    
    # print(df)

    df.to_excel('coinranking.xlsx', sheet_name='dataCoin', index=True)

    cryt = pd.read_excel('coinranking.xlsx')
    # print(response.json())


    # Save the DataFrame to a table in the database
    cryt.to_sql("coinrankingdata", conn, if_exists="replace")

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()
data()





