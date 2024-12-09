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

with open('ch09/input.txt') as f:
    lines = f.read().splitlines()

## parse data

data = lines[0]
print(f"Len: {len(data)}")

file_size = 0
file_count = 0
space_size = 0
space_count = 0
for idx, d in enumerate(data):
    if idx % 2 == 0:
        file_size += int(d)
        file_count += 1
    else:
        space_size += int(d)
        space_count += 1
    
# File size: 50174 in 10000 files, space_size: 44938 in 9999 free blocks, total: 95112
print(f"File size: {file_size} in {file_count} files, space_size: {space_size} in {space_count} free blocks, total: {file_size+space_size}")

## functions

## part 1

start_time = time.time()
result = 0

# the space ocupied isn't too large, under 100k, but as there are 10k files, I can't use a character code to represent it. it'd have to be an int.
# disk_map = np.zeros((file_size+space_size,), dtype=int)

disk_map=np.empty((file_size+space_size,))
disk_map.fill(-1)

# fill the disk
disk_pointer = 0
file_num = 0
for idx, d in enumerate(data):
    val = int(d)
    if idx % 2 == 0: #file
        disk_map[disk_pointer:disk_pointer+val] = file_num
        file_num += 1
    disk_pointer += val


def find_free_space(disk_map, starting_from):
    first_empty = np.argmax(disk_map[starting_from:]==-1) + starting_from

    empty_length = 0
    while first_empty+empty_length < len(disk_map) and disk_map[first_empty+empty_length] == -1:
        empty_length += 1

    return first_empty, empty_length 


next_free = 0
disk_size = file_size+space_size
last_file_pos = disk_size
while True: 
    next_free, empty_length = find_free_space(disk_map, next_free) 
    
    # ugly but it works
    if empty_length >= 10:
        break

    # now get values from the end with the size of the empty space --- need argmax from the end
    last_file_pos = disk_size - np.argmax(disk_map[::-1] >= 0) -1
    
    count = 0 
    # ugly -- I'm sure I have too many variables down there
    while empty_length > 0 and disk_map[last_file_pos] != -1:
        disk_map[next_free+count] = int(disk_map[last_file_pos])
        disk_map[last_file_pos] = -1
        last_file_pos -= 1
        empty_length -= 1
        count += 1

    # print(disk_map)

# np.set_printoptions(threshold=sys.maxsize, precision=0)
# print(disk_map.astype(int))

for idx, val in enumerate(disk_map):
    if val == -1:
        continue
    else:
        result += (val*idx)

# 6390180901651
print("Result part 1: ", int(result)) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0



print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))