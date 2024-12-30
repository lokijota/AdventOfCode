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

## global variables

with open('ch22/input.txt') as f:
    lines = f.read().splitlines()

## parse data

## functions and classes

def random_number_generator(seed):
    nb = ((seed*64)^seed) % 16777216
    nb = int(nb/32)^nb
    nb = ((nb*2048)^nb)%16777216
    return nb

## part 1

start_time = time.time()
result = 0

# print(random_number_generator(123))

for random_nb in lines:
    random_nb = int(random_nb)
    for _ in range(0, 2000):
        random_nb = random_number_generator(random_nb)

    print(random_nb) 
    result += random_nb

print("Result part 1: ", result) # 13584398738
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))


