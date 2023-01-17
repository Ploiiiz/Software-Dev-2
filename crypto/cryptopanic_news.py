import requests
import header
import pandas as pd

# Your API key
api_key = header.apiKeys_cryptopanic

# Base URL for the API
base_url = "https://cryptopanic.com/api/v1/posts/"

# Parameters for the request
params = {"auth_token": api_key}

# Send the request to the API
response = requests.get(base_url, params=params)

# Check the status code of the response
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()
    # Convert JSON data to Pandas DataFrame
    # df = pd.read_json(data)
    print(data)
else:
    print("Error:", response.status_code)
