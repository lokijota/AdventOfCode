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
from operator import add, sub

## read data

## global variables

with open('ch16/input.txt') as f:
    lines = f.read().splitlines()

## parse data

labirynth = []
for row in lines:
    labirynth.append([letter for letter in row])

labirynth = np.array(labirynth)
edge_len = len(labirynth)

## functions

def printmap(the_map):
    for row in the_map:
        for val in row:
            print(val, end="")
        print()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printPath(map, path):

    for r in range(0, edge_len):
        for c in range(0, edge_len):
            if [r,c] in [[node[0],node[1]] for node in path]: #path[2:]:
                print(f"{bcolors.OKGREEN}{map[r][c]}{bcolors.ENDC}", end="")
            else:
                print(map[r][c], end="")
        print()

###### https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
###### As in 2022 and 2023, trying Dijkstra. Reusing code from https://github.com/lokijota/AdventOfCode2023/blob/main/Challenges/ch17/code_graph.py

class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
        
    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical.
        In other words, if there's a path from node A to B with a value V,
        there needs to be a path from node B to node A with a value V.
        JOTA: COMMENTED CODE FOR THE BEHAVIOUR ABOVE -- DON'T WANT THINGS TO BE REVERSIBLE
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)
        
        # for node, edges in graph.items():
        #     for adjacent_node, value in edges.items():
        #         if graph[adjacent_node].get(node, False) == False:
        #             graph[adjacent_node][node] = value
                    
        return graph
    
    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes
    
    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            # JOTA added "node in self.graph and" because of the cleanup() addition 
            if node in self.graph and self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]
    

    # JOTA adition to clean-up nodes that have no connections, from the graph and node base -- makes dijkstra faster
    def cleanup(self):
        # self.nodes = nodes
        # self.graph = self.construct_graph(nodes, init_graph)

        self.graph = {k: v for k, v in self.graph.items() if len(v) > 0}
        self.nodes = [node for node in self.nodes if node in self.graph.keys()]
        return 1

def dijkstra_algorithm(graph, start_node):
    "Applies Dijkstra's shortest path algorithm"
    unvisited_nodes = list(graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            # JOTA edit - prevent revisiting nodes
            if current_min_node in previous_nodes:
                prev_visited_node = previous_nodes[current_min_node]
                if prev_visited_node[0] == neighbor[0] and prev_visited_node[1] == neighbor[1]:
                    continue
            # JOTA end edit

            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node

            # JOTA edit - this was an attempt at early termination but has the same result but takes more time (300 secs more for the input)
            # if neighbor[0] == nrows -1 and neighbor[1] == ncols - 1:
            #     print("pim achei-lo", tentative_value)
            #     return previous_nodes, shortest_path
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path

def print_result(previous_nodes, shortest_path, start_node, target_node):
    "Auxiliary function to print the path and map in a convenient way and returns the sum of the cost"
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    
    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed([''.join(i) for i in [str(i) for i in path]])))
    printPath(map, path)

    return shortest_path[target_node]


## part 1

start_time = time.time()
result = 0

start_pos = np.unravel_index(np.argmax(labirynth == "S"), labirynth.shape)
end_pos = np.unravel_index(np.argmax(labirynth == "E"), labirynth.shape)

# 1.0 create graph
nodes = []
init_graph = {}
for node in nodes:
    init_graph[node] = {}

for idx_row, row in enumerate(labirynth):
    for idx_col, val in enumerate(row):
        if val in [".", "S", "E"]:

            for surrounding in [(idx_row+direction[0], idx_col+direction[1], direction[2]) for direction in [(0,1, "E"), (0,-1, "W"), (1,0, "S"), (-1, 0, "N") ]]:
                if labirynth[surrounding[0], surrounding[1]] == ".":
                    nodes.append((idx_row, idx_col, surrounding[2]))
                    init_graph[(idx_row, idx_col, surrounding[2])] = {}
                    print("Added: ", (idx_row, idx_col, surrounding[2]))

print(f"Nb of Nodes: {len(init_graph)}, start pos = {start_pos}, end pos = {end_pos}")

# 2.0 

print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

print("Result part 2: ", int(result)) #1453087
print("--- %s seconds ---" % (time.time() - start_time))