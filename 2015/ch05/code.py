import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

import hashlib
# from itertools import batched
# from itertools import groupby
# import numpy as np
# from collections import deque 
# import math
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

with open('ch05/input.txt') as f:
    lines = f.read().splitlines()

## functions


## part 1

start_time = time.time()
result = 0

# It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
# It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
# It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.

for line in lines:
    # the code is all on gh copilot...
    vowel_count = sum(1 for c in line if c in 'aeiou')
    has_double = any(line[i] == line[i+1] for i in range(len(line)-1))
    has_forbidden = any(sub in line for sub in ['ab', 'cd', 'pq', 'xy'])

    if vowel_count >= 3 and has_double and not has_forbidden:
        result += 1


print("Result part 1: ", result) # 
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

for line in lines:
    # the code is all on gh copilot...
    has_repeated = any((line[i]+line[i+1]) in line[i+2:] for i in range(len(line)-2))
    has_double = any(line[i] == line[i+2] for i in range(len(line)-2))

    if has_repeated and has_double:
        print(line)
        result += 1

print("Result part 2: ", result)  # 51
print("--- %s seconds ---" % (time.time() - start_time))
