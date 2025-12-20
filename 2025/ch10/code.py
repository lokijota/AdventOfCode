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

with open('ch10/input.txt') as f:
    lines = f.read().splitlines()

## classes and functions
class Machine:
    def __init__(self, light_diagram, button_wirings, joltage_requirements):
        self.light_diagram = light_diagram
        self.button_wirings = button_wirings
        self.joltage_requirements = joltage_requirements

        self.indices_of_on_lights = [idx for idx, character in enumerate(self.light_diagram) if character == "#"]

        # def set_bit(value, bit):
        #     return value | (1<<bit)
        # def clear_bit(value, bit):
        #     return value & ~(1<<bit)
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

print("Result part 1: ", result) # 
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0



print("Result part 2: ", result)  # 
print("--- %s seconds ---" % (time.time() - start_time))
