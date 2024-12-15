import copy
import itertools
import math
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import random
import re
import sys
import time
from collections import deque, Counter
from tqdm import tqdm

## read data

## global variables

with open('ch12/input.txt') as f:
    lines = f.read().splitlines()

## parse data

# convert list of strings into numpy array
map = []
for row in lines:
    map.append([letter for letter in row])

map = np.array(map)

# print(map)

## functions

def find_unvisited(map: np.array) -> tuple:
    """ Find an invisited position. Expects the visited position mask as parameter, not the map of plot of land itself """
    pos = np.unravel_index(np.argmax(map == 0), map.shape)

    if pos == (0,0) and map[pos] != 0:
        return None

    return pos

def region_grow(map, visited_map, plant_type, region_start, region):
    """ grow the region as per part 1 and count the area and fences along the way"""

    if region_start in region:
        return 0,0

    region.add(region_start)
    visited_map[region_start] = 1

    # print(visited_map)

    # find the surrounding positions within map
    surrounding_positions = [(region_start[0]+x[0], region_start[1]+x[1]) for x in [(1,0), (-1,0), (0,-1), (0,1)]]

    # remove the ones already visited
    surrounding_positions = set(surrounding_positions)-region

    fences = 0
    area = 1
    for surrounding_position in surrounding_positions:
        if surrounding_position[0] < 0 or surrounding_position[1] < 0 or surrounding_position[0]>=map.shape[0] or surrounding_position[1]>=map.shape[1]:
            fences += 1
        elif map[region_start] != map[surrounding_position]:
            fences += 1
        else:
            a,f = region_grow(map, visited_map, plant_type, surrounding_position, region)
            area += a
            fences += f

    return area, fences


def find_edges(region):
    """ Find all the possible single segment edges around a region """

    edges = []

    for pos in region:
        if (pos[0]+1, pos[1]) not in region:
            # if there's nothing below this square, add the respective bottom edge
            edges.append( (pos[0]+1, pos[1], pos[0]+1, pos[1]+1, "down" ))

        if (pos[0]-1, pos[1]) not in region:
            # if there's nothing above this square, add the respective top edge
            edges.append( (pos[0], pos[1], pos[0], pos[1]+1, "up" ))

        if (pos[0], pos[1]-1) not in region:
            # if there's nothing to the left of this square, add the respective left edge
            edges.append( (pos[0], pos[1], pos[0]+1, pos[1], "left" ))

        if (pos[0], pos[1]+1) not in region:
            # if there's nothing to the right of this square, add the respective right edge
            edges.append( (pos[0], pos[1]+1, pos[0]+1, pos[1]+1, "right" ))

    return edges

## part 1

start_time = time.time()
result = 0

# using a replica of the map to mark what's visited or not
visited_map = np.zeros(map.shape, dtype=int)
regions  = []

# 1. find unvisited starting point for a region
# walrus operator was new to me: https://stackoverflow.com/questions/50297704/what-are-assignment-expressions-using-the-walrus-or-operator-why-was-t
while (region_start := find_unvisited(visited_map)) != None:
    # print("Unvisited plot of land: ", region_start)

    # 2. region grow it
    region = set()

    size, fences = region_grow(map, visited_map, map[region_start], region_start, region)
    # print(map[region_start], size, fences)
    # print(visited_map)
    result += (size*fences)

    regions.append(region)

print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# leverages the regions list built in part 1
for region in regions:

    all_edges = find_edges(region)
    # print("All edges at start of processing: ", len(all_edges), ", region: ", region)

    sides_count = 0
    while len(all_edges) > 0:
        edge = all_edges.pop()

        if edge[0] == edge[2]: # horizontal edge
            extend_right = [x for x in all_edges if x[0] == edge[0] and x[1] == edge[3] and x[2] == edge[0] and x[3] > edge[3] and x[4] == edge[4]]
            extend_left  = [x for x in all_edges if x[0] == edge[0] and x[1] < edge[1] and x[2] == edge[0] and x[3] == edge[1] and x[4] == edge[4]]
            
            if len(extend_right) > 0:
                all_edges.remove(extend_right[0])
                all_edges.append((edge[0], edge[1], edge[2], extend_right[0][3], edge[4]))
            elif len(extend_left) > 0: # in all_edges:
                all_edges.remove(extend_left[0])
                all_edges.append((edge[0], extend_left[0][1], edge[2], edge[3], edge[4]))
            else:
                # can't extend either way so we found a full side
                sides_count += 1
                # print(" - Removing completed side: ", edge)
        else:
            # vertical edge, edge[1] == edge[3]
            extend_down = [x for x in all_edges if x[0] == edge[2] and x[1] == edge[1] and x[2] > edge[2] and x[3] == edge[3] and x[4] == edge[4]]
            extend_up =   [x for x in all_edges if x[0] < edge[0] and x[1] == edge[1] and x[2] == edge[0] and x[3] == edge[3] and x[4] == edge[4]]

            if len(extend_down) > 0: # in all_edges:
                all_edges.remove(extend_down[0])
                all_edges.append((edge[0], edge[1], extend_down[0][2], edge[3], edge[4]))
            elif len(extend_up) > 0: # in all_edges:
                all_edges.remove(extend_up[0])
                all_edges.append((extend_up[0][0], edge[1], edge[2], edge[3], edge[4]))
            else:
                # can't extend either way so we found a full side
                sides_count += 1
                # print(" - Removing completed side: ", edge)
    
    result += len(region)*sides_count
    print("Sides: ", sides_count, "Result: ", result)

# 858684

print("Result part 2: ", int(result)) #
print("--- %s seconds ---" % (time.time() - start_time))