# import requests

# # Set the API endpoint URL
# url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

# # Set the API key
# api_key = "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0"

# # Set the query parameters
# params = {
#     "frequencyType": "daily",
#     "frequency": 1,
#     "startDate": "2022-01-01",
#     "endDate": "2022-01-31",
#     "symbol": "AAPL"
# }

# # Set the request headers
# headers = {
#     "X-RapidAPI-Key": api_key
# }

# # Make the API request
# response = requests.get(url, params=params, headers=headers)

# # Check the status code of the response
# if response.status_code == 200:
#     # If the request is successful, print the data
#     data = response.json()
#     print(data)
# else:
#     # If the request is unsuccessful, print the error message
#     print(response.text)


import requests

url = "https://yh-finance-complete.p.rapidapi.com/investp"

querystring = {"conversion":"eur-usd"}

headers = {
	"X-RapidAPI-Key": "7743c81996msh2ad1ff32ce0021ap1d042djsn21d3138a2fb0",
	"X-RapidAPI-Host": "yh-finance-complete.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)