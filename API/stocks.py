# Alpha Vantage



from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts = TimeSeries(key='7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='5min', outputsize='full')
data['4. close'].plot()
plt.title('Intraday Times Series for the MSFT stock (5 min)')
plt.show()

# import http.client

# conn = http.client.HTTPSConnection("alpha-vantage.p.rapidapi.com")

# headers = {
#     'X-RapidAPI-Key': "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0",
#     'X-RapidAPI-Host': "alpha-vantage.p.rapidapi.com"
#     }

# conn.request("GET", "/query?interval=5min&function=TIME_SERIES_INTRADAY&symbol=MSFT&datatype=json&output_size=compact", headers=headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

# import http.client

# conn = http.client.HTTPSConnection("alpha-vantage.p.rapidapi.com")

# headers = {
#     'X-RapidAPI-Key': "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0",
#     'X-RapidAPI-Host': "alpha-vantage.p.rapidapi.com"
#     }

# conn.request("GET", "/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&outputsize=compact&datatype=json", headers=headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

# import requests

# # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo'
# r = requests.get(url)
# data = r.json()

# print(data)



# import csv
# import requests

# # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# CSV_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey=demo'

# with requests.Session() as s:
#     download = s.get(CSV_URL)
#     decoded_content = download.content.decode('utf-8')
#     cr = csv.reader(decoded_content.splitlines(), delimiter=',')
#     my_list = list(cr)
#     for row in my_list:
#         print(row)