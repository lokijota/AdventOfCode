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

## read data

## global variables

with open('ch11/input.txt') as f:
    entries = f.read().split(" ")

## parse data

data = dict()
for entry in entries:
    data[int(entry)] = 1

## functions

## part 1

start_time = time.time()
result = 0

# 25 for part 1, 75 for part 2 -- code is the same
for j in range(75):
    new_data = dict()

    for key,count in data.items():
        # rule 1
        if key == 0:
            new_data[1] = new_data.get(1, 0) + count
        # rule 2
        elif len(str(key)) % 2 == 0:

            key_s = str(key)

            left  = int(key_s[0:len(key_s)//2])
            right = int(key_s[len(key_s)//2:])

            new_data[left] = new_data.get(left, 0) + count
            new_data[right] = new_data.get(right, 0) + count
        # rule 3
        else:
            new_data[key*2024] = new_data.get(key*2024, 0) + count

    data = new_data

    # print(j+1, sum(data.values()))

result = sum(data.values())
print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

# start_time = time.time()
# result = 0


# print("Result part 2: ", int(result)) #
# print("--- %s seconds ---" % (time.time() - start_time))