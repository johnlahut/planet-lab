import os, re

root_dir = "/Users/bharghavbaddam/PycharmProjects/CCN_Project/Traceroute_1-5"  # path to the root directory to search
number_of_files_1_2 = 0
for root, dirs, files in os.walk(root_dir, onerror=None):  # walk the root dir
    for filename in files:  # iterate over the files in the current dir
        number_of_files_1_2 = number_of_files_1_2 + 1
print("The number of files ", number_of_files_1_2)


root_dir = "/Users/bharghavbaddam/PycharmProjects/CCN_Project/Traceroute_5-1"  # path to the root directory to search
number_of_files_2_1 = 0
for root, dirs, files in os.walk(root_dir, onerror=None):  # walk the root dir
    for filename in files:  # iterate over the files in the current dir
        number_of_files_2_1 = number_of_files_2_1 + 1
print("The number of files ", number_of_files_2_1)