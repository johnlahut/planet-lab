import os, re
import matplotlib.pylab as plt

keyword = '* * *'  # ask the user for keyword, use raw_input() on Python 2.x

root_dir = "/Users/bharghavbaddam/PycharmProjects/CCN_Project/Traceroute_1-2"  # path to the root directory to search
dict1 = {}
dict3 = {}
outageCount = 0
list1 = ['155.225' , '200.17']
edgeCount = 0
coreCount = 0
totalLineCount = 0
longOutNew = 0
for root, dirs, files in os.walk(root_dir, onerror=None):  # walk the root dir
    for filename in files:  # iterate over the files in the current dir

        file_path = os.path.join(root, filename)  # build the file path
        # print(file_path)
        try:
            # with open(file_path, "r") as f:

            lineCount = 0

            starCount = 0
            tempCount = 0
            with open(file_path,"r") as f:
                for i, l in enumerate(f):
                    pass
                lineCount = i + 1

            with open(file_path,"r") as f:  # open the file for reading
                # read the file line by line


                for line in f:  # use: for i, line in enumerate(f) if you need line numbers
                    # try:
                    #     line = line.decode("utf-8")  # try to decode the contents to utf-8
                    # except ValueError:  # decoding failed, skip the line
                    #     continue
                    line = line.strip()
                    line = line.lower()
                    words = line.split("  ")

                    tempCount = tempCount + 1
                    for word in words:
                        if ('* * *' in word):
                            starCount = starCount + 1

                    if '*' in line or '* * *' in line:
                        totalLineCount = totalLineCount + 1

                    if(tempCount == lineCount):
                            if('* * *' not in words):
                                if (starCount > 0 ):
                                    outageCount = outageCount + 1

                    if list1[0] in line or list1[1] in line:
                        if '*' in line:
                            edgeCount = edgeCount + 1
                    if list1[0] not in line and list1[1] not in line:
                        if '*' in line:
                            coreCount = coreCount + 1
                    if (tempCount == lineCount - 1):
                        if '* * *' in line:
                            edgeCount = edgeCount + 1
                            coreCount = coreCount - 1

                    if(tempCount == lineCount):
                        if '* * *' in line:
                            longOutNew = longOutNew + 1




        except (IOError, OSError):  # ignore read and permission errors
            pass
root_dir = "/Users/bharghavbaddam/PycharmProjects/CCN_Project/Traceroute_2-1"  # path to the root directory to search
dict1 = {}
dict3 = {}
outageCount2 = 0
list1 = ['155.225' , '200.17']
edgeCount2 = 0
coreCount2 = 0
totalLineCount2 = 0
longOutNew2 = 0
for root, dirs, files in os.walk(root_dir, onerror=None):  # walk the root dir
    for filename in files:  # iterate over the files in the current dir

        file_path = os.path.join(root, filename)  # build the file path
        # print(file_path)
        try:
            # with open(file_path, "r") as f:

            lineCount2 = 0

            starCount2 = 0
            tempCount2 = 0
            with open(file_path,"r") as f:
                for i, l in enumerate(f):
                    pass
                lineCount2 = i + 1

            with open(file_path,"r") as f:  # open the file for reading
                # read the file line by line


                for line in f:  # use: for i, line in enumerate(f) if you need line numbers
                    # try:
                    #     line = line.decode("utf-8")  # try to decode the contents to utf-8
                    # except ValueError:  # decoding failed, skip the line
                    #     continue
                    line = line.strip()
                    line = line.lower()
                    words = line.split("  ")
                    tempCount2 = tempCount2 + 1
                    for word in words:
                        if ('* * *' in word):
                            starCount2 = starCount2 + 1

                    if '*' in line or '* * *' in line:
                        totalLineCount2 = totalLineCount2 + 1

                    if(tempCount2 == lineCount2):
                            if('* * *' not in words):
                                if (starCount2 > 0 ):
                                    outageCount2 = outageCount2 + 1

                    if list1[0] in line or list1[1] in line:
                        if '*' in line:
                            edgeCount2 = edgeCount2 + 1
                    if list1[0] not in line and list1[1] not in line:
                        if '*' in line:
                            coreCount2 = coreCount2 + 1
                    if (tempCount2 == lineCount2 - 1):
                        if '* * *' in line:
                            edgeCount2 = edgeCount2 + 1
                            coreCount2 = coreCount2 - 1

                    if (tempCount2 == lineCount2):
                        if '* * *' in line:
                            longOutNew2 = longOutNew2 + 1


        except (IOError, OSError):  # ignore read and permission errors
            pass
longCount =0
temp = 0
for i in range(outageCount):
    temp = temp +1
    if(temp%70 == 0):
        longCount = longCount+1

longCount2 =0
temp2 = 0
for i in range(outageCount2):
    temp2 = temp2 +1
    if(temp2%70 == 0):
        longCount2 = longCount2+1


edgePercent1to2 = (edgeCount/totalLineCount)*100
corePercent1to2 = (coreCount/totalLineCount)*100

edgePercent2to1 = (edgeCount2/totalLineCount2)*100
corePercent2to1 = (coreCount2/totalLineCount2)*100


print("Long Term Outage 1 to 2", longCount)
print("Long Term Outage 2 to 1", longCount2)

print("Outage Count 1 to 2",outageCount)
print("Outage Count 2 to 1",outageCount2)

print("Edge Percentage 1 to 2 ", edgePercent1to2)
print("Core Percentage 1 to 2", corePercent1to2)

print("Edge Percentage 2 to 1 ", edgePercent2to1)
print("Core Percentage 2 to 1", corePercent2to1)

print("Long Term Outage New Calculation on 1 to 2 ",longOutNew)
print("Long Term Outage New Calculation on 2 to 1 ",longOutNew2)