import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

from itertools import groupby
import numpy as np
from collections import deque 
import math
# from collections import Counter
# import sys
# import re
# import copy
# from tqdm import tqdm
# import random
# import matplotlib.pyplot as plt
# import numpy as np

## read data

## global variables

with open('ch06/input.txt') as f:
    lines = f.read().splitlines()

operands = [line.split() for line in lines[:-1]]
operands = [[int(el) for el in i] for i in operands]
operands_matrix = np.array(operands)

operators = lines[-1].split()

## functions

## part 1

start_time = time.time()
result = 0

for operator_idx in range(len(operators)):
    if operators[operator_idx] == "+":
        result += np.sum(operands_matrix[:, operator_idx])
    else:
        result += math.prod(operands_matrix[:, operator_idx])

print("Result part 1: ", result) # 4693159084994
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0



print("Result part 2: ", result)  # 
print("--- %s seconds ---" % (time.time() - start_time))