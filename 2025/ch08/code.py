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

## functions

def group_cleanup(distance_matrix, coords, circuit_nb):
    '''Delete all the inner connections for the same circuit -- no longer need to be considered'''
    '''So if here's a circuit with A-B and B-C, this function removes A-B, B-C and A-C if they're still there.'''
    '''This prunning severely reduces the size of the distance matrix, and massively improves perf of this approach'''
    '''Only using this for part 2, although it would also help in part 1 -- just didn't want to clone the distance matrix'''

    if circuit_nb == -1:
        return distance_matrix
    
    # print(f"Len before: {len(distance_matrix)}, ", end="")
    # reminder: coord["a,b,c"] -> [ [a, b, c], NN]
    for k1, v1 in coords.items():
        for k2, v2 in coords.items():
            if v1[1] == circuit_nb and v2[1] == circuit_nb:
                # delete from the matrix, it's pointless to check it again
                distance_matrix.pop(k1+"#"+k2, None)

    # print(f"after: {len(distance_matrix)}")

    return distance_matrix

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

circuit_count = 0
circuit_sizes = dict()

n = 1000

while n > 0:

    the_min = 1000000
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
        circuit_count += 1

        # remove from the distance matrix
        del distance_matrix[the_min_key] 

    # already in same group, ignore
    elif coords[p0key][1] == coords[p1key][1]:
        del distance_matrix[the_min_key] 

    # is any of the points in a group but the other isn't? if so, add to existing group
    elif (coords[p0key][1] == -1 or coords[p1key][1] == -1) and max_group > -1:
       coords[p0key][1] = max_group
       coords[p1key][1] = max_group
       # one of these assignments is redundant, I know

       circuit_sizes[max_group] += 1

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

if (circuit_count > 0):
    print(f"Larger circuits: {sorted(circuit_sizes.values(), reverse=True)[:3]}")

    ordered_circuit_sizes = sorted(circuit_sizes.values(), reverse=True)
    result = ordered_circuit_sizes[0] * ordered_circuit_sizes[1] * ordered_circuit_sizes[2]

print("Result part 1: ", result) # 163548
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

circuit_count = 0

# cleanup from part 1
for coords_val in coords.values():
    coords_val[1] = -1

unassigned_junction_boxes = len(lines)

while True:
    the_min = 1000000000
    the_min_key = ""
    
    # find closest points (ie, minimum distance)
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
        #print("New circuit",circuit_count , "Distance: ", the_min)
        coords[p0key][1] = circuit_count
        coords[p1key][1] = circuit_count
        circuit_count += 1
        unassigned_junction_boxes -= 2

        # remove from the distance matrix
        del distance_matrix[the_min_key] 

    # already in same group, ignore
    elif coords[p0key][1] == coords[p1key][1]:
        del distance_matrix[the_min_key] 

    # is any of the points in a group but the other isn't? if so, add to existing group
    elif (coords[p0key][1] == -1 or coords[p1key][1] == -1) and max_group > -1:

       #print("Expand circuit", max_group , "Distance: ", the_min)

       coords[p0key][1] = max_group
       coords[p1key][1] = max_group
       # one of these assignments is redundant, I know

       unassigned_junction_boxes -= 1

       # remove from the distance matrix
       del distance_matrix[the_min_key]

       distance_matrix = group_cleanup(distance_matrix, coords, max_group)

    # the points are in different groups... need to be joined together
    elif coords[p0key][1] > -1 and coords[p1key][1] > -1:
        #print("Join circuits ",p0key[1], "and", p1key[1], "Distance: ", the_min)

        # and now go over the group assignments and if = the 2nd assign the first
        oldgroup = coords[p1key][1]
        for k, v in coords.items():
            if v[1] == oldgroup:
                coords[k][1] = coords[p0key][1]
            
        del distance_matrix[the_min_key]

        distance_matrix = group_cleanup(distance_matrix, coords, coords[p0key][1])

    if unassigned_junction_boxes <= 10:
        result = int(p0key.split(",")[0])*int(p1key.split(",")[0]) 
        print("Unassigned:", unassigned_junction_boxes, "Last junction box joined: ", p0key, p1key, "->", result)
    
    if len(distance_matrix) == 0: # note: unassigned_junction_boxes == 0 doesn't work, stops one step before
        break
 
print("Result part 2: ", result)  #772452514 
print("--- %s seconds ---" % (time.time() - start_time))