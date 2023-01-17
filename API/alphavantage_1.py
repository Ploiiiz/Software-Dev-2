import requests
import csv
import pandas
import unittest

api_key = "4JJ6E759L3IN858J"
url = "https://www.alphavantage.co/query"

class functionsTest(unittest.TestCase):

    def test_statusCode(self):
        request = getListingStatus()
        status_code = request.status_code
        assert status_code == 200

    def test_fileOut(self):
        filename = 'listing_status.csv'
        contentToCSV(getListingStatus(),filename)
        out = open(filename,'r')
        out.close()
        assert out != FileNotFoundError

    def test_entryCount(self):
        count_csv = 0
        with open('listing_status.csv','r') as m:
            for i in m:
                count_csv += 1
            count_csv -= 1
        count_df = makeDataFrame('listing_status.csv').shape[0]
        assert count_csv == count_df
    
    def test_checkContent_exist(self):
        response = getFullDailyData('IBM')
        decoded_content = response.content.decode('utf-8')
        err = "Error" in decoded_content
        assert err == False
    
    def test_checkContent_nonexist(self):
        response = getFullDailyData('HELLO')
        decoded_content = response.content.decode('utf-8')
        err = "Error" in decoded_content
        assert err == True
    
    def test_makeDataFrame(self):
        symbol = "IBM"
        filename = symbol + '.csv'
        response = getFullDailyData(symbol)
        contentToCSV(response,filename)
        dataFrame = makeDataFrame(filename)
        assert type(dataFrame) == pandas.core.frame.DataFrame
            
def getListingStatus():
    params = {
        "function"  :   "LISTING_STATUS",
        "apikey"    :   api_key
    }
    response = requests.request("GET",url,params=params)
    return response

def contentToCSV(response,filename):
    decoded_content = response.content.decode('utf-8')
    content = csv.reader(decoded_content.splitlines(), delimiter=',')
    content_list = list(content)
    with open(filename,'w') as m:
        for row in content_list:
            m.write(','.join(row))
            m.write('\n')

def makeDataFrame(filename):
    df = pandas.read_csv(filename)
    return df

def getFullDailyData(symbol):
    params = {
        "function"  :   "TIME_SERIES_DAILY_ADJUSTED",
        "symbol"    :   symbol,
        "apikey"    :   api_key,
        "datatype"  :   None,
        "outputsize":   "full"
    }
    response = requests.request("GET",url,params=params)
    return response

print(getFullDailyData('IBM').content)


# if __name__ == "__main__":
#     unittest.main()