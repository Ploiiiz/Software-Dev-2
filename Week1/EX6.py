from unittest.mock import patch
import unittest 
class addTenTest(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', '3', '2 4 6', '2 4 6', '2 4 6'])
    def test_1(self, input):
        result = addTen()
        assert result == [3]

    @patch('builtins.input', side_effect=['1', '3', '1 2 3', '4 5 6', '7 8 9'])
    def test_2(self, input):
        result = addTen()
        assert result == [0]

    @patch('builtins.input', side_effect=['2', '4', '1 2 3 4', '1 2 3 4', '1 2 3 4', '1 2 3 4'
                                        , '5', '2 2 2 2 2', '2 2 2 2 2', '2 2 2 2 2', '2 2 2 2 2', '2 2 2 2 2'])
    def test_3(self, input):
        result = addTen()
        assert result == [4,10]

    @patch('builtins.input', side_effect=['1', '3', '6 7 2', '8 5 9' , '5 3 9'])
    def test_4(self, input):
        result = addTen()
        assert result == [0]

def addTen():
    panels = int(input())
    tables = []
    countt = []
    for i in range(panels):
        tables.append([])
        size = int(input())
        for j in range(size):
            temp = input()
            tables[i].append(list(map(int,temp.split())))

    for table in tables:
        s = len(table)
        c = [[] for i in range(s)]
        for row in table:
            for e in range(s):
                c[e].append(row[e])
        table+=c

    for table in tables:
        count = 0
        for row in table:
            for i in range(len(row)):
                for j in range(2,len(row)+1):
                    if i+j <= len(row):
                        if sum(row[i:i+j]) == 10:
                            #print(row[i:i+j])
                            count += 1
        #print(count)
        countt.append(count)
    return countt

if __name__ == '__main__':
    # print(addTen())
    unittest.main()