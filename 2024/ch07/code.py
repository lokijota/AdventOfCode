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
from itertools import pairwise, product
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

def generator(operator_symbols, n):
    """Generate all the combinations of operators to apply. Simple but innefficient, as it happens for every single sequence"""
    yield from product(*([operator_symbols] * n))  #itertools.product

for row in data:
    # print(row)
    lr = len(row[1])-1
    for x in generator('+*|', lr):
        operations = (''.join(x))

        register = row[1][0]

        for opval in zip(operations, row[1][1:]):
            if opval[0] == "+":
                register += opval[1]
            elif opval[0] == "*":
                register *= opval[1]
            else:
                register = int(f'{register}{opval[1]}')
                # register = int(str(register) + str(opval[1]))
 
            if register > row[0]:
                break
        
            # print(op, register)
        
        if register == row[0]:
            # print(f"found, {result}")
            result += row[0]
            break



print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))