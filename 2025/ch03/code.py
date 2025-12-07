import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

## read data

## global variables

with open('ch03/input.txt') as f:
    lines = f.read().splitlines()

data = []
for line in lines:
    data.append([int(x) for x in list(line)])

# print(data)
## functions

## part 1

start_time = time.time()
result = 0

# for bank in data:
#     max_joltage = bank[0]*10 + bank[1]
#     for idx, bat1 in enumerate(bank[:-1]):
#         for idx2, bat2 in enumerate(bank[idx+1:]):
#             # print("Comparing: ", bat1, " with ", bat2)
#             joltage = bat1*10+bat2
#             if joltage > max_joltage:
#                 max_joltage = joltage
    
#     print("----- Max joltage for bank is ", max_joltage)
#     result += max_joltage

# second implementation
pattern_size = 2

for bank in data:
    current_pos = 0
    bank_max = 0
    digits_found = 0

    for n in range(pattern_size):
        highest = max(bank[current_pos:len(bank)-pattern_size+1+digits_found])
        if bank_max == 0:
            bank_max = highest
        else:
            bank_max = bank_max*10 + highest
        digits_found += 1

        # update the current position
        current_pos = bank.index(highest, current_pos) + 1

    result += bank_max

print("Result part 1: ", result) # 17432
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

pattern_size = 12

for bank in data:
    current_pos = 0
    bank_max = 0
    digits_found = 0

    for n in range(pattern_size):
        highest = max(bank[current_pos:len(bank)-pattern_size+1+digits_found])
        if bank_max == 0:
            bank_max = highest
        else:
            bank_max = bank_max*10 + highest
        digits_found += 1

        # update the current position
        current_pos = bank.index(highest, current_pos) + 1

    result += bank_max

print("Result part 2: ", result) # 173065202451341
print("--- %s seconds ---" % (time.time() - start_time))