import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

from itertools import groupby
import numpy as np
# from collections import deque, Counter
# import sys
# import re
# import copy
# from tqdm import tqdm
# import random
# import matplotlib.pyplot as plt
# import numpy as np

## read data

## global variables

with open('ch04/input.txt') as f:
    lines = f.read().splitlines()

data = lines

# print(data)
## functions

## part 1

start_time = time.time()
result = 0

nrows = len(data)
ncols = len(data[0])

counts = np.zeros(shape=(nrows+2, ncols+2), dtype=int)

# first, add
for row_idx in range(nrows):
    for col_idx in range(ncols):

        if data[row_idx][col_idx] == "@":
            # note the +1 at the end, as we created a count structure with +2 size in each dimmension, to avoid border checks
            # These are ignored down below
            uprow = row_idx-1+1
            downrow = row_idx+1+1
            leftcol = col_idx-1+1
            rightcol = col_idx+1+1

            counts[uprow][leftcol] += 1
            counts[uprow][col_idx+1] += 1
            counts[uprow][rightcol] += 1
            counts[row_idx+1][leftcol] += 1
            counts[row_idx+1][rightcol] += 1
            counts[downrow][leftcol] += 1
            counts[downrow][col_idx+1] += 1
            counts[downrow][rightcol] += 1

            # print("At ", row_idx, col_idx)
            # print(counts[1:-1,1:-1])
        else: 
            counts[row_idx+1][col_idx+1] = 50

            # print(counts)
# second, count (ignoring the borders)
result = (counts[1:-1,1:-1] < 4).sum() 

print("Result part 1: ", result) # 1495
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# print(counts[1:-1,1:-1])
rolls_removed = 0
itemindex = np.where(counts[1:-1,1:-1] < 4)

while len(itemindex[0]) > 0:

    for rollnb in range(len(itemindex[0])):
        row_idx = itemindex[0][rollnb]
        col_idx = itemindex[1][rollnb]

        # print("Removing at ", row_idx, col_idx)
        uprow = row_idx-1+1
        downrow = row_idx+1+1
        leftcol = col_idx-1+1
        rightcol = col_idx+1+1

        # print("Before removal on:", row_idx, col_idx)
        # print(counts)

        counts[uprow][leftcol] -= 1
        counts[uprow][col_idx+1] -= 1
        counts[uprow][rightcol] -= 1
        counts[row_idx+1][leftcol] -= 1
        counts[row_idx+1][col_idx+1] = 50  # mark as removed
        counts[row_idx+1][rightcol] -= 1
        counts[downrow][leftcol] -= 1
        counts[downrow][col_idx+1] -= 1
        counts[downrow][rightcol] -= 1

        # print("After removal:")
        # print(counts)
        
    rolls_removed += len(itemindex[0])
    itemindex = np.where(counts[1:-1,1:-1] < 4)

result = rolls_removed
print("Result part 2: ", result) # 8768
print("--- %s seconds ---" % (time.time() - start_time))