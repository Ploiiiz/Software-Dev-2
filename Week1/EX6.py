panels = int(input())
tables = []
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
    print(count)