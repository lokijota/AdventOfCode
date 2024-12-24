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

with open('ch19/input.txt') as f:
    lines = f.read().split("\n\n")

## parse data
towels = lines[0].split(", ")
patterns = lines[1].split("\n")

## functions and classes

def find_pattern(pattern, towels, dead_ends = []):
    if len(pattern) == 0:
        return True
    elif pattern in dead_ends:
        return False
    
    for towel in towels:
        if pattern.startswith(towel) and find_pattern(pattern[len(towel):], towels, dead_ends):
            return True

    dead_ends.append(pattern)
    return False

## part 1

start_time = time.time()
result = 0

count = 0
for pattern in patterns:
    count += 1
    result += int(find_pattern(pattern, towels, []))
    # print("Current count: ", result, "of", count)

# 226 in 0.2 secs
print("Result part 1: ", result) 
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))