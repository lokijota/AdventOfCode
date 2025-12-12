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

# ok, so this the numbers are not always right aligned, which is annoying
# and require going back to the original data before it was converted to 
# a matrix of integers

# get the positions of the operators -- that's where the numbers for each colum start
column_starts = []
operand_lines = np.array([list(line) for line in lines[:-1]])

for idx, el in enumerate(lines[-1]):
    if el != " ":
        column_starts.append(idx)

# now let's collect the numbers

for idx, column_start in enumerate(column_starts):
    if idx < len(column_starts)-1:
        col_end = column_starts[idx+1]-1 # isto falha para o último mas vamos ignorar por agora
    else:
       col_end = 4000 # or whatever

    column = operand_lines[:, column_start:col_end].transpose()

    vals = ','.join([''.join(row) for row in column]).split(",")
    vals = [int(x) for x in vals]

    if operators[idx] == "+":
        result += np.sum(vals)
    else:
        result += math.prod(vals)

print("Result part 2: ", result)  # 11643736116335
print("--- %s seconds ---" % (time.time() - start_time))