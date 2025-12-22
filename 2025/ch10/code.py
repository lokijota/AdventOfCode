import sys
import time
# assuming jotalibrary.py is in the same directory / for the code to work we run the python from the top level directory
sys.path.append(".") 
from jotalibrary import *

import numpy as np
from collections import deque 
from scipy.optimize import linprog
# from itertools import groupby
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

with open('ch10/input.txt') as f:
    lines = f.read().splitlines()

## classes and functions
class Machine:
    def __init__(self, light_diagram, button_wirings, joltage_requirements):
        self.light_diagram = light_diagram
        self.button_wirings = button_wirings
        self.joltage_requirements = joltage_requirements

        self.indices_of_on_lights = [idx for idx, character in enumerate(self.light_diagram) if character == "#"]

        self.target_configuration = 0
        for idx in self.indices_of_on_lights:
            self.target_configuration |= (1<<idx)
        # print('{:b}'.format(self.target_configuration))

    @staticmethod
    def press(light_config, buttons):
        # print('{:b}'.format(light_config))
        for idx in buttons:
            light_config = light_config ^ (1 << idx)
        # print('{:b}'.format(light_config))
        return light_config

    def press_joltages(self, button_presses):
        lights = np.zeros(len(self.joltage_requirements), dtype=int)

        for idxbp, bp in enumerate(button_presses):
            for bw in self.button_wirings[idxbp]:
                lights[bw] += bp 

        # for idx in button_presses:
        #     current_joltages[idx] += 1
        return lights

manual = []
# [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
# The manual describes one machine per line. Each line contains a single indicator light diagram in [square brackets],
# one or more button wiring schematics in (parentheses), and joltage requirements in {curly braces}.
for line in lines:
    parts = line.split(" ")
    light_diagram = parts[0].removeprefix("[").removesuffix("]")
    button_wirings = [list(map(int, x.removeprefix("(").removesuffix(")").split(","))) for x in parts[1:len(parts)-1]]
    joltage_requirements = list(map(int, parts[-1].removeprefix("{").removesuffix("}").split(",")))
    
    manual.append(Machine(light_diagram, button_wirings,joltage_requirements))

## part 1

start_time = time.time()
result = 0

for machine in manual:
    bfs = deque()
    bfs.append([0, 0])
    # break # go to part 2

    while len(bfs)>0:
        head = bfs.popleft()
        for bw in machine.button_wirings:
            # print("Before: ", head[0], "will press:", bw, "target is", machine.target_configuration)
            val = Machine.press(head[0], bw)
            # print(" Pressed resulted in:", val)
            if val == machine.target_configuration:
                result += head[1] + 1
                print("  Found min presses for ", machine.light_diagram, ":", head[1]+1)
                bfs.clear()
                break
            else:
                bfs.append([val, head[1]+1])

print("Result part 1: ", result) # 530
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

# Using Simplex algorithm as per the code example here
# https://stackoverflow.com/questions/45873783/python-linprog-minimization-simplex-method
# And this example was useful to clarify how to use with equalities
# https://stackoverflow.com/questions/46702953/linear-programming-using-scipy-optimize-linprog-returns-suboptimal-solution?rq=3

for machine in manual:
    
    coefficient_matrix = np.zeros(shape=(len(machine.joltage_requirements), len(machine.button_wirings)) , dtype=int)

    for idxbw, bw in enumerate(machine.button_wirings):
        for button in bw:
            coefficient_matrix[button, idxbw] = 1

    # identity_matrix = np.eye(len(machine.button_wirings), dtype=int)
    # A_ub = np.concatenate((coefficient_matrix, identity_matrix))*-1
    # As the positiveness of y1 and y2 can be guaranteed under bounds=(0, None), we can remove the extra values
    A_ub = coefficient_matrix*-1
    # print(A_ub)

    # b_ub = np.array(machine.joltage_requirements + [0]*len(machine.button_wirings))*-1
    # As the positiveness of y1 and y2 can be guaranteed under bounds=(0, None), we can remove the extra values
    b_ub = np.array(machine.joltage_requirements)*-1
    # print(b_ub)

    c = np.ones(len(machine.button_wirings), dtype=int)
    # print(c)

    # optimize.linprog *always* minimizes your target function
    # important note: the line below uses equalities, in the equations, while the other one assumes >= and gives the wrong result
    res = linprog(c, A_eq = A_ub, b_eq = b_ub, integrality=3, bounds=(0, max(machine.joltage_requirements)))
    # res = linprog(c, A_ub, b_ub, integrality=3, bounds=(0, max(machine.joltage_requirements)))

    # simulate the button presses in each result, to compare
    joltages_after_presses = machine.press_joltages(res.x.astype(int))
    if (machine.joltage_requirements!=joltages_after_presses).any():

        # weirdly, simulating the button presses, gives the wrong result for 4 of the machines, eg:

        # Joltages:  [56, 74, 68, 51, 33, 39, 58, 48, 52, 69]
        #            [54 72 66 49 32 37 56 47 50 67]
        # Optimal value: 95 <-- this is number I'm adding to the result
        # Presses (X): [ 0  0  4 11 13 19  2 13  4 14 11  1  0] , Sum presses= 92 <- see how it gives 3 under the Optimal value returned!!
        # Success: True , Status: 0 , Message: Optimization terminated successfully. (HiGHS Status 7: Optimal)
        # N Iterations: 12

        print("--------\nJoltages: ", machine.joltage_requirements)
        print("          ", joltages_after_presses)
        print('Optimal value:', int(res.fun), '\nPresses (X):', res.x.astype(int), ", Sum presses=", sum(res.x.astype(int)))
        print("Success:", res.success, ", Status:", res.status, ", Message:", res.message)
        print("N Iterations:", res.nit)

    result += int(res.fun)

print("Result part 2: ", result)  # 20172
print("--- %s seconds ---" % (time.time() - start_time))