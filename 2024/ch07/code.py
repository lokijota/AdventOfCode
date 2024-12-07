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
from itertools import pairwise
import math

## read data

## global variables

with open('ch07/input.txt') as f:
    lines = f.read().splitlines()

## parse data

data = []

for line in lines:
    parts = line.split(":")
    data.append((int(parts[0]), [int(val.strip()) for val in parts[1].lstrip().split(" ")]))

## functions

## part 1

start_time = time.time()
result = 0

for row in data:
    for j in range(2**len(row[1])):
        
        register = row[1][0]

        for val in row[1][1:]:
            op = j & 1
            j = j >> 1

            if op == 0:
                register += val
            else:
                register *= val
            
            if register > row[0]:
                break
        
            # print(op, register)
        
        if register == row[0]:
            # print("found")
            result += row[0]
            break

print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0


print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))