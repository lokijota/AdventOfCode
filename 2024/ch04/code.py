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

# regex_expr = ".*?(?:(mul\(\d+,\d+\)).*?)+"
# doesn't restrict 1-3 digits

print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))