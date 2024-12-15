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
from operator import add

## read data

## global variables

with open('ch15/sample.txt') as f:
    lines = f.read().split("\n\n")

## parse data

map = []
for row in lines[0].splitlines():
    map.append([letter for letter in row])

map = np.array(map)

instructions = np.array(lines[1].replace("\n", ""))
instructions = instructions.flatten()[0]

map_backup = np.copy(map) # for part 2

## functions

dir_ht = dict()
dir_ht["^"] = (-1, 0)
dir_ht["v"] = (1, 0)
dir_ht["<"] = (0, -1)
dir_ht[">"] = (0, 1)

def find_moveable_range(slice, reverse):

    data = slice
    if reverse:
        data = reversed(data)

    moveable = 0
    for element in data:
        if element == "O":
            moveable += 1
        elif element == "#":
            return 0
        elif element == ".":
            return moveable
    
    return moveable
    

def move_robot(map: np.array, robot_pos: tuple, instruction: str) -> tuple:

    target_pos = (robot_pos[0] + dir_ht[instruction][0], robot_pos[1] + dir_ht[instruction][1])

    if map[*target_pos] == ".":
        map[*robot_pos] = "."
        map[*target_pos] = "@"

        return target_pos

    if map[*target_pos] == "O":
        
        slice = []
        if instruction == "^":
            slice = map[0:robot_pos[0], robot_pos[1]]
            if (rl := find_moveable_range(slice, True)) > 0:
                start_row = robot_pos[0]-rl
                end_row = robot_pos[0]
                map[start_row-1:end_row, robot_pos[1]] = map[start_row:end_row+1, robot_pos[1]]
                map[*robot_pos] = "."
                robot_pos = target_pos

        elif instruction == ">":
            slice = map[robot_pos[0], robot_pos[1]+1:]
            if (rl := find_moveable_range(slice, False)) > 0:
                map[robot_pos[0], robot_pos[1]+1:robot_pos[1]+rl+2]  = map[robot_pos[0], robot_pos[1]:robot_pos[1]+rl+1] 
                map[*robot_pos] = "."
                robot_pos = target_pos

        elif instruction == "v":
            slice = map[robot_pos[0]+1:, robot_pos[1]]
            if (rl := find_moveable_range(slice, False)) > 0:
                map[robot_pos[0]+1:robot_pos[0]+rl+2, robot_pos[1]] = map[robot_pos[0]:robot_pos[0]+rl+1, robot_pos[1]]
                map[*robot_pos] = "."
                robot_pos = target_pos

        elif instruction == "<":
            slice = map[robot_pos[0], 0:robot_pos[1]]
            if (rl := find_moveable_range(slice, True)) > 0:
                start_col = robot_pos[1]-rl
                end_col = robot_pos[1]
                map[robot_pos[0], start_col-1:end_col] = map[robot_pos[0], start_col:end_col+1]
                map[*robot_pos] = "."
                robot_pos = target_pos
        
        # print(slice)

    return robot_pos

def score(map):
    score = 0
    for idx_row, row in enumerate(map):
        for idx_col, val in enumerate(row):
            if val == "O":
                score += (idx_row*100 + idx_col)

    return score


## part 1

start_time = time.time()
result = 0

robot_pos = np.unravel_index(np.argmax(map == "@"), map.shape)

for instruction in instructions:
    robot_pos = move_robot(map, robot_pos, instruction)

# print(map)

result = score(map)
print("Result part 1: ", result) # 1429911
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# enlarge the map
fat_map = []

for idx_row, row in enumerate(map_backup):
    new_row = []
    for idx_col, val in enumerate(row):
        if val == "#":
            new_row.append("#")
            new_row.append("#")
        elif val == "O":
            new_row.append("[")
            new_row.append("]")
        elif val == ".":
            new_row.append(".")
            new_row.append(".")
        elif val == "@":
            new_row.append("@")
            new_row.append(".")
    
    fat_map.append(new_row)

map = np.array(fat_map)

with np.printoptions(threshold=np.inf, linewidth=np.inf):
    print(map)

print("Result part 2: ", int(result)) #
print("--- %s seconds ---" % (time.time() - start_time))