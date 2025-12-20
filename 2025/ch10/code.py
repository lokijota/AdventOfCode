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

with open('ch10/sample.txt') as f:
    lines = f.read().splitlines()

manual = dict()
# [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
# The manual describes one machine per line. Each line contains a single indicator light diagram in [square brackets],
# one or more button wiring schematics in (parentheses), and joltage requirements in {curly braces}.
for line in lines:
    parts = line.split(" ")
    light_diagram = parts[0].removeprefix("[").removesuffix("]")
    button_wirings = [list(map(int, x.removeprefix("(").removesuffix(")").split(","))) for x in parts[1:len(parts)-1]]
    joltage_requirements = list(map(int, parts[-1].removeprefix("{").removesuffix("}").split(",")))
    manual[light_diagram] = [button_wirings, joltage_requirements]

## functions


## part 1

start_time = time.time()
result = 0


print("Result part 1: ", result) # 
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0



print("Result part 2: ", result)  # 
print("--- %s seconds ---" % (time.time() - start_time))
