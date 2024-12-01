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

with open('ch01/input.txt') as f:
    lines = f.read().splitlines()

data = []

for line in lines:
    data.append([int(x) for x in line.replace("   ", " ").split(" ")])

## functions

## part 1

start_time = time.time()
result = 0

data = np.array(data)
c1 = data[:,0]
c1.sort()
c2 = data[:,1]
c2.sort()
result = sum(abs(c2-c1)) # anticipated trick here -- abs is needed as it's the "distance" between the two columns

# 3246517
print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# using Counter to find frequency of elements
frequency = Counter(c2)

result = 0
for val in c1:
    result += val * frequency[val]

# 29379307
print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))