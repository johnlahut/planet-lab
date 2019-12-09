import os, re
import matplotlib.pylab as plt

keyword = '*'  # ask the user for keyword, use raw_input() on Python 2.x

root_dir = "/Users/bharghavbaddam/PycharmProjects/CCN_Project/Traceroute_6-8"  # path to the root directory to search
count = 0
dict1 = {}
dict3 = {}
generalCount =0
for root, dirs, files in os.walk(root_dir, onerror=None):  # walk the root dir
    for filename in files:  # iterate over the files in the current dir
        generalCount = generalCount+1
        file_path = os.path.join(root, filename)  # build the file path
        # print(file_path)
        try:
            with open(file_path, "r") as f:  # open the file for reading
                # read the file line by line
                hit_count_1_2 = 0
                for line in f:  # use: for i, line in enumerate(f) if you need line numbers
                    # try:
                    #     line = line.decode("utf-8")  # try to decode the contents to utf-8
                    # except ValueError:  # decoding failed, skip the line
                    #     continue
                    line = line.strip()
                    line = line.lower()
                    words = line.split(" ")

                    for word in words:
                        if word is '*':
                            hit_count_1_2 = hit_count_1_2+1
                    # for word in words:
                    #     if word is '*':
                    #         count = count+1
                    #         break
                    data1 = filename.split('_')
                    dict1[data1[2]] = hit_count_1_2
                    if (hit_count_1_2 > 0 ):
                        dict3[data1[2]] = hit_count_1_2
                    if keyword in line:
                        count = count + 1
                        break
                    # if keyword in line:  # if the keyword exists on the current line...
                    #     print(file_path)  # print the file path
                    #     break  # no need to iterate over the rest of the file
        except (IOError, OSError):  # ignore read and permission errors
            pass
print("The number of files 6-8 with * ", count)

root_dir_2 = "/Users/bharghavbaddam/PycharmProjects/CCN_Project/Traceroute_8-6"  # path to the root directory to search
count_2 = 0
dict2 = {}
dict4 = {}
generalCount2 = 0
for root, dirs, files in os.walk(root_dir_2, onerror=None):  # walk the root dir
    for filename2 in files:  # iterate over the files in the current dir
        generalCount2 = generalCount2 + 1
        file_path = os.path.join(root, filename2)  # build the file path
        # print(file_path)
        try:
            with open(file_path, "r") as f:  # open the file for reading
                # read the file line by line
                hit_count_2_1 = 0
                for line in f:  # use: for i, line in enumerate(f) if you need line numbers
                    # try:
                    #     line = line.decode("utf-8")  # try to decode the contents to utf-8
                    # except ValueError:  # decoding failed, skip the line
                    #     continue
                    line = line.strip()
                    line = line.lower()
                    words = line.split(" ")

                    for word in words:
                        if word is '*':
                            hit_count_2_1 = hit_count_2_1+1

                    # for word in words:
                    #     if word is '*':
                    #         count_2 = count_2 +1
                    #         break
                    data2 = filename2.split('_')
                    dict2[data2[2]] = hit_count_2_1
                    if (hit_count_2_1 > 0 ):
                        dict4[data2[2]] = hit_count_2_1
                    if keyword in line:
                        count_2 = count_2 + 1
                        break
                    # if keyword in line:  # if the keyword exists on the current line...
                    #     print(file_path)  # print the file path
                    #     break  # no need to iterate over the rest of the file
        except (IOError, OSError):  # ignore read and permission errors
            pass
print("The number of files 8-6 with * ", count_2)

totalCountFiles = generalCount+generalCount2
hitCountFiles = count+count_2

fraction = ((count+count_2)/totalCountFiles) *100
print("Total number of files ", totalCountFiles)
print("Fraction in 6-8 and 8-6 in ",fraction)

# lists1 = sorted(dict1.items()) # sorted by key, return a list of tuples
#
# x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples

# plt.plot(x1, y1)
# plt.xlabel("Dates")
# plt.ylabel("Number of packet drops")
# plt.title("B Nodes 1-2 Outages")
# plt.show()

# lists2 = sorted(dict2.items()) # sorted by key, return a list of tuples
#
# x2, y2 = zip(*lists2) # unpack a list of pairs into two tuples
#
# plt.plot(x2, y2)
# plt.xlabel("Dates")
# plt.ylabel("Number of packet drops")
# plt.title("B Nodes 2-1 Outages")
# plt.show()
#
# lists1 = sorted(dict3.items()) # sorted by key, return a list of tuples
#
# x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples
#
# plt.plot(x1, y1)
# plt.xlabel("Dates")
# plt.ylabel("Number of packet drops")
# plt.title("B Nodes 1-2 OutagesOnly")
# plt.show()

# lists2 = sorted(dict4.items()) # sorted by key, return a list of tuples
#
# x2, y2 = zip(*lists2) # unpack a list of pairs into two tuples
#
# plt.plot(x2, y2)
# plt.xlabel("Dates")
# plt.ylabel("Number of packet drops")
# plt.title("B Nodes 2-1 Outages Only")
# plt.show()