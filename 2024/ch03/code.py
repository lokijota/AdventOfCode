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

## read data

## global variables

with open('ch03/sample.txt') as f:
    lines = f.read().splitlines()

data = []

## functions

## part 1

start_time = time.time()
result = 0


print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0


print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))