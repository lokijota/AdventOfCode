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

## read data

## global variables

with open('ch04/input.txt') as f:
    lines = f.read().splitlines()

## functions

def collect_strings(lines):
    result = lines
    transposed_lines = [''.join(s) for s in zip(*lines)]

    last_row= len(lines)
    last_col = len(lines[0])-1

    # collect strings from left and right columns
    diagonal_up = []
    diagonal_down = []

    for idx, _ in enumerate(lines):
        # collect diagonal up
        row = idx
        col = 0
        diagonal_string_from_left = ""
        diagonal_string_from_right = ""
        while row >= 0:
            diagonal_string_from_left += lines[row][col]
            diagonal_string_from_right += lines[row][last_col-col]
            col += 1
            row -= 1

        diagonal_up.append(diagonal_string_from_left)
        diagonal_up.append(diagonal_string_from_right)

        # collect diagonal down
        row = idx+1 # +1 to avoid doing the diagonals twice
        col = 0
        diagonal_string_from_left = ""
        diagonal_string_from_right = ""
        while row < last_row:
            diagonal_string_from_left += lines[row][col]
            diagonal_string_from_right += lines[row][last_col-col]
            col += 1
            row += 1

        diagonal_down.append(diagonal_string_from_left)
        diagonal_down.append(diagonal_string_from_right)

    return result + transposed_lines + diagonal_down + diagonal_up 

## part 1

start_time = time.time()
result = 0

text = collect_strings(lines)

for row in text:

    if len(row) < 4: 
        continue

    result += row.count("XMAS")
    result += row.count("SAMX")

print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# get the convolution
# do a bitwise xor with the different options

def check_sequence(tridim_array):
    # inspired by the idea of convolutions, I thought I'd apply rolling masks of 3x3
    # Bumped into several annoying issues, eg np.bitwise_xor not working with strings forcing to covert then to ints
    # anyway, could have done some optimizations but it runs in 0.14 secs so it's good enough

    # print(tridim_array)

    masks = [ [["M", ".", "M"],  [".", "A", "."], ["S", ".", "S"]], \
              [["M", ".", "S"],  [".", "A", "."], ["M", ".", "S"]], \
              [["S", ".", "M"],  [".", "A", "."], ["S", ".", "M"]], \
              [["S", ".", "S"],  [".", "A", "."], ["M", ".", "M"]] ]

    masks = np.array(masks)

    # tridim_array_cp = np.copy(tridim_array)
    tridim_array_cp = np.array([[ord(el) for el in row] for row in tridim_array])

    for mask in masks:
        mask[0,1] = tridim_array[0,1]
        mask[1,0] = tridim_array[1,0]
        mask[1,2] = tridim_array[1,2]
        mask[2,1] = tridim_array[2,1]

        mask = np.array([[ord(el) for el in row] for row in mask])

        if np.bitwise_xor(mask, tridim_array_cp).sum() == 0:
            return True

    return False

# convert list of strings into numpy array
map = []
for row in lines:
    map.append([letter for letter in row])

map = np.array(map,str) 

# look for A's excluinding outside border
for idxrow, row in enumerate(map[1:-1, 1:-1]):
    # print(idxrow, row)
    for idxcol, letter in enumerate(row):
        if letter == "A":
            # print (idxrow, idxcol)    
            if check_sequence(map[idxrow:idxrow+3, idxcol:idxcol+3]):
                result += 1

print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))