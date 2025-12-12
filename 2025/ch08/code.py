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
# import numpy as np
## read data

## global variables

with open('ch08/input.txt') as f:
    lines = f.read().splitlines()

coords = [np.array([int(x[0]), int(x[1]), int(x[2])]) for x in [lin.split(",") for lin in lines]]

## functions

## part 1

start_time = time.time()
result = 0

distance_matrix = dict()

for c1 in coords:
    for c2 in coords:
       key=str(c1[0])+str(c1[1])+str(c1[2]) + str(c2[0])+str(c2[1])+str(c2[2])
       dist =np.linalg.norm(c1-c2)  
       if dist != 0.0:
           distance_matrix[key] = dist
       # distance_matrix[str(c1)+str(c2)] = np.linalg.norm(c1-c2) 
       # numpy.sqrt(numpy.sum((a - b) ** 2, axis=1))

for distance in distance_matrix.keys():
    if distance_matrix[distance] == 0.0:
        del distance_matrix[distance] 

print(min(distance_matrix.values()))


print("Result part 1: ", result) # 
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0



print("Result part 2: ", result)  # 
print("--- %s seconds ---" % (time.time() - start_time))