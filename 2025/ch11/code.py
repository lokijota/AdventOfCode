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
# from matplotlib import path

## read data

## global variables

with open('ch11/input.txt') as f:
    lines = f.read().splitlines()

data = {}
for line in lines:
    parts = line.split(":")
    targets = parts[1].split()
    data[parts[0]] = targets

## functions

## part 1

start_time = time.time()
result = 0

# 1.0 Create data structure for the graph

# nodes = list(data.keys())
# nodes.append("out")

# # create nodes
# # init_graph["Origin"]["Destinatin"] = distance
# init_graph = {}
# for node in nodes:
#     init_graph[node] = {}

# # create edges
# for source_device, target_devices in data.items():
#     for target_device in target_devices:
#         init_graph[source_device][target_device] = 1

# graph = Graph(nodes, init_graph)
# previous_nodes, shortest_path = graph.dijkstra_algorithm(start_node="you")
# graph.print_result(previous_nodes, shortest_path, start_node="you", target_node="out")


def count_paths(graph, source, target):
    if source == target:
        return 1
    
    count = 0
    for connection in graph[source]:
        count += count_paths(graph, connection, target)    

    return count

result =  count_paths(data, "you", "out")

print("Result part 1: ", result) # 786
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0



print("Result part 2: ", result)  # 
print("--- %s seconds ---" % (time.time() - start_time))
