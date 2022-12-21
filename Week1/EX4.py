#arr = input("Members: ").split()

import unittest
class DuplicateTest(unittest.TestCase):
    def test_1(self):
        result = checkDuplicates([-1,1,3,5,0])
        assert result == False
    def test_2(self):
        result = checkDuplicates([0,0,1,5,3,-2])
        assert result == [0]
    def test_3(self):
        result = checkDuplicates([-1,2,5,-2,-1,2])
        assert result == [-1,2]
    def test_0(self):
        result = checkDuplicates([])
        assert result == False


def checkDuplicates(arr):
    a = sorted(arr)
    dupe = []
    for i in range(1,len(a)):
        if a[i] == a[i-1] and a[i] not in dupe:
            dupe.append(a[i])
    if dupe != []:
        return dupe 
    else: return False

# print(checkDuplicates(arr))
if __name__ == "__main__":
    # print(checkDuplicates([-1,1,3,5,0]))
    unittest.main()