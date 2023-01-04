from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/historical"

parameters = {
  "date": "2023-01-12",  # Retrieve data for January 1, 2022
  "convert": "USD"
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '986899e3-848a-4744-924c-3964570ccd76',
#   'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters,headers=headers)
 

  data = json.loads(response.text)
#   df = pd.DataFrame(data['data'])
  
#   print(df)
  print(data)
#   df.to_excel('cryptoago.xlsx', sheet_name='Sheet1', index=True)
  
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)