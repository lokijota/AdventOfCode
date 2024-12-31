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

with open('ch23/input.txt') as f:
    lines = f.read().splitlines()

## parse data

## functions and classes

def has_pc_starting_with_t(iterable):
    for element in iterable:
        if element.startswith("t"):
            return True
    
    return False

## part 1

start_time = time.time()
result = 0

# connected_computers_list = []

# for line in lines:
#     pc1, pc2 = line.split("-")

#     matches = []
#     for idx, connected_computers in enumerate(connected_computers_list):
#         if pc1 in connected_computers or pc2 in connected_computers_list:
#             matches.append(idx)
    
#     if len(matches) == 0:
#         new_group = set()
#         new_group.add(pc1)
#         new_group.add(pc2)
#         connected_computers_list.append(new_group)
#     elif len(matches) == 1:
#         connected_computers_list[matches[0]].add(pc1)
#         connected_computers_list[matches[0]].add(pc2)
#     else: #merge two sets
#         connected_computers_list[matches[0]].update(connected_computers_list[matches[1]])
#         connected_computers_list[matches[0]].add(pc1)
#         connected_computers_list[matches[0]].add(pc2)
#         connected_computers_list.remove(connected_computers_list[matches[1]])

# now check the 

# for pc_set in connected_computers_list:
#     if has_pc_starting_with_t(pc_set):
#         for pc_trio in itertools.combinations(pc_set, 3):
#             if has_pc_starting_with_t(pc_trio):
#                 result += 1

pc_connections = {}

for line in lines:
    pc1, pc2 = line.split("-")
    if pc1 not in pc_connections:
        pc_connections[pc1] = set()
    pc_connections[pc1].add(pc2)
    pc_connections[pc1].add(pc1) # add itself to the set
    
    if pc2 not in pc_connections:
        pc_connections[pc2] = set()
    pc_connections[pc2].add(pc1)
    pc_connections[pc2].add(pc2) # add itself to the set
                                
results = set()

for key, value in pc_connections.items():

    if has_pc_starting_with_t(value):
        for pc_trio in itertools.combinations(value, 3):
            if has_pc_starting_with_t(pc_trio):
                if pc_trio[1] in pc_connections[pc_trio[0]] and pc_trio[2] in pc_connections[pc_trio[0]] and \
                    pc_trio[0] in pc_connections[pc_trio[1]] and pc_trio[2] in pc_connections[pc_trio[1]] and \
                    pc_trio[0] in pc_connections[pc_trio[2]] and pc_trio[1] in pc_connections[pc_trio[2]]:

                    results.add(frozenset(pc_trio))

result = len(results)
print("Result part 1: ", result) # 1119 in 0.029 seconds
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0


print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))


