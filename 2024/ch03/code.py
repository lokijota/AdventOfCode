import time
from collections import deque, Counter
import sys
import numpy as np
import re, regex
import copy
from tqdm import tqdm
import random
import matplotlib.pyplot as plt
import numpy as np
from itertools import pairwise

## read data

## global variables

with open('ch03/input.txt') as f:
    lines = f.read() #.splitlines()

data = []

## functions

## part 1

start_time = time.time()
result = 0

# regex_expr = ".*?(?:(mul\(\d+,\d+\)).*?)+"
# doesn't restrict 1-3 digits

regex_expr = "mul\(\d+,\d+\)"
results = re.findall(regex_expr, lines)


sum = 0
for op in results:
    op = str(op)
    op = op.replace("mul(", "").replace(")", "")
    parts = op.split(",")
    left = int(parts[0])
    right = int(parts[1])

    sum += left*right

result = sum


# It's worth noting that a repeated capture group will only store the last match that it found.
# Every time it makes a match, it will overwrite the previous match with the one it just found.



print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0


print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))