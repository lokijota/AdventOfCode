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

with open('ch20/input.txt') as f:
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
    """ Find possble cheats for part 1 """

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

# move to helper
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_map(grid, path=[]):
    for idx_row, rows in enumerate(grid):
        for idx_col, val in enumerate(rows):
            if (idx_row, idx_col) in path:
                print(f"{bcolors.OKGREEN}O{bcolors.ENDC}", end="")
            else:
                print(val, end="")
        print()


def region_grow(current_pos, past_path, future_path, max_radius, region):
    """ returns the region surrounding the current pos composed of #/walls """
    # if grid[current_pos] == ".":
    #     return 

    if grid[current_pos] in ["#", "E"]: # != "S":
        region.add(current_pos)

    # find the surrounding positions within map
    surrounding_positions = [(current_pos[0]+x[0], current_pos[1]+x[1]) for x in [(1,0), (-1,0), (0,-1), (0,1)]]

    for surrounding_position in surrounding_positions:
        if surrounding_position[0] > 0 and surrounding_position[1] > 0 and \
            surrounding_position[0] < grid.shape[0]-1 and surrounding_position[1] < grid.shape[1]-1 and \
            grid[surrounding_position] == "#" and max_radius > 0:

            region_grow(surrounding_position, past_path, future_path, max_radius-1, region)

    return

def region_grow_by_distance(pos, distance):
    """ used for part 2, does region grow to select all the positions inside a losange defined with manhattan distance (20 as per problem statement) """

    region = set()
    # region.add(pos) # un-needed - jota: remove it's from old code

    for manhattan in range(1,distance+1):
        for row in range(pos[0]-manhattan, pos[0]+manhattan+1):

            if row < 1 or row >= grid.shape[0]-1:
                continue

            lower_limit = pos[1]
            upper_limit = pos[1]

            if row <= pos[0]:
                lower_limit += - (pos[0]-row) + manhattan
                upper_limit += + (pos[0]-row) - manhattan
                # lower_limit += pos[1] - (pos[0]-row) + manhattan
                # upper_limit += pos[1] + (pos[0]-row) - manhattan
            else:
                lower_limit += - (row-pos[0]) + manhattan 
                upper_limit += (row-pos[0]) - manhattan

            for col in [lower_limit, upper_limit]:
                if col > 0 and col < grid.shape[1]-1: #row>0 and row<grid.shape[0]-1 and 
                    region.add((row,col))
 
    return region

def find_cheats_pt2(pos, prev_path, future_path):
    """ Find possble cheats for part 2 """

    region = region_grow_by_distance(pos, 20)
    lenpp = len(prev_path)
    lenfp = len(future_path)

    # find cheats from any of the possible starting points in the above region
    cheats = []

    for region_pos in region:
        if grid[region_pos] in [".", "E"] and region_pos not in prev_path:
            
            # look for the index of the current position in the future path
            pos_in_future_path = [idx for idx, val in enumerate(future_path) if val == region_pos]

            manhattan_distance_to_pos = abs(pos[0]-region_pos[0]) + abs(pos[1]-region_pos[1])

            path_len_with_cheat = lenpp + lenfp - pos_in_future_path[0] - 1 + manhattan_distance_to_pos
            cheats.append((region_pos[0], region_pos[1], path_len_with_cheat)) 

    return cheats

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

# now test all the positions of the path and see if we can cheat
savings = dict()

for idx, pos in enumerate(path):
    cheats = find_cheats_pt2(pos, path[0:idx+1], path[idx:])
    print("At step", idx, "of pass, there are # cheats:", len(cheats))

    for c in cheats:
        saving = len(path) - c[2]
        if saving >= 100:
            result += 1
        # if saving not in savings:
        #     savings[saving] = 0
        # savings[saving] += 1

# for k,v in savings.items():
#     if k >= 100:
#         result += v

# 1008040 in 569 seconds
print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))