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
    pos = np.unravel_index(np.argmax(map == 0), map.shape)

    if pos == (0,0) and map[pos] != 0:
        return None

    return pos

def region_grow(map, visited_map, plant_type, region_start, region):

    if region_start in region:
        return 0,0

    region.add(region_start)
    visited_map[region_start] = 1

    # print(visited_map)

    # find the surrounding positions within map
    surrounding_positions = [(region_start[0]+x[0], region_start[1]+x[1]) for x in [(1,0), (-1,0), (0,-1), (0,1)]]
    # surrounding_positions = [pos for pos in surrounding_positions if pos>=(0,0) and pos<map.shape ]

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

## part 1

start_time = time.time()
result = 0

# using a replica of the map to mark what's visited or not
visited_map = np.zeros(map.shape, dtype=int)
tracking = []

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

print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0


print("Result part 2: ", int(result)) #
print("--- %s seconds ---" % (time.time() - start_time))