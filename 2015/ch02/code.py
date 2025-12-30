import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

# from itertools import groupby
# import numpy as np
# from collections import deque 
# import math
# from collections import Counter
# import sys
# import re
# import copy
# from tqdm import tqdm
# import random
# import matplotlib.pyplot as plt
# from matplotlib import path

## read data

## global variables

with open('ch02/input.txt') as f:
    lines = f.read().splitlines()

## functions


## part 1

start_time = time.time()
result = 0

for line in lines:
    
    sizes = [int(x) for x in line.split('x')]
    smallest = min(sizes)
    
    area = 2*sizes[0]*sizes[1] + 2*sizes[1]*sizes[2] + 2*sizes[0]*sizes[2] + min(sizes[0]*sizes[1], sizes[1]*sizes[2], sizes[0]*sizes[2] )
    result += area

print("Result part 1: ", result) # 1586300
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

for line in lines:
    sizes = [int(x) for x in line.split('x')]
    sizes.sort()

    ribbon = 2*sizes[0] + 2*sizes[1] + sizes[0]*sizes[1]*sizes[2]
    result += ribbon

print("Result part 2: ", result)  # 
print("--- %s seconds ---" % (time.time() - start_time))
