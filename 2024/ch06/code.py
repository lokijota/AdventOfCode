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
from itertools import pairwise
import math

## read data

## global variables

with open('ch06/input.txt') as f:
    lines = f.read().splitlines()

## parse data

# convert list of strings into numpy array
map = []
for row in lines:
    map.append([letter for letter in row])

map = np.array(map,str) 

guard_row, guard_col = np.asarray(np.where(map == "^")).T[0]
initial_guard_row, initial_guard_col = guard_row, guard_col

map_size = map.shape[0]

# Q: would it make sense to use integers instead? would it speed up things later on?

## functions

def print_map():
    """Convenience, for debug only"""
    print("-----------")
    for row in map:
        for col in row:
            print(col, end="")
        print()


def is_it_loop(guard_row, guard_col):
    """Returns 1 if it finds a loop, returns 0 otherwise"""
    """Code is very similar to code of part 1, but with some subtle differences specific for part 2... so yeah, duplicated"""
    """Note to track that it's a repeated path we need to include the direction in the path, unlike in the implementation in part 1"""

    the_path = set()
    direction = "^"

    while guard_row >= 0 and guard_row < map_size and guard_col >= 0 and guard_col < map_size:

        if direction == "^":
            # uncomment for visualization map[guard_row, guard_col] = "0" # visited
            if guard_row > 0:
                if map[guard_row-1, guard_col] != "#":
                    guard_row -= 1
                    if (guard_row, guard_col, direction) in the_path:
                        return 1
                    
                    the_path.add((guard_row, guard_col, direction))
                else:
                    direction = ">"
            else:
                guard_row -= 1
        elif direction == ">":
            # uncomment for visualization map[guard_row, guard_col] = "0" # visited
            if guard_col < map_size-1:
                if map[guard_row, guard_col+1] != "#":
                    guard_col += 1
                    if (guard_row, guard_col, direction) in the_path:
                        return 1
                    
                    the_path.add((guard_row, guard_col, direction))
                else:
                    direction = "v"
            else:
                guard_col += 1
        elif direction == "v":
            # uncomment for visualization map[guard_row, guard_col] = "0" # visited
            if guard_row < map_size-1:
                if map[guard_row+1, guard_col] != "#":
                    guard_row += 1
                    if (guard_row, guard_col, direction) in the_path:
                        return 1
                    
                    the_path.add((guard_row, guard_col, direction))
                else:
                    direction = "<"
            else:
                guard_row += 1
        else: # if direction = "<"
            # uncomment for visualization map[guard_row, guard_col] = "0" # visited
            if guard_col > 0:
                if map[guard_row, guard_col-1] != "#":
                    guard_col -= 1
                    if (guard_row, guard_col, direction) in the_path:
                        return 1
                    
                    the_path.add((guard_row, guard_col, direction))
                else:
                    direction = "^"
            else:
                guard_col -= 1
    
    # if we got here it's because we exited the map, hence we're loopless
    return 0

## part 1

start_time = time.time()
result = 0

possible_obstacle_positions = set() # set of tuples: (row, col)

# The new obstruction can't be placed at the guard's starting position

direction = "^"
while guard_row >= 0 and guard_row < map_size and guard_col >= 0 and guard_col < map_size:

    if direction == "^":
        map[guard_row, guard_col] = "0" # visited
        if guard_row > 0:
            if map[guard_row-1, guard_col] != "#":
                guard_row -= 1
                possible_obstacle_positions.add((guard_row, guard_col))
            else:
                direction = ">"
        else:
            guard_row -= 1
    elif direction == ">":
        map[guard_row, guard_col] = "0" # visited
        if guard_col < map_size-1:
            if map[guard_row, guard_col+1] != "#":
                guard_col += 1
                possible_obstacle_positions.add((guard_row, guard_col))
            else:
                direction = "v"
        else:
            guard_col += 1
    elif direction == "v":
        map[guard_row, guard_col] = "0" # visited
        if guard_row < map_size-1:
            if map[guard_row+1, guard_col] != "#":
                guard_row += 1
                possible_obstacle_positions.add((guard_row, guard_col))
            else:
                direction = "<"
        else:
            guard_row += 1
    else: # if direction = "<"
        map[guard_row, guard_col] = "0" # visited
        if guard_col > 0:
            if map[guard_row, guard_col-1] != "#":
                guard_col -= 1
                possible_obstacle_positions.add((guard_row, guard_col))
            else:
                direction = "^"
        else:
            guard_col -= 1


a, counts = np.unique(map, return_counts=True)
print("Count of each charater in the map, 0 gives us the unique visited positions:", a, counts)

print(f"Maximum theoretical positions where we can put an obstacle: {len(possible_obstacle_positions)}")

result = counts[2]
print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# ugly but fast
possible_obstacle_positions.discard((initial_guard_row, initial_guard_col))

for pos in tqdm(possible_obstacle_positions):

    # uncomment for visualization map[map == "0"] = "."

    map[pos[0], pos[1]] = "#"
    result += is_it_loop(initial_guard_row, initial_guard_col)
    # uncomment for visualization map[pos[0], pos[1]] = "B"
    # uncomment for visualization print_map()
    map[pos[0], pos[1]] = "."

print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))