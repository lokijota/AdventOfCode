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
# from operator import add, sub
# import networkx as nx

## read data

## global variables

with open('ch18/input.txt') as f:
    lines = f.read().splitlines()

## parse data

if len(lines) < 30: # sample input data set
    grid = np.full(shape=(7,7), fill_value='.', dtype=str)
    count_drops = 12
    end_pos = (6,6)
else: # proper final dataset
    grid = np.full(shape=(71,71), fill_value='.', dtype=str)
    count_drops = 1024
    end_pos = (70,70)

## functions and classes

def printgrid(grid):
    for rows in grid:
        for val in rows:
            print(val, end="")
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
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)

        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]

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

def printPath(grid, path):
    for r in range(0, grid.shape[0]):
        for c in range(0, grid.shape[0]):
            if [r,c] in [[node[0],node[1]] for node in path]: 
                print(f"{bcolors.OKGREEN}O{bcolors.ENDC}", end="")
            else:
                print(grid[r][c], end="")
        print()

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
                current_min_node = node # the node we happen to be looking at
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
            # elif tentative_value == shortest_path[neighbor]:
            #     print("Found equal distance, ", tentative_value, " with neighbour ", neighbor, "current min node:", current_min_node)

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
    print(f"Number of nodes visited: {len(path)}")
    printPath(grid, path)

    return shortest_path[target_node]

## part 1

start_time = time.time()
result = 0

# make all the pieces drop and put them on the map
marked_positions = 0
for line in lines[:count_drops]:
    drop_location = tuple([int(s) for s in line.split(",")])

    grid[drop_location[1], drop_location[0]] = '#' #r,c
    marked_positions += 1

printgrid(grid)

# create the graph

nodes = []
init_graph = {}
for node in nodes:
    init_graph[node] = {}

# nodes
for idx_row, row in enumerate(grid):
    for idx_col, val in enumerate(row):
        if val == ".":
            nodes.append((idx_row, idx_col))
            init_graph[(idx_row, idx_col)] = {}
        
# edges
edge_count = 0
for node in nodes:
    for surrounding in [(node[0]+direction[0], node[1]+direction[1]) for direction in [(0,1), (0,-1), (1,0), (-1, 0) ]]:
        if surrounding[0] >= 0 and surrounding[1] >= 0 and surrounding[0] < grid.shape[0] and surrounding[1] < grid.shape[0] \
                    and grid[surrounding] != "#":
            init_graph[node][surrounding] = 1
            edge_count += 1

print(f"Nb of Nodes: {len(init_graph)}, nb of Edges: {edge_count} ")

# 
graph = Graph(nodes, init_graph)
previous_nodes, shortest_path_dj = dijkstra_algorithm(graph=graph, start_node=(0,0))
result = print_result(previous_nodes, shortest_path_dj, start_node=(0,0), target_node=end_pos)

# printPath(grid, shortest_path_dj)

print("Result part 1: ", int(result)) # 432 in 1.5 seconds after adding code to avoid adding repeated nodes to the nodes list (stupid mistake)
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# make all the remaining pieces drop and put them on the map
for line in lines[count_drops:]:
    drop_location = tuple([int(s) for s in line.split(",")]) #x,y
    drop_location = (drop_location[1], drop_location[0]) #r,c

    grid[drop_location] = '#'
    marked_positions += 1

    # if we added a stone that means we have to remove connections to and from it
    nodes.remove(drop_location)

    del init_graph[drop_location] 
    for k,v in init_graph.items():
        if drop_location in v.values():
            del v[drop_location]
            edge_count -= 1

    print("Deleted ", drop_location, ", marked positions: ", marked_positions)
    print(f"  Nb of Nodes: {len(init_graph)}, nb of Edges: {edge_count}")

    graph = Graph(nodes, init_graph)
    previous_nodes, shortest_path_dj = dijkstra_algorithm(graph=graph, start_node=(0,0))
    if end_pos not in previous_nodes:
        result = (drop_location[1], drop_location[0])
        print(">>> No path to target after removing ", result)
        break

# Result part 2:  (56, 27)
# --- 1306.9152591228485 seconds ---
print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))