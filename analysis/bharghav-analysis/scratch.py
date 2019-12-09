import null as null

lineCount = 0
outageCount =0
list1 = ['155.225.2' , '200.17.202']
listEdge = []
listCore = []
edgeCount = 0
coreCount = 0
totalLineCount = 0
with open('/Users/bharghavbaddam/PycharmProjects/CCN_Project/Traceroute_1-2/traceroute_1-2_2019-11-21_02-04-04.txt',
          "r") as f:
    for i, l in enumerate(f):
        pass
    lineCount = i+1
with open('/Users/bharghavbaddam/PycharmProjects/CCN_Project/Traceroute_1-2/traceroute_1-2_2019-11-21_02-04-04.txt',
          "r") as f:  # open the file for reading
    # read the file line by line

    starCount = 0
    tempCount = 0

    # print(lineCount)
    for line in f:  # use: for i, line in enumerate(f) if you need line numbers
        # try:
        #     line = line.decode("utf-8")  # try to decode the contents to utf-8
        # except ValueError:  # decoding failed, skip the line
        #     continue
        line = line.strip()
        line = line.lower()

        words = line.split("  ")

        if '*' in line or '* * *' in line:
            totalLineCount = totalLineCount + 1
        if list1[0] in line or list1[1] in line:
            if '*' in line:
                edgeCount = edgeCount+1

        if list1[0] not in line and list1[1] not in line:
             if '*' in line:
                 coreCount = coreCount+1

        tempCount = tempCount + 1
        if (tempCount == lineCount - 1):
            if '* * *' in line:
                edgeCount = edgeCount+1
                coreCount = coreCount -1

if(starCount > 0 and tempCount == lineCount):
    outageCount = outageCount + 1

for i in listEdge:
    for j in i:
        if '*' in j:
            edgeCount = edgeCount + 1

for i in listCore:
    for j in i:
        if '*' in j:
            coreCount = coreCount + 1

print(edgeCount)
print(coreCount)
print(totalLineCount)