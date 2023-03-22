import data, db_utils, utils
import os
import unittest
import pandas as pd
from unittest.mock import patch, mock_open

class TestCheckAvailable(unittest.TestCase):

    def test_check_us_stock(self):
        result = data.check_available('AAPL')
        self.assertEqual(result, 'AAPL')
    
    def test_check_th_stock(self):
        result = data.check_available('PTT')
        self.assertEqual(result, 'PTT.BK')

    def test_check_none_stock(self):
        result = data.check_available('-')
        self.assertEqual(result, None)

    def test_txt_to_list(self):
        # Define test data
        path = '/test/path'
        filename = 'test_file.txt'
        file_contents = 'line1\nline2\nline3\n'
        
        # Set up mock file object
        with patch('builtins.open', mock_open(read_data=file_contents)) as mock_file:
            # Call the function
            result = data.txt_to_list(path, filename)
            
            # Assert the expected behavior
            mock_file.assert_called_once_with(os.path.join(path, filename), 'r')
            assert result == ['line1', 'line2', 'line3']
    
    @patch('db_utils.read_table')
    def test_read_all(self, mock_read):
        my_table_data = 'foo'

        # Configure mock read_table to return the test data
        mock_read.return_value = my_table_data

        # Call the function that uses read_table
        result = data.read_all('test')

        # Assert that the function behaves correctly
        self.assertEqual(result,['foo','foo','foo','foo'])

    def test_daybreak(self):
        # Define test data
        dates = pd.to_datetime(['2022-01-01', '2022-01-03'])
        data = {'col1': [1, 2], 'col2': [3, 4]}
        dfd = pd.DataFrame(data=data, index=dates)

        # Call the function with the test data
        daybreaks = utils.daybreak(dfd)

        # Assert the expected behavior
        expected_daybreaks = [pd.Timestamp('2022-01-02')]
        assert daybreaks == expected_daybreaks
    
    def test_hourbreak(self):
        hours = pd.to_datetime(['2022-01-01 12:00:00', '2022-01-01 14:00:00'])
        data = {'col1': [1, 2], 'col2': [3, 4]}
        dfd = pd.DataFrame(data=data, index=hours)

        hourbreaks = utils.hourbreak(dfd)

        expected_hourbreaks = [pd.Timestamp('2022-01-01 13:00:00')]
        assert hourbreaks == expected_hourbreaks

    

if __name__ == '__main__':
    unittest.main()