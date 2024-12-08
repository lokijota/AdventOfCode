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
import itertools
import math
import operator

## read data

## global variables

with open('ch08/input.txt') as f:
    lines = f.read().splitlines()

## parse data

# convert list of strings into numpy array
map = []
for row in lines:
    map.append([letter for letter in row])

map = np.array(map,str) 

## functions

def print_map():
    """Convenience, for debug only"""
    print("------------")
    for row in map:
        for col in row:
            print(col, end="")
        print()

## part 1

start_time = time.time()
result = 0

# create a dictionary where the key is the frequency character and in each position it has the position tuple (row, col) where it's found
frequency_map = dict()

for idx_row, row in enumerate(map):
    for idx_col, col in enumerate(row):
        if col != ".":
            if col in frequency_map:
                frequency_map[col].append((idx_row, idx_col))
            else:
                frequency_map[col] = [(idx_row, idx_col)]


# print(frequency_map)

antinodes = set()
for frequency in frequency_map.keys():
    for comb in itertools.combinations(frequency_map[frequency], 2):
        # calculate distance
        dv = comb[0][0] - comb[1][0]
        dh = comb[0][1] - comb[1][1]
        # print(dv, dh)

        antinodes.add((comb[0][0]+dv,comb[0][1]+dh))
        antinodes.add((comb[1][0]-dv,comb[1][1]-dh))

        # print(comb)

map_size = map.shape[0]
for antinode in antinodes:
    if antinode[0] >= 0 and antinode[0]<map_size and antinode[1] >= 0 and antinode[1] < map_size:
        result += 1
        if map[*antinode] == ".":
            map[*antinode] = "#"

print_map()

print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

def calc_antinode(antinodes, base, dv, dh, operator):
    """This avoids code repetition in the main loop below"""
    while True:
            antinode = (operator(base[0], dv), operator(base[1], dh))
            if antinode[0] >= 0 and antinode[0]<map_size and antinode[1] >= 0 and antinode[1] < map_size:
                antinodes.add(antinode)
                base = antinode
            else:
                break

    return antinodes 

antinodes = set()
for frequency in frequency_map.keys():
    for comb in itertools.combinations(frequency_map[frequency], 2):
        # calculate vertical and horizontal distance
        dv = comb[0][0] - comb[1][0]
        dh = comb[0][1] - comb[1][1]

        calc_antinode(antinodes, comb[0], dv, dh, operator.add)
        calc_antinode(antinodes, comb[1], dv, dh, operator.add)
        calc_antinode(antinodes, comb[0], dv, dh, operator.sub)
        calc_antinode(antinodes, comb[1], dv, dh, operator.sub)

result = len(antinodes)

# mark in map just for visualization convenience
for antinode in antinodes:
    if map[*antinode] == ".":
        map[*antinode] = "#"

print_map()

print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))