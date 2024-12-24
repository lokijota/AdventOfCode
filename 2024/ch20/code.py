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
# from operator import add, sub
# import networkx as nx

## read data

## global variables

with open('ch20/sample.txt') as f:
    lines = f.read().splitlines()

## parse data
grid = []
for row in lines:
    grid.append([letter for letter in row])

grid = np.array(grid)
edge_len = grid.shape[0]

start_pos = np.unravel_index(np.argmax(grid == "S"), grid.shape)
end_pos = np.unravel_index(np.argmax(grid == "E"), grid.shape)

## functions and classes

def find_path(start_pos, end_pos, path=[]):
    current_pos = start_pos

    while current_pos != end_pos:
        for surrounding in [(current_pos[0]+direction[0], current_pos[1]+direction[1]) for direction in [(0,1), (0,-1), (1,0), (-1, 0) ]]:
            if grid[surrounding] in [".", "E"] and surrounding not in path:
                path.append(surrounding)
                current_pos = surrounding
                break
    
    path.append(end_pos)

    return path

def find_cheats(pos, prev_path, future_path):
    cheats = []

    for surrounding in [(pos[0]+dir[0], pos[1]+dir[1], pos[0]+dir[2], pos[1]+dir[3] ) for dir in [(0,1,0,2), (0,-1, 0, -2), (1,0, 2, 0), (-1, 0, -2, 0) ]]:
        # second pair of numbers must be inside the map        
        if surrounding[2] < 0 or surrounding[3] < 0 or surrounding[2] >= grid.shape[0] or surrounding[3] >= grid.shape[1]:
            continue

        # first two numbers must have a "#""
        if grid[surrounding[:2]] != "#":
            continue

        # second pair of numbers must be a "." or "E" and not visited yet
        if grid[surrounding[2:]] in [".", "E"] and tuple(surrounding[2:]) not in prev_path:

            # it's not in the prev path, so it's the in the future path. let's find the position and calculate the distance
            res = [idx for idx, val in enumerate(future_path) if val == tuple(surrounding[2:])]

            path_len_with_cheat = len(prev_path) + len(future_path) - res[0] - 1
            cheats.append(tuple([*surrounding[:2], path_len_with_cheat])) 
    
    return cheats

def print_map(grid):
    for rows in grid:
        for val in rows:
            print(val, end="")
        print()


def region_grow(current_pos, past_path, future_path, max_radius, region):
    """ returns the positions """
    if grid[current_pos] == "." or max_radius == -1:
        print("  skipped", current_pos)
        return region

    if grid[current_pos] != "S":
        print("  added", current_pos)
        region.add(current_pos)

    # find the surrounding positions within map
    surrounding_positions = [(current_pos[0]+x[0], current_pos[1]+x[1]) for x in [(1,0), (-1,0), (0,-1), (0,1)]]

    # remove the ones already visited
    surrounding_positions = set(surrounding_positions)-region

    for surrounding_position in surrounding_positions:
        if surrounding_position[0] > 0 and surrounding_position[1] > 0 and \
            surrounding_position[0] < grid.shape[0]-1 and surrounding_position[1] < grid.shape[1]-1 and \
            grid[surrounding_position] == "#" and max_radius >= 0:

            print("region grow from", surrounding_position, "radius is", max_radius-1)
            rad = max_radius-1
            region_grow(surrounding_position, past_path, future_path, rad, region)
        else:
            print("not region growing from", surrounding_position, "radius is already", max_radius)


    return region

## part 1

start_time = time.time()
result = 0

# start by finding the path without cheating
path = find_path(start_pos, end_pos, [])
print(f"Size of path: {len(path)}")

# we can also jump from the start position
path.insert(0, start_pos)

# now test all the positions of the path and see if we can cheat
savings = dict()

for idx, pos in enumerate(path):
    cheats = find_cheats(pos, path[0:idx+1], path[idx:])

    for c in cheats:
        saving = len(path) - c[2] - 2
        if saving not in savings:
            savings[saving] = 0
        savings[saving] += 1

for k,v in savings.items():
    # print(f"{v} cheats saving {k} picoseconds")
    if k >= 100:
        result += v

# 1445 in 3.5 seconds
print("Result part 1: ", result) 
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

region = set()
region_grow(start_pos, path, [], 3, region)

print(len(region))
print_map(grid)
print()

for pos in region:
    grid[pos] = "X"


print_map(grid)
# print(region)

# cheats are a radius of manhattan distance? or only over walls? or... region grow on walls under manhattan distance?

# similar logic to above:
# do region growing starting on the current point, for "#" (and excluding edges)
# only grow if manhattan distance under the radius-1
# after having the region, check if it's in an edge and on the other side is the future path
# in this case, there's a possible jump here

print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))