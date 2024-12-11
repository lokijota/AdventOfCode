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
import itertools
import math
import operator

## read data

## global variables

with open('ch10/input.txt') as f:
    lines = f.read().splitlines()

## parse data

# convert list of strings into numpy array
map = []
for row in lines:
    map.append([letter for letter in row])

map = np.array(map,int)

## functions

## part 1

start_time = time.time()
result = 0

# paths = deque()
paths = set()

# find all the starting positions: 0's and put in the queue

# structure: current digit, where it is located, coords of where the path started
starting_points = [(0, *coords, *coords) for coords in list(zip(*np.where(map==0)))]
paths.update(starting_points)

dim = map.shape[0]

end_positions = set()

while paths:
    pos = paths.pop()

    if pos[0] == 9:
        end_positions.add(pos)
    else:
        # find surounding elements that have the value+1, for each of them add to the deque again
        surrounding_positions = [ (pos[1]-1, pos[2]), (pos[1]+1, pos[2]),(pos[1], pos[2]-1),(pos[1], pos[2]+1) ]
        surrounding_positions = [ el for el in surrounding_positions if el[0]>=0 and el[0]<dim and el[1]>=0 and el[1]<dim and map[el[0], el[1]] == pos[0]+1 ]

        [paths.add((pos[0]+1, el[0], el[1], pos[3], pos[4])) for el in surrounding_positions]

result = len(end_positions)
print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0


print("Result part 2: ", int(result)) #
print("--- %s seconds ---" % (time.time() - start_time))