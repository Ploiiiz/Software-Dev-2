arr = input("Members: ").split()

def checkDuplicates(arr):
    s = set(arr)
    if len(arr) == len(s): return True 
    else: return False

print(checkDuplicates(arr))