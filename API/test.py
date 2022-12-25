from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts = TimeSeries(key='7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
data['4. close'].plot()
plt.title('Intraday Times Series for the MSFT stock (1 min)')
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