import copy
import itertools
import math
import matplotlib.pyplot as plt
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

with open('ch25/input.txt') as f:
    records = f.read().split("\n\n")

## parse data

lock_shapes = []
lock_counts = []

key_shapes = []
key_counts = []

for entry in records:
    # read elements to a list, reshape to the shape of the lock, and remove first and last rows which are just markers
    marker = entry[0]

    record_shape = np.reshape([element for element in entry if element in ["#", "."]], (7,5))[1:-1]

    counts = []
    for column in record_shape.T:
        counts.append(np.count_nonzero(column == "#"))
    
    if marker == "#": #lock
        lock_shapes.append(record_shape)
        lock_counts.append(counts)

    else: #key
        key_shapes.append(record_shape)
        key_counts.append(counts)


## functions and classes

## part 1

start_time = time.time()
result = 0

for the_key in key_counts:
    for the_lock in lock_counts:
        print("Comparing", the_key, the_lock)
        if all(kh+lh <= 5 for kh,lh in zip(the_key,the_lock)):
            result += 1

print("Result part 1: ", result) #3127
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))


