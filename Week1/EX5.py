arr = input("Array members: ").split()

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
                ans.append([num, arr[l], arr[r]])
                l += 1
                while arr[l] == arr[l-1]:
                    l += 1
    return ans

print(ThreeSum(arr))