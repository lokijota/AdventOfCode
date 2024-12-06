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
from itertools import pairwise
import math

## read data

## global variables

with open('ch05/input.txt') as f:
    lines = f.read().splitlines()

## parse data

rules = set()
pages = []

parsing_rules = True

for line in lines:

    if parsing_rules == False:
        pages.append([int(el) for el in line.split(",")])
        continue

    if len(line) == 0:
        parsing_rules = False
        continue

    parts = line.split("|")
    rules.add( (int(parts[0]), int(parts[1]) ))

## functions


## part 1

start_time = time.time()
result = 0

part2_unordered = []

for page in pages:

    correctly_ordered = True
    for pair in pairwise(page):
        # print(pair)

        if not pair in rules:
            correctly_ordered = False
            break

    if correctly_ordered == True:
        result += page[int(len(page)/2)]
        # print(f"Adding {page[int(len(page)/2)]}")
    else:
        part2_unordered.append(page)


print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# process the part2_unordered list here

random.seed()
for unordered in part2_unordered:

   # print(unordered)

   correctly_ordered = False 
   while correctly_ordered == False:
       # print(unordered)

       correctly_ordered = True
       for pair in pairwise(unordered):
            if not pair in rules:
                correctly_ordered = False
                # print("wrong: ", pair)

                if (pair[1], pair[0]) in rules:
                    # trocar os elementos e tentar de novo
                    del unordered[unordered.index(pair[1])]
                    unordered.insert( unordered.index(pair[0]), pair[1])
                    # print(f"Replaced to {unordered}")
                break

       # input("prima uma chave")

   result += unordered[int(len(unordered)/2)]
   # print(f"Unordered now ordered: Adding {unordered[int(len(unordered)/2)]}")


print("Result part 2: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))