from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import header_coinmarketcap

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

start = 1
limit = 5000 #limit 5000

parameters = {
  "start": start,
  "limit": limit,
  'convert':'USD'
}

headers = header_coinmarketcap.headers

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters,headers=headers)
 

  data = json.loads(response.text)
  df = pd.DataFrame(data['data'])
  
  print(df)
  df.to_excel('coinmarketcap.xlsx', sheet_name='Sheet1', index=True)
  
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


