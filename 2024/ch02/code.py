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

print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))