import copy
import itertools
import math
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import random
import re
import sys
import time
from collections import deque, Counter
from tqdm import tqdm
from sympy import solve, Eq, linsolve, symbols, nonlinsolve
from sympy.parsing.sympy_parser import parse_expr
from sympy.abc import a, b


## read data

## global variables

with open('ch13/input.txt') as f:
    entries = f.read().split("\n\n")

## parse data

claw_machines = []

# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
regex_str = "Button A: X\+(\d+), Y\+(\d+)\sButton B: X\+(\d+), Y\+(\d+)\sPrize: X=(\d+), Y=(\d+)"
for entry in entries:
    claw_machines.append(tuple(map(int, re.findall(regex_str, entry)[0])))

## functions

## part 1

start_time = time.time()
result = 0

for claw_machine in claw_machines:
    butAX = claw_machine[0]
    butAY = claw_machine[1]
    butBX = claw_machine[2]
    butBY = claw_machine[3]
    targetX = claw_machine[4]
    targetY = claw_machine[5]

    eq_x = -targetX + a*butAX + b*butBX
    eq_y = -targetY + a*butAY + b*butBY
    
    # print(linsolve([eq_x, eq_y], (a,b)))
    solution = linsolve([eq_x, eq_y], (a,b))

    if len(solution) > 0: # if there is a solution
        sol_x = solution.args[0][0]
        sol_y = solution.args[0][1]
        
        if sol_x == int(sol_x) and sol_y == int(sol_y) and sol_x <= 100 and sol_y <= 100:
            result += int(sol_x*3 + sol_y*1)
            print(f"Press A {sol_x}, press B {sol_y}, Running cost is {result}")
        else:
            print(f"No solution -- {sol_x}, {sol_y}")

print("Result part 1: ", result) # 36250
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

for claw_machine in claw_machines:
    butAX = claw_machine[0]
    butAY = claw_machine[1]
    butBX = claw_machine[2]
    butBY = claw_machine[3]
    targetX = claw_machine[4]
    targetY = claw_machine[5]

    eq_x = -targetX-10000000000000 + a*butAX + b*butBX
    eq_y = -targetY-10000000000000 + a*butAY + b*butBY
    
    # print("   ", linsolve([eq_x, eq_y], (a,b)))
    solution = linsolve([eq_x, eq_y], (a,b))

    if len(solution) > 0: # if there is a solution
        sol_x = solution.args[0][0]
        sol_y = solution.args[0][1]
        
        if sol_x == int(sol_x) and sol_y == int(sol_y):
            result += int(sol_x*3 + sol_y*1)
            print(f"Press A {sol_x}, press B {sol_y}, Running cost is {result}")
        else:
            print(f"No solution -- {sol_x}, {sol_y}")

# 83232379451012
print("Result part 2: ", int(result)) #
print("--- %s seconds ---" % (time.time() - start_time))