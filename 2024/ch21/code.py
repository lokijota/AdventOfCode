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

with open('ch21/input.txt') as f:
    lines = f.read().splitlines()

## parse data

## functions and classes

class NumericKeyboard:
    def __init__(self, controller):
        self.current_position = "A"
        self.parent = controller
        self.count_moves = 0
        self.key_coordinates = { "7" : (0, 0), "8" : (0, 1), "9" : (0, 2), "4" : (1, 0), "5" : (1, 1), "6" : (1, 2), "1" : (2, 0), "2" : (2, 1), "3" : (2, 2), "0" : (3, 1), "A" : (3, 2) }

    def lowest_cost_of_move_to(self, target_key):
        paths = self.get_paths_to(target_key)
        self.count_moves += len(paths[0])
        print(f"current key {self.current_position}, target key = {target_key}, sum of moves = {self.count_moves}")
        self.current_position = target_key

        return self.parent.lowest_cost_key_sequence(paths)

    def get_paths_to(self, target_key):
        # Note: this is a lot of work but this only happens for the main inputs in the data files, i.e., not for a lot of repetitions. So there's no 
        # advantage in optimizing this calculation by storing results in a cache.

        # first we have to find how to get to the target key, and for that we have to determine the possible valid paths
        vert_diff = self.key_coordinates[target_key][0] - self.key_coordinates[self.current_position][0]        
        horz_diff = self.key_coordinates[target_key][1] - self.key_coordinates[self.current_position][1]

        needed_moves = ""
        if horz_diff > 0:
            needed_moves += horz_diff*">"
        else:
            needed_moves += abs(horz_diff)*"<"

        if vert_diff > 0:
            needed_moves += vert_diff*"v"
        else:
            needed_moves += abs(vert_diff)*"^"

        # this generates all possible paths to the target key. This is a set of tuples, where each tuple is a path,
        # but I convert that to strings for convenience of my thinking brain
        possible_paths = set(itertools.permutations(needed_moves, len(needed_moves)))
        possible_paths = { "".join(path) for path in possible_paths }

        # now we have to check if the paths are valid, i.e. they don't go through location with no key
        invalid_paths = set()
        for path in possible_paths:
            curr_pos_row, curr_pos_col = self.key_coordinates[self.current_position]

            for move in path:
                if move == ">":
                    curr_pos_col += 1
                elif move == "<":
                    curr_pos_col -= 1
                elif move == "v":
                    curr_pos_row += 1
                elif move == "^":
                    curr_pos_row -= 1
                
                if curr_pos_row == 3 and curr_pos_col == 0:
                    # print(f"invalid path: {path}")
                    invalid_paths.add(path)

        # and this allows us to finally determine the valid paths
        valid_paths = possible_paths - set(invalid_paths)

        valid_paths_with_A = set()
        for path in valid_paths:
            valid_paths_with_A.add( path + "A" ) 

        return list(valid_paths_with_A)
    
alternative_paths_cache = {}
path_cache = {}

class DirectionalKeyboard:
    def __init__(self, id, controller):
        self.id = id
        self.current_position = "A"
        self.key_coordinates = { "^" : (0, 1), "A" : (0, 2), "<" : (1, 0), "v" : (1, 1),  ">" : (1, 2) }
        self.count_moves = 0
        self.parent = controller

    def lowest_cost_key_sequence(self, key_sequences_on_lower_kbd):
        global lcks_cache

        # aggressive use of caches, yep. this one is super effective.
        lcks_cache_key = self.id + "-".join(key_sequences_on_lower_kbd)
        if lcks_cache_key in lcks_cache:
            return lcks_cache[lcks_cache_key]

        min_cost = math.inf
        min_path = []

        for key_sequence_on_lower_kbd in key_sequences_on_lower_kbd:
            key_sequences_on_this_kbd = self.get_alternative_paths(key_sequence_on_lower_kbd)

            min_kp_cost = 0
            min_kp_path = []
            for idx_kp, kp in enumerate(key_sequences_on_this_kbd):
                lc_cost, lc_path = self.parent.lowest_cost_key_sequence(kp)
                self.current_position = key_sequence_on_lower_kbd[idx_kp] # each entry in the key_presses list leaves the final key in a different position, corresponding to the entry in the path
                min_kp_cost += lc_cost
                min_kp_path.append(lc_path)
        
            # self.current_position = "A"

            if min_kp_cost < min_cost:
                min_cost = min_kp_cost
                min_path = min_kp_path

        lcks_cache[lcks_cache_key] = (min_cost, min_path)
        return min_cost, min_path

    def get_alternative_paths(self, path: str):
        """ Example path value for the first directional keyboard is. ^^>A """ 
        global alternative_paths_cache

        cache_key = self.current_position + "_" + path
        if cache_key in alternative_paths_cache:
            return alternative_paths_cache[cache_key]

        alt_path = []
        curr_pos = self.current_position
        for key in path:
            alt_path.append(path_cache[(curr_pos, key)])
            curr_pos = key

        alternative_paths_cache[cache_key] = alt_path
        return alt_path

    def possible_paths(self):
        global path_cache

        if len(path_cache) > 0:
            return path_cache
        
        valid_paths_between_keys = {}

        # 1. All the possible directional key moves, eg from "^" to "A". There are 20, for 5 keys in pairs.
        source_target_keys_set = set(itertools.permutations(self.key_coordinates.keys(), 2))

        # 2. Now find the paths between the keys, similar logic to Numeric_Keyboard.move_to()
        for source_target_keys in source_target_keys_set:
            # first we have to find how to get to the target key, and for that we have to determine the possible valid paths
            vert_diff = self.key_coordinates[source_target_keys[1]][0] - self.key_coordinates[source_target_keys[0]][0]
            horz_diff = self.key_coordinates[source_target_keys[1]][1] - self.key_coordinates[source_target_keys[0]][1]

            needed_moves = ""
            if horz_diff > 0:
                needed_moves += horz_diff*">"
            else:
                needed_moves += abs(horz_diff)*"<"

            if vert_diff > 0:
                needed_moves += vert_diff*"v"
            else:
                needed_moves += abs(vert_diff)*"^"

            # this generates all possible paths from the source to the the target key
            possible_paths = set(itertools.permutations(needed_moves, len(needed_moves)))
            possible_paths = { "".join(path) for path in possible_paths }

            # now we have to check if the paths are valid, i.e. they don't go through location with no key
            invalid_paths = set()
            for path in possible_paths:
                curr_pos_row, curr_pos_col = self.key_coordinates[source_target_keys[0]]
                
                for move in path:
                    if move == ">":
                        curr_pos_col += 1
                    elif move == "<":
                        curr_pos_col -= 1
                    elif move == "v":
                        curr_pos_row += 1
                    elif move == "^":
                        curr_pos_row -= 1
                    
                    if curr_pos_row == 0 and curr_pos_col == 0:
                        # print(f"invalid numerical path: {path}")
                        invalid_paths.add(path)

            # and this allows us to finally determine the valid paths
            valid_paths_between_keys[source_target_keys] = list(possible_paths - set(invalid_paths))
            valid_paths_between_keys[source_target_keys] = [ path + "A" for path in valid_paths_between_keys[source_target_keys] ]

        valid_paths_between_keys[("^", "^")] = [ "A" ]
        valid_paths_between_keys[("<", "<")] = [ "A" ]
        valid_paths_between_keys[(">", ">")] = [ "A" ]
        valid_paths_between_keys[("v", "v")] = [ "A" ]
        valid_paths_between_keys[("A", "A")] = [ "A" ]
    
        path_cache = valid_paths_between_keys
        return valid_paths_between_keys

class HumanKeyboard:
    def __init__(self):
        self.count_moves = 0
        self.parent = None
    
    def lowest_cost_key_sequence(self, paths):
        return len(paths[0]), paths[0]

## part 1

start_time = time.time()
result = 0

# create the keyboard hierarchy
human_kbd = HumanKeyboard()

robot_kbds = []
kbd_above = human_kbd

for robot_num in range(25,0,-1):
    robot_kbds.insert(0, DirectionalKeyboard(f"Directional {robot_num}", kbd_above))
    kbd_above = robot_kbds[0]

path_cache = robot_kbds[0].possible_paths()
lcks_cache = {}

num_kbd = NumericKeyboard(robot_kbds[0])

# run the simulation
for line in lines:
    cost = 0
    multiplier = int(line[0:3])

    for key in line:
        step_cost, path = num_kbd.lowest_cost_of_move_to(key) 
        cost += step_cost
        # path = [x for xs in path for x in xs]
        # path = [x for xs in path for x in xs]
        # path = [x for xs in path for x in xs]
        # path = "".join(path)
        print(f" . Step cost for key {key} = {step_cost}") # don't print or it hangs!, path = {path}")

    print(f"Cost for line {line} = {cost}")
    result += multiplier * cost

print("Result part 1: ", result)  # 202274
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# see loop above -- just change to create 2 or 25 robots
# 245881705840972 in 0.0007 seconds
print("Result part 2: ", result)


