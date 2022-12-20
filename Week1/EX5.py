# arr = input("Array members: ").split()
# arr = [int(i) for i in arr]
import unittest
class ThreeSumTestCase(unittest.TestCase):
    def test_1(self):
        result = ThreeSum([-3,0,3,1,2])
        assert result == [(-3,0,3), (-3,1,2)]
    def test_2(self):
        result = ThreeSum([1,1,2,4,5,2])
        assert result == []
    def test_3(self):
        result = ThreeSum([1,1,-2,4,5,0])
        assert result == [(-2,1,1)]
    def test_4(self):
        result = ThreeSum([])
        assert result == []
    

def ThreeSum(arr):
    ans = []
    arr.sort()
    for i, num in enumerate(arr):
        if i > 0 and num == arr[i-1]:
            continue
        l,r = i+1,len(arr)-1
        while l<r:
            tsum = num + arr[l] + arr[r]
            if tsum < 0:
                l += 1
            elif tsum > 0:
                r -= 1
            else:
                ans.append((num, arr[l], arr[r]))
                l += 1
                while arr[l] == arr[l-1]:
                    l += 1
    return ans

# print(ThreeSum(arr))
if __name__ == '__main__':
    ThreeSum()
    # unittest.main()