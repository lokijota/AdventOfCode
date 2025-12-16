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
import matplotlib.pyplot as plt
from matplotlib import path

## read data

## global variables

with open('ch09/input.txt') as f:
    lines = f.read().splitlines()

red_tiles = [[int(j) for j in line.split(",")] for line in lines]
red_tiles = [(r,c) for (c,r) in red_tiles] # input has col,row instead of row,col (bah)

## functions


## part 1

start_time = time.time()
result = 0

larger_area = 0
for tile1 in red_tiles:
    for tile2 in red_tiles:
        if tile1 != tile2:
            area = abs(tile1[0]-tile2[0]+1) * abs(tile1[1]-tile2[1]+1)
            if area > larger_area:
                larger_area = area

result = larger_area

print("Result part 1: ", result) # 4782151432
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0
larger_area = 0

def draw_line(map, start, end):
    h_start = min(start[0], end[0])
    h_end = max(start[0], end[0])
    v_start = min(start[1], end[1])
    v_end = max(start[1], end[1])

    if h_start>h_end:
        h_start, h_end = h_end, h_start
    if v_start>v_end:
        v_start, v_end = v_end, v_start

    if h_start == h_end:
        map[h_start, v_start+1:v_end] = 128
    elif v_start == v_end:
        map[h_start+1:h_end, v_start] = 128
    
    return map

def draw_on_map(map, red_tiles):

    for idx, rt in enumerate(red_tiles[:-1]):
        # draw the corners
        map[rt[0], rt[1]] = 255

        map = draw_line(map, rt, red_tiles[idx+1])

    map[red_tiles[-1][0], red_tiles[-1][1]] = 255
    map = draw_line(map, red_tiles[-1], red_tiles[0])
    
    return map

# Small optmization by shifting all tiles to start from 0,0 (saves memory in case I go for a map approach)
dim_sizes = np.array(red_tiles).max(axis=0) - np.array(red_tiles).min(axis=0)
deltas = np.array(red_tiles).max(axis=0) - dim_sizes
red_tiles = [list(np.array(tile) - deltas) for tile in red_tiles]

map = np.zeros((dim_sizes[0]+1, dim_sizes[1]+1), dtype=int)

map = draw_on_map(map, red_tiles)

# plt.imshow(map.transpose(), cmap='gray_r', vmin=0, vmax=255) #cmap='gray', 

red_tiles_arr = np.array(red_tiles)

# 1. Create a reference structure of all row and column start positions (the indices where red tiles are located)
# Note that the rows/cols are overlaping: the last down pos is the first of the next tile

row_starts = np.unique(sorted(red_tiles_arr[:,0])) #248
col_starts = np.unique(sorted(red_tiles_arr[:,1])) #248 items, 496 unsorted

# 2. Now create a compressed map of row_starts x col_starts
compressed_map = np.zeros((len(row_starts), len(col_starts)), dtype=int)

# 3. Fill the compressed map by checking each cell center point if it is inside the polygon

rtp = path.Path(red_tiles)

for r in range(len(row_starts)):
    for c in range(len(col_starts)):
        # radius -- without this, or with a positive radius, it wouldn't get the points over the line right
        # not sure if it'll also work on the full data set
        if rtp.contains_point((row_starts[r], col_starts[c]), radius=-0.1):
            compressed_map[r, c] = 128  # inside

# plt.imshow(compressed_map.transpose(), cmap='gray_r', vmin=0, vmax=255, interpolation="none") #cmap='gray', 

# 4. Now check all possible rectangles in the compressed map (which is much smaller) for enclosed areas
larger_area = 0
larger_area_edges = []
larger_area_edges_compressed = []

# print("Compressed map:")
# print(compressed_map)

print("Starting rectangle search on compressed map...")
for r1 in range(len(row_starts)):
    for r2 in range(r1+1, len(row_starts)):
        for c1 in range(len(col_starts)):
            for c2 in range(c1+1, len(col_starts)):
                
                # Define corners in real map coordinates
                corner1 = [row_starts[r1], col_starts[c1]]
                corner2 = [row_starts[r1], col_starts[c2]]
                corner3 = [row_starts[r2], col_starts[c1]]
                corner4 = [row_starts[r2], col_starts[c2]]
                
                if (compressed_map[r1, c1] in (128, 256) and
                    compressed_map[r1, c2] in (128, 256) and
                    compressed_map[r2, c1] in (128, 256) and
                    compressed_map[r2, c2] in (128, 256)):

                    # two of these have to be on the original red_tiles list
                    if (corner1 in red_tiles and corner4 in red_tiles) or (corner2 in red_tiles and corner3 in red_tiles):

                        # Calculate area in original map coordinates
                        h_start = row_starts[r1]
                        h_end = row_starts[r2]
                        v_start = col_starts[c1]
                        v_end = col_starts[c2]
                        area = (h_end - h_start + 1) * (v_end - v_start + 1)

                        # no point doing any more checks if the area is smaller (this could be higher up but prob no significant impact)
                        if area < larger_area:
                            continue
                        
                        enclosed = True

                        # Check the edges
                        for cc in range(c1, c2+1):
                            if compressed_map[r1, cc] != 128 or compressed_map[r2, cc] != 128:
                                enclosed = False
                                break
                        for rr in range(r1, r2+1):
                            if compressed_map[rr, c1] != 128 or compressed_map[rr, c2] != 128:
                                enclosed = False
                                break
                        
                        if enclosed:
                            if area > larger_area:
                                print(" New larger area found: ", area, "H:", h_start, "-", h_end, "V:", v_start, "-", v_end )
                                print("      --- %s seconds ---" % (time.time() - start_time))
                                larger_area = area

result = larger_area

print("Result part 2: ", result)  # 1450414119
print("--- %s seconds ---" % (time.time() - start_time))
