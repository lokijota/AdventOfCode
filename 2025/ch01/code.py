import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

## read data

## global variables

with open('ch01/input.txt') as f:
    lines = f.read().splitlines()

data = lines

print(data)
## functions

## part 1

start_time = time.time()
result = 0

current_pos = 50
cross_zero_count = 0

for rotation in data:
    if rotation[0] == 'L':
        current_pos -= int(rotation[1:]) 
    else:
        current_pos += int(rotation[1:])

    current_pos = current_pos % 100
    if current_pos == 0:
        cross_zero_count += 1

result = cross_zero_count

print("Result part 1: ", result) # 962
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

current_pos = 50
cross_zero_count = 0

for rotation in data:
    clicks = int(rotation[1:])
    cross_zero_count += clicks//100 # floor division to count full circles
    clicks = clicks % 100 # remaining clicks after full circles

    prev_pos = current_pos

    if rotation[0] == 'L':
        current_pos -= clicks 
    else:
        current_pos += clicks
    
    if prev_pos != 0:
        if current_pos <= 0 or current_pos >= 100:
            cross_zero_count += 1

    current_pos = current_pos % 100

result = cross_zero_count

print("Result part 2: ", result) # 5782
print("--- %s seconds ---" % (time.time() - start_time))