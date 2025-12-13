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

with open('ch08/input.txt') as f:
    lines = f.read().splitlines()

coords = dict()
for line in lines:
    parts = line.split(",")
    coords[line] = [np.array([int(x) for x in parts]), -1 ]

# coords = [np.array([int(x[0]), int(x[1]), int(x[2])]) for x in [lin.split(",") for lin in lines]]

## functions

## part 1

start_time = time.time()
result = 0

distance_matrix = dict()

for k1, v1 in coords.items():
    for k2, v2 in coords.items():
        key = k1 + "#" + k2
        dist = np.linalg.norm(v1[0]-v2[0])  
        if dist != 0.0 and k2+"#"+k1 not in distance_matrix.keys():
           distance_matrix[key] = dist
    #i note: both c1-c2 and c2-c1 are in the keys... (the diagonals). they have to be removed in the code below

print(len(distance_matrix))
# print("min: ", min(distance_matrix.values()))

circuit_count = 0
circuit_sizes = dict()

n = 1000

while n > 0:

    the_min = 100000
    the_min_key = ""
    
    # find closest points
    for key, value in distance_matrix.items():
        if value < the_min:
            the_min = value
            the_min_key = key

    points = the_min_key.split("#")
    p0key = points[0]
    p1key = points[1]

    # if none of the points is in a group, create one
    max_group = max(coords[p0key][1],coords[p1key][1])
    if max_group == -1:
        coords[p0key][1] = circuit_count
        coords[p1key][1] = circuit_count
        circuit_sizes[circuit_count] = 2

        # print("Joined ", points[0] , "and", points[1], "in circuit", circuit_count)

        circuit_count += 1

        # remove from the distance matrix
        del distance_matrix[the_min_key] 

    # already in same group, ignore
    elif coords[p0key][1] == coords[p1key][1]:
        del distance_matrix[the_min_key] 

        # print(f"In same group, skipping: {coords[points[0]][1]}, distance is {the_min}")

    # is any of the points in a group but the other isn't? if so, add to existing group
    elif (coords[p0key][1] == -1 or coords[p1key][1] == -1) and max_group > -1:
    #    print(f" oo  {coords[points[0]][1]} - {coords[points[1]][1]}")

       coords[p0key][1] = max_group
       coords[p1key][1] = max_group
       # one of these assignments is redundant, I know

       circuit_sizes[max_group] += 1

    #    print(f"Added to existing group {max_group}")

       # remove from the distance matrix
       del distance_matrix[the_min_key] 
    
    # the points are in different groups... need to be joined together
    elif coords[p0key][1] > -1 and coords[p1key][1] > -1:

        # print(f"Merge groups {coords[points[0]][1] } and {coords[points[1]][1]} into group {coords[points[0]][1]}")

        circuit_sizes[coords[p0key][1]] += circuit_sizes[coords[p1key][1]]

        del circuit_sizes[coords[p1key][1]]
        # and now go over the group assignments and if = the 2nd assign the first

        oldgroup = coords[p1key][1]
        for k, v in coords.items():
            if v[1] == oldgroup:
                coords[k][1] = coords[p0key][1]
            
        del distance_matrix[the_min_key]

    n -= 1

# print(f"Circuit Count: {circuit_count}")
# print(f"Circuit Sizes: {circuit_sizes}")
print(f"Larger circuits: {sorted(circuit_sizes.values(), reverse=True)[:3]}")

ordered_circuit_sizes = sorted(circuit_sizes.values(), reverse=True)
result = ordered_circuit_sizes[0] * ordered_circuit_sizes[1] * ordered_circuit_sizes[2]

print("Result part 1: ", result) # 163548
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0



print("Result part 2: ", result)  # 
print("--- %s seconds ---" % (time.time() - start_time))