import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

from copy import deepcopy

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

def count_paths(graph, source, target):
    """ Simple recursive function that counts all the possible paths from source to target"""
    """ Doesn't actually scale for large/complex paths """
    if source == target or source == "out":
        return 1
    
    count = 0
    for connection in graph[source]:
        count += count_paths(graph, connection, target)    

    return count

result = count_paths(data, "you", "out")

print("Result part 1: ", result) # 786
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

def remove_nodes(graph, nodes_to_remove):
    """ Remove outgoing nodes from the graph """
    for itkey, itval in graph.items():
        for node_to_remove in nodes_to_remove:
            if node_to_remove in itval:
                itval.remove(node_to_remove)
    
    return graph

ascendants_cache = {}
ascendants_cache["svr"] = []

def find_ascendants(graph, node):
    """ Finds the nodes that point to a given node """
    """ Builds a cache using a dictionary, for performance """
    if node == "svr":
        return []

    if node in ascendants_cache.keys():
        return ascendants_cache[node]

    ascendants = []
    for itkey, itval in graph.items():
        if node in itval:
            ascendants.append(itkey)
    
    ascendants_cache[node] = ascendants
    return ascendants

def trace_distance_map2(graph, start_node, nodes_at_distance, distance, acc = 0):
    """ Main function for part 2 """
    """ Starting from a target node, it gathers all the nodes that are reacheable with 1 step away from it towards the source """
    """ It keeps accumulating the distance and returns it at the end """
    """ Recursive function. In the first call you must pass teh start node, and the end node in a dictionary with a single entry and a count of 1 """
    """ The function than moves back 1 vertex distance at a time, and keeps an accumulator with how many paths there are to that original """
    """ single entry. """
    # print(distance, len(nodes_at_distance))
    if start_node in nodes_at_distance.keys():
        # While moving back towards the source, we found path(s) from start to end. But there may be other paths between the start node
        # and the current ones, so let's store the count in an accumulator
        acc += nodes_at_distance[start_node]
        del nodes_at_distance[start_node]
    # elif distance > 600:
    #     return 0
    
    # if it turns out that we explored everything we had to explore, then return the # of paths between 
    if len(nodes_at_distance) == 0:
        return acc

    ascendants = []
    for node in nodes_at_distance.keys():
        ascendants += [(asc, nodes_at_distance[node]) for asc in find_ascendants(graph, node)]
    
    # consolidate the # of lists
    consolidated_ascendants = {}
    for asc in ascendants:
        if asc[0] in consolidated_ascendants:
            consolidated_ascendants[asc[0]] += asc[1]
        else:
            consolidated_ascendants[asc[0]] = asc[1]

    return trace_distance_map2(graph, start_node, consolidated_ascendants, distance+1, acc)

start_time = time.time()
result = 0

##
# Ok the approach is to break this into 2 problems with 3 segments each: check count of paths for each segment:
# - svr to dac, in a graph where I removed out and fft (to simplify graph/avoid double passing on fft)
# - svr to fft, , in a graph where I removed out and dac (to simplify graph/ avoid double passing on dac)
# - dac to fft and fft to dac, ...
# - dac to out, ...
# - fft to out, ...
# And then at the end multiply the results for each of the paths we found. If any of the segments has 0, means there's no path between that segment


# svr to dac or fft avoiding fft/dac
svr_to_dac = deepcopy(data)
svr_to_dac = remove_nodes(svr_to_dac, ["out", "fft"])
dm = {}
dm["dac"] = 1
svr_to_dac_count = trace_distance_map2(svr_to_dac, "svr", dm, 1)

svr_to_fft = deepcopy(data)
svr_to_fftt = remove_nodes(svr_to_fft, ["out", "dac"])
dm = {}
dm["fft"] = 1
ascendants_cache.clear() # to force a cache rebuild
svr_to_fft_count = trace_distance_map2(svr_to_fft, "svr", dm, 1)

# dac to fft and fft to dac
dac_to_fft = deepcopy(data)
dac_to_fft = remove_nodes(dac_to_fft, ["out", "svr"])
dm = {}
dm["fft"] = 1
ascendants_cache.clear() # to force a cache rebuild
dac_to_fft_count = trace_distance_map2(dac_to_fft, "dac", dm, 1)

fft_to_dac = dac_to_fft
dm = {}
dm["dac"] = 1
ascendants_cache.clear() # to force a cache rebuild
fft_to_dac_count = trace_distance_map2(fft_to_dac, "fft", dm, 1)

# dac and fft to end, excluding the other
fft_to_out = deepcopy(data)
fft_to_out = remove_nodes(fft_to_out, ["dac", "svr"])
dm = {}
dm["out"] = 1
ascendants_cache.clear() # to force a cache rebuild
fft_to_out_count = trace_distance_map2(fft_to_out, "fft", dm, 1)

dac_to_out = deepcopy(data)
dac_to_out = remove_nodes(dac_to_out, ["fft", "svr"])
dm = {}
dm["out"] = 1
ascendants_cache.clear() # to force a cache rebuild
dac_to_out_count = trace_distance_map2(dac_to_out, "dac", dm, 1)

# print(svr_to_dac_count)
# print(svr_to_fft_count)
# print(dac_to_fft_count)
# print(fft_to_dac_count)
# print(fft_to_out_count)
# print(dac_to_out_count)

result = svr_to_dac_count*dac_to_fft_count*fft_to_dac_count + svr_to_fft_count*fft_to_dac_count*dac_to_out_count

print("Result part 2: ", result)  # 495845045016588
print("--- %s seconds ---" % (time.time() - start_time))