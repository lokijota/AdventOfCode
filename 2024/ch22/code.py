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

with open('ch22/input.txt') as f:
    lines = f.read().splitlines()

## parse data

## functions and classes

def random_number_generator(seed):
    nb = ((seed*64)^seed) % 16777216
    nb = int(nb/32)^nb
    nb = ((nb*2048)^nb)%16777216
    return nb

## part 1

start_time = time.time()
result = 0

for random_nb in lines:
    random_nb = int(random_nb)

    for _ in range(0, 2000):
        random_nb = random_number_generator(random_nb)

    result += random_nb

print("Result part 1: ", result) # 13584398738
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# trying to have everything pre-calculated

# 1. this code calculates a list of lists of last digits
random_numbers_sequences = []

for random_nb in lines:
    random_nb = int(random_nb)
    sequence_2000 = []
    sequence_2000.append(random_nb%10)

    for j in range(0, 2000):
        random_nb = random_number_generator(random_nb)
        sequence_2000.append(random_nb%10)

    random_numbers_sequences.append(sequence_2000)

# 2. this code calculates the deltas between the last digits for each of the sequences in the lists
# stores them as strings for convenience in the next step

deltas = []
for sequence in random_numbers_sequences:
    sequence_deltas = []
    for j in range(1, 2001):
        delta = sequence[j] - sequence[j-1]
        sequence_deltas.append(str(delta))
    deltas.append(sequence_deltas)

# 3. now feed the cache: dictionaries with the sequences of 4 and the respective add value
cache_list = []

for seq_idx, sequence in enumerate(deltas):
    sequence_4_deltas = {}

    for j in range(3, 2000):
        cache_key = sequence[j-3] + "." + sequence[j-2] + "." + sequence[j-1] + "." + sequence[j]
        if cache_key not in sequence_4_deltas:
            sequence_4_deltas[cache_key] = random_numbers_sequences[seq_idx][j+1]
        
    cache_list.append(sequence_4_deltas)

# 4. finally calculate the result

the_cache = dict()
last_idx_added = dict() # flag to not let add the same cache key (sequence of deltas) multiple times per sequence

for seq_idx, sequence in enumerate(deltas):

    found_in_sequence = []
    for j in range(3, 2000):
        cache_key = sequence[j-3] + "." + sequence[j-2] + "." + sequence[j-1] + "." + sequence[j]

        if cache_key not in last_idx_added or seq_idx != last_idx_added[cache_key]:
            if cache_key not in the_cache:
                the_cache[cache_key] = random_numbers_sequences[seq_idx][j+1]
            else:
                the_cache[cache_key] += random_numbers_sequences[seq_idx][j+1]
            last_idx_added[cache_key] = seq_idx

max = 0
for key in the_cache.keys():
    if the_cache[key] > max:
        max = the_cache[key]
        best_key = key

print(f"Best sequence is {best_key}, with worth {max}")


# Cheeky! Below: as a missing sequence is worth 0, it turns out that the best-valued sequence is not in the first list.
# So ended up going brute-forcing it. I'm sure there's better ways, for example calculating the sequences as we go along,
# instead of building the hashmaps and then going through them.

# best_sequence = 0
# best_sequence_key = 0
# for key in cache_list[0].keys():

#     this_sequence = cache_list[0][key]
#     for sequence in cache_list[1:]:
#         if key in sequence:
#             this_sequence += sequence[key]
    
#     if this_sequence > best_sequence:
#         best_sequence = this_sequence
#         best_sequence_key = key
    # print(f"Sequence {key} has worth {this_sequence}")            

# ok, so this is the brute force approach, but above I found a better method that avoids this
# best_sequence = 0
# best_sequence_key = 0

# for i0 in range(-10,11):
#     for i1 in range(-10,11):
#         for i2 in range(-10,11):
#             for i3 in range(-10,11):

#                 this_sequence = 0
#                 key = str(i0) + "." + str(i1) + "." + str(i2) + "." + str(i3) 
#                 for sequence in cache_list:
#                     if key in sequence:
#                         this_sequence += sequence[key]
            
#                 if this_sequence > best_sequence:
#                     best_sequence = this_sequence
#                     best_sequence_key = key
#                     print(f"(new best) Sequence {key} has worth {this_sequence}")  

result = max

# With Brute force solution: Result part 2:  1612, best sequence is 2.-1.-1.2, found in 80.4 seconds ---
# With the current solution where I avoid going over the dictionaries multiple times, found in 4.4 seconds ---

print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))


