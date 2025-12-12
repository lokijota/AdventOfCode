import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

from itertools import groupby
import numpy as np
from collections import deque 
import math
# from collections import Counter
# import sys
# import re
# import copy
# from tqdm import tqdm
# import random

# import matplotlib.pyplot as plt
# import numpy as np
## read data

## global variables

with open('ch07/input.txt') as f:
    lines = f.read().splitlines()

diagram = np.array([list(line) for line in lines])
start_pos = lines[0].find("S")

## functions

## part 1

start_time = time.time()
result = 0

tachion_cols = set()
tachion_cols.add(start_pos)

row = 1
nsplits = 0

while row < len(lines):

    next_tachion_cols = set()

    for tachion_col in tachion_cols:
        # print(tachion_col)

        if diagram[row][tachion_col] == ".":
            next_tachion_cols.add(tachion_col)
        else:
            next_tachion_cols.add(tachion_col-1)
            next_tachion_cols.add(tachion_col+1)
            nsplits += 1

    tachion_cols = next_tachion_cols 
    row += 1

result = nsplits

print("Result part 1: ", result) # 1602
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

tachion_universe = dict()
tachion_universe[start_pos] = 1
row = 1

while row < len(lines):
    next_tachion_universe = dict()

    for tachion_col in tachion_universe.keys():
        # print(tachion_col)

        if diagram[row][tachion_col] == ".":
            if tachion_col not in next_tachion_universe.keys(): 
                next_tachion_universe[tachion_col] = tachion_universe[tachion_col]
            else:
                next_tachion_universe[tachion_col] += tachion_universe[tachion_col]
        else:

            if tachion_col-1 not in next_tachion_universe.keys():
                next_tachion_universe[tachion_col-1] = tachion_universe[tachion_col]
            else:
                next_tachion_universe[tachion_col-1] += tachion_universe[tachion_col]

            if tachion_col+1 not in next_tachion_universe.keys():
                next_tachion_universe[tachion_col+1] = tachion_universe[tachion_col]
            else:
                next_tachion_universe[tachion_col+1] += tachion_universe[tachion_col]


    tachion_universe = next_tachion_universe
    # print(tachion_universe)
    row += 1


for universes in tachion_universe.values():
    result += universes

print("Result part 2: ", result)  # 135656430050438
print("--- %s seconds ---" % (time.time() - start_time))