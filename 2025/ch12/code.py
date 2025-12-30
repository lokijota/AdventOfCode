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
# from matplotlib import path

## read data

## global variables

with open('ch12/input.txt') as f:
    lines = f.read().splitlines()

reading_shapes = True

shapes = []
counts = []
boxes = []

for line in lines:

    if "x" in line:
        reading_shapes = False

    if reading_shapes:
        if ":" in line:
            shapes.append([])
            counts.append(0)
        elif len(line) == 0:
            continue
        else:
            shapes[-1].append(line)
            counts[-1] += line.count("#")
    else:
        parts = line.split(":")
        sizes = parts[0].split("x")
        boxes.append([(int(sizes[0]), int(sizes[1]))])

        part_counts = parts[1].split()
        [boxes[-1].append(int(item)) for item in part_counts]

## functions


## part 1

start_time = time.time()
result = 0

# print some statistics
fit_for_sure = 0
doesnt_fit_for_sure = 0

for box in boxes:
    rect_area = box[0][0] * box[0][1]
    part_area = 0

    three_multiple_box_area = box[0][0]//3*3 * box[0][1]//3*3
    part_count_area = sum(box[1:])*9
    
    for idx, part_count in enumerate(box[1:]):
        part_area += part_count * counts[idx]
    
    if rect_area-part_area<0:
        doesnt_fit_for_sure += 1

    print(f"Rectangle area: {rect_area}, Parts area={part_area}, diff = {rect_area-part_area}") 

    print(f"    3x3 part area= {part_count_area}, enclosing area 3x3= {three_multiple_box_area}, it fits for sure={part_count_area<= three_multiple_box_area}")
    if part_count_area<=three_multiple_box_area:
        fit_for_sure += 1


print(f"Total fits: {len(boxes)}, total fit for sure: {fit_for_sure}, total doesn't fit for sure: {doesnt_fit_for_sure}, to be analysed: {len(boxes)-fit_for_sure-doesnt_fit_for_sure}")

# the delta above = 0 on the full input data set, so no need to play tetris with this... (!) tricky. However in the sample, this doesn't work. Trickster!
result = fit_for_sure

print("Result part 1: ", result) #  587
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0



print("Result part 2: ", result)  # 
print("--- %s seconds ---" % (time.time() - start_time))
