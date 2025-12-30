import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

from itertools import batched
# from itertools import groupby
# import numpy as np
# from collections import deque 
# import math
# from collections import Counter
# import sys
# import re
# import copy
# from tqdm import tqdm
# import random
# import matplotlib.pyplot as plt
# from matplotlib import path

## read data

## global variables

with open('ch03/input.txt') as f:
    lines = f.read().splitlines()

## functions


## part 1

start_time = time.time()
result = 0

x = 0
y = 0

visits = dict()
visits[(x,y)] = 1

for direction in lines[0]:
    if direction == '>':
        x += 1
    elif direction == '<':
        x -= 1
    elif direction == '^':
        y += 1
    elif direction == 'v':
        y -= 1

    visits[(x,y)] = visits.get((x,y), 0) + 1

result = len(visits.keys())
# result = len(list(filter(lambda elem: elem[1] > 1, visits.items())))

print("Result part 1: ", result) # 2592
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0


# Changed implementation to sets, as I had misinterpreted part 1 initially to be only houses that got more than 1 present
x_santa = 0
y_santa = 0
x_robot = 0
y_robot = 0

visits_set = set()
visits_set.add((0,0))

for command_santa, command_robot in batched(lines[0], 2, strict=True):

    if command_santa == '>':
        x_santa += 1
    elif command_santa == '<':
        x_santa -= 1
    elif command_santa == '^':
        y_santa += 1
    elif command_santa == 'v':
        y_santa -= 1

    visits_set.add((x_santa, y_santa))

    if command_robot == '>':
        x_robot += 1
    elif command_robot == '<':
        x_robot -= 1
    elif command_robot == '^':
        y_robot += 1
    elif command_robot == 'v':
        y_robot -= 1

    visits_set.add((x_robot, y_robot))

result = len(visits_set)

print("Result part 2: ", result)  # 2360
print("--- %s seconds ---" % (time.time() - start_time))
