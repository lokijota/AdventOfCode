import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

# from collections import deque, Counter
# import sys
# import numpy as np
# import re
# import copy
# from tqdm import tqdm
# import random
# import matplotlib.pyplot as plt
# import numpy as np

## read data

## global variables

with open('ch02/input.txt') as f:
    lines = f.read().split(',')

data = []
for line in lines:
    data.append([int(x) for x in line.split("-")])

# print(data)
## functions

## part 1

start_time = time.time()
result = 0

for id_range in data:

    for num in range(id_range[0], id_range[1] + 1):
        num_as_str = str(num)
        strlen = len(num_as_str)

        if strlen%2 == 1: # skip odd lengths
            continue

        strlen_floor2 = strlen // 2

        if num_as_str[:strlen_floor2] == num_as_str[strlen_floor2:]:
            result += num

print("Result part 1: ", result) # 23534117921
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# Auxilary dictionary with possible repetitions per string length
split_positions = {}
split_positions[2] = [[0,1]]
split_positions[3] = [[0,1,2]]
split_positions[4] = [[0,2], [0,1,2,3]]
split_positions[5] = [[0,1,2,3,4]]
split_positions[6] = [[0,3], [0,2,4], [0,1,2,3,4,5]]
split_positions[7] = [[0,1,2,3,4,5,6]]
split_positions[8] = [[0,4], [0,2,4,6], [0,1,2,3,4,5,6,7]]
split_positions[9] = [[0,3,6], [0,1,2,3,4,5,6,7,8]]
split_positions[10] = [[0,5], [0,2,4,6,8], [0,1,2,3,4,5,6,7,8,9]]

for id_range in data:

    for num in range(id_range[0], id_range[1] + 1): # for each range
        num_as_str = str(num)
        strlen = len(num_as_str)

        if strlen  == 1:
            continue

        for val_check in split_positions[strlen]: # eg if strlen = 4, then [[0,2], [0,1,2,3]]
            invalid = True
            first_val = num_as_str[val_check[0]:val_check[1]-val_check[0]] 

            for pos in val_check[1:]: # [0,1,2,3]
                next_val = num_as_str[pos:pos+val_check[1]-val_check[0]]
                if next_val != first_val:
                    invalid = False
                    break

            if invalid:
                result += num
                break # skip to next number and stop checking for other elements in val_checks

print("Result part 2: ", result) # 31755323497
print("--- %s seconds ---" % (time.time() - start_time))