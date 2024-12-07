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
import math

## read data

## global variables

with open('ch06/input.txt') as f:
    lines = f.read().splitlines()

## parse data

# convert list of strings into numpy array
map = []
for row in lines:
    map.append([letter for letter in row])

map = np.array(map,str) 

guard_row, guard_col = np.asarray(np.where(map == "^")).T[0]
map_size = map.shape[0]

# Q: would it make sense to use integers instead? would it speed up things later on?

## functions

## part 1

start_time = time.time()
result = 0

direction = "^"
while guard_row >= 0 and guard_row < map_size and guard_col >= 0 and guard_col < map_size:

    if direction == "^":
        map[guard_row, guard_col] = "0" # visited
        if guard_row > 0:
            if map[guard_row-1, guard_col] != "#":
                guard_row -= 1
            else:
                direction = ">"
        else:
            guard_row -= 1
    elif direction == ">":
        map[guard_row, guard_col] = "0" # visited
        if guard_col < map_size:
            if map[guard_row, guard_col+1] != "#":
                guard_col += 1
            else:
                direction = "v"
        else:
            guard_col += 1
    elif direction == "v":
        map[guard_row, guard_col] = "0" # visited
        if guard_row < map_size-1:
            if map[guard_row+1, guard_col] != "#":
                guard_row += 1
            else:
                direction = "<"
        else:
            guard_row += 1
    else: # if direction = "<"
        map[guard_row, guard_col] = "0" # visited
        if guard_col > 0:
            if map[guard_row, guard_col-1] != "#":
                guard_col -= 1
            else:
                direction = "^"
        else:
            guard_col -= 1


a, counts = np.unique(map, return_counts=True)
print(a, counts)

print(map)

print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0



print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))