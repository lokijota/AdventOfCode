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

with open('ch24/input.txt') as f:
    lines = f.read().split("\n\n")

## parse data

circuit = {}

for inputs in lines[0].split("\n"):
    input_var, input_val = inputs.split(": ")
    circuit[input_var] = [int(input_val), "input", "noop", "noop"]

for operations in lines[1].split("\n"):
    operation, output = operations.split(" -> ")
    operation = operation.split(" ")
    circuit[output] = [None, operation[1], operation[0], operation[2]]


## functions and classes

def calculate(var, circuit):

    if circuit[var][0] is not None:
        return circuit[var][0]

    if circuit[var][1] == "AND":
        circuit[var][0] = calculate(circuit[var][2], circuit) & calculate(circuit[var][3], circuit)

    if circuit[var][1] == "OR":
        circuit[var][0] = calculate(circuit[var][2], circuit) | calculate(circuit[var][3], circuit)

    if circuit[var][1] == "XOR":
        circuit[var][0] = calculate(circuit[var][2], circuit) ^ calculate(circuit[var][3], circuit)

    return circuit[var][0]

## part 1

start_time = time.time()
result = 0

start_var = 0
values = []
while True:
    current_var = f'z{start_var:02}'
    if current_var not in circuit:
        break

    values.insert(0, calculate(current_var, circuit))
    start_var += 1

result = "".join([str(x) for x in values])
result = int(result, 2)

print("Result part 1: ", result) # 59364044286798 in 0.00012 seconds
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0


print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))


