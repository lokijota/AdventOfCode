import time
from collections import deque, Counter
import sys
import numpy as np
import re
import copy
from tqdm import tqdm
import random
import matplotlib.pyplot as plt
import numpy as np
from itertools import pairwise

## read data

## global variables

with open('ch02/input.txt') as f:
    lines = f.read().splitlines()

data = []

# for line in lines:
    # data.append(line.split(" "))

## functions

## part 1

start_time = time.time()
result = 0

deltas = []

# pairwise is new in python 3.10 - https://docs.python.org/3.10/library/itertools.html?highlight=pairwise#itertools.pairwise
count = 0
for line in lines:
    row = [int(y)-int(x) for (x, y) in pairwise(line.split(" "))]

    if row[0] > 0:
        conditions = all(el>0 and el<=3 for el in row)
    elif row[0] < 0:
        conditions = all(el<0 and el>=-3 for el in row)
    else:
        continue

    if conditions == True:
        count += 1

    deltas.append(row)


result = count

print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

def count_infractions(deltas):
    inf = 0
    removal_candidates = set()

    for index, el in enumerate(deltas):
        if el<=0 or el>3:
            inf += 1
            removal_candidates.add(index)
            removal_candidates.add(index+1)

    return inf, removal_candidates

    # return sum(1 for el in data if el<=0 or el>3)

count = 0
for line in lines:
    row = [int(el) for el in line.split(" ")]
    row_pair_deltas = [int(y)-int(x) for (x, y) in pairwise(row)]

    # to make things simpler I can flip all the numbers if negative
    negative_count = sum(1 for el in row_pair_deltas if el<0)
    if negative_count>1:
        row = [-el for el in row]
        row_pair_deltas = [-el for el in row_pair_deltas]

    # ok so now all the sequences are increasing
    res, removal_candidates = count_infractions(row_pair_deltas)
    if res == 0:
        count += 1
        continue
        
    for rc in removal_candidates:
        removed_el = row[rc]
        row.pop(rc)

        row_pair_deltas = [int(y)-int(x) for (x, y) in pairwise(row)]
        res, _ = count_infractions(row_pair_deltas)

        # if we have one removal that removes the inconsistencies, we're fine
        if res == 0:
            count += 1
            break
        else:
            row.insert(rc, removed_el)
            # and continue checking

result = count

print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))