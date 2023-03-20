import requests
import json
import pandas as pd
import sqlite3
import header

def fiat():
    conn = sqlite3.connect("coinranking.db")
    headers = header.headers        
    url = "https://coinranking1.p.rapidapi.com/reference-currencies"
    querystring = {"limit":"50","offset":"0"}

    

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != 200:
                print("Error: Could not retrieve data from Coinranking API")
                exit()
    data = json.loads(response.text)
    new_data = pd.DataFrame(data['data']["currencies"])
    new_data.to_sql('fiat',conn, if_exists="replace")
    conn.commit()
    conn.close()


def searchfiat(symbol):
    fiat()
    conn = sqlite3.connect("coinranking.db")
    query = f'''
    SELECT uuid FROM fiat WHERE symbol = '{symbol}'
    '''
    data = pd.read_sql_query(query,conn)     
    data = data.loc[0, 'uuid']

    return data

# print(searchfiat('USD'))