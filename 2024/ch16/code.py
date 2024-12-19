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
import networkx as nx

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
            if [r,c] in [[node[0],node[1]] for node in path]: 
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
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)

        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]

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
    printPath(labirynth, path)

    return shortest_path[target_node]

ninety_deg_pos = dict()
ninety_deg_pos["N"] = [ (0, -1, "W"), (0, 1, "E") ]
ninety_deg_pos["S"] = ninety_deg_pos["N"]
ninety_deg_pos["E"] = [ (-1, 0, "N"), (1, 0, "S") ]
ninety_deg_pos["W"] = ninety_deg_pos["E"]

def get_available_rotation_nodes(labirynth, node):
    if node[2] == "X": # end node, there's no escaping it
        return []

    rotated_positions = ninety_deg_pos[node[2]]
    return [(node[0]+pos[0], node[1]+pos[1], pos[2]) for pos in rotated_positions if labirynth[(node[0]+pos[0], node[1]+pos[1])] == "."]


## part 1

start_time = time.time()
result = 0

start_pos = np.unravel_index(np.argmax(labirynth == "S"), labirynth.shape)
start_pos = (start_pos[0], start_pos[1], "E")
end_pos = np.unravel_index(np.argmax(labirynth == "E"), labirynth.shape)
end_pos = (end_pos[0], end_pos[1], "X")


# 1.0 Create graph
nodes = []
init_graph = {}
for node in nodes:
    init_graph[node] = {}

for idx_row, row in enumerate(labirynth):
    for idx_col, val in enumerate(row):
        if val in [".", "S"]: # don't do this logic when it's the E node
            for surrounding in [(idx_row+direction[0], idx_col+direction[1], direction[2]) for direction in [(0,1, "E"), (0,-1, "W"), (1,0, "S"), (-1, 0, "N") ]]:
                nodes.append((idx_row, idx_col, surrounding[2]))
                init_graph[(idx_row, idx_col, surrounding[2])] = {}
        elif val == "E":
            nodes.append((idx_row, idx_col, "X")) # x marks the spot -- the ending
            init_graph[(idx_row, idx_col, "X")] = {}

print(f"Nb of Nodes: {len(init_graph)}, start pos = {start_pos}, end pos = {end_pos}")

# 2.0 Add edges

edge_count = 0
nx_edges = []

def shorten(node):
    return f"{node[0]}.{node[1]}{node[2]}"

for node in nodes:
    for surrounding in [(node[0]+direction[0], node[1]+direction[1], direction[2]) for direction in [(0,1, "E"), (0,-1, "W"), (1,0, "S"), (-1, 0, "N") ]]:
        if labirynth[surrounding[0], surrounding[1]] == ".": # and surrounding not in init_graph[node]:
            if node[2] == surrounding[2]: # pointing in the same direction, just connect with weight 1
                init_graph[node][surrounding] = 1 # weight of moving in a straight line
                # nx_edges.append((shorten(node), shorten(surrounding)))
                edge_count += 1
            elif len(rotated_90_degrees_nodes := get_available_rotation_nodes(labirynth, node))>0:
                for rotated_node in rotated_90_degrees_nodes:
                    init_graph[node][rotated_node] = 1001
                    # nx_edges.append((shorten(node), shorten(rotated_node)))
                    edge_count += 1

        elif labirynth[surrounding[0], surrounding[1]] == "E":
            if node[2] == surrounding[2]: # pointing in the same direction, just connect with weight 1
                init_graph[node][end_pos] = 1 # weight of moving in a straight line
                nx_edges.append((shorten(node), shorten(end_pos)))
                edge_count += 1
            elif len(rotated_90_degrees_nodes := get_available_rotation_nodes(labirynth, node))>0:
                for rotated_node in rotated_90_degrees_nodes:
                    init_graph[node][end_pos] = 1001
                    nx_edges.append((shorten(node), shorten(end_pos)))
                    edge_count += 1
    
    # print(f"Node {node} is now connected to {init_graph[node]}")

# For visualization but it doesn't really work
# instantiate a nx.Graph object
# G = nx.DiGraph()
# G.add_edges_from(nx_edges)
# options = {
#     'node_color': 'red',
#     'node_size': 5,
#     'width': 2,
#     'edge_color': 'green',
#     'font_size': 11
# }

# subax1 = plt.subplot(111) # the figure has 1 row, 1 columns, and this plot is the first plot.
# fig = plt.figure(1, figsize=(2000, 1000), dpi=60)
# nx.draw(G, with_labels=True, font_weight='normal', **options)
# plt.show()
                
print(f"Nb of edges: {edge_count}")

graph = Graph(nodes, init_graph)
previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=start_pos)

print_result(previous_nodes, shortest_path, start_node=start_pos, target_node=end_pos)

print("Result part 1: ", result) #91464 in 123.4 seconds
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

print("Result part 2: ", int(result)) #1453087
print("--- %s seconds ---" % (time.time() - start_time))