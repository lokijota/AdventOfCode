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

with open('ch04/input.txt') as f:
    lines = f.read().splitlines()

## functions


## part 1

start_time = time.time()
result = 0

result = 1

while True:
    s = "iwrupvqb" + str(result)
    res = hashlib.md5(s.encode())

    if res.hexdigest().startswith("00000"):
        print(f"Solution is {result}")
        print(res.hexdigest())
        break

    result += 1

print("Result part 1: ", result) # 346386
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

result = 1

while True:
    s = "iwrupvqb" + str(result)
    res = hashlib.md5(s.encode())

    if res.hexdigest().startswith("000000"):
        print(f"Solution is {result}")
        print(res.hexdigest())
        break

    result += 1

print("Result part 2: ", result)  # 9958218
print("--- %s seconds ---" % (time.time() - start_time))
