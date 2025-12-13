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

with open('ch09/sample.txt') as f:
    lines = f.read().splitlines()


## functions


## part 1

start_time = time.time()
result = 0



print("Result part 1: ", result) # 163548
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0


 
print("Result part 2: ", result)  #772452514 
print("--- %s seconds ---" % (time.time() - start_time))