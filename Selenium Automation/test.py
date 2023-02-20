l = []
for i in range(10):
    a = input("ins: ")
    if a == '':
        break
    else:
        l.append(a)
for i in l:
    print(i.split()[0])

for i in l:
    print(' '.join(i.split()[1:]))