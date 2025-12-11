import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

from itertools import groupby
import numpy as np
from collections import deque 
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

with open('ch05/input.txt') as f:
    lines = f.read().splitlines()

id_ranges = []
ingredient_ids = []

processing_ranges = True
for line in lines:
    if line == "":
        processing_ranges = False
        continue

    if processing_ranges:
        id_ranges.append([int(x) for x in line.split("-")])
    else: 
        ingredient_ids.append(int(line))

print(id_ranges)
print(ingredient_ids)

## functions

## part 1

start_time = time.time()
result = 0

for ingredient_id in ingredient_ids:
    for id_range in id_ranges:
        if ingredient_id >= id_range[0] and ingredient_id <= id_range[1]:
            result += 1
            break

print("Result part 1: ", result) # 664
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

id_ranges_merged = []

print(id_ranges)
id_ranges = sorted(id_ranges, key=lambda x: x[0])
print(id_ranges)

id_queue = deque(id_ranges)

while id_queue:
    current_range = id_queue.popleft()

    while id_queue:
        next_range = id_queue[0]
        if current_range[1] < next_range[0]:
            id_ranges_merged.append(current_range)
            break
        else:
            current_range[1] = max(current_range[1], next_range[1])
            id_queue.popleft()

    if not id_queue:
        id_ranges_merged.append(current_range)
    
result = sum([r[1] - r[0] + 1 for r in id_ranges_merged])

print("Result part 2: ", result)  # 350780324308385
print("--- %s seconds ---" % (time.time() - start_time))