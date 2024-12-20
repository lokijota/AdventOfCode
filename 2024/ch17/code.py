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
# from collections import deque, Counter
# from tqdm import tqdm
# from operator import add, sub
# import networkx as nx

## read data

## global variables

with open('ch17/input.txt') as f:
    lines = f.read().splitlines()

## parse data

register_a = int(lines[0].split(": ")[1])
register_b = int(lines[1].split(": ")[1])
register_c = int(lines[2].split(": ")[1])
bytecode = [int(instruction) for instruction in lines[4].split(": ")[1].split(",")]

## functions and classes
    
class ChronospacialComputer:
    """ My first class im this year's AoC. It's a been a while, my old friend. """
    def __init__(self, register_a, register_b, register_c):
        self.a = register_a
        self.b = register_b
        self.c = register_c
        self.ip = 0
        self.last_output = []
        self.last_program = []
    
    def __str__(self):
        separator = ', ' 
        return separator.join(map(str, self.last_output)) 

    def combo_operand(self, operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.a
        elif operand == 5:
            return self.b
        elif operand == 6:
            return self.c

    def run(self, program):
        self.last_program = program

        while self.ip < len(program):

            match program[self.ip]:
                case 0:
                    self.a = int(self.a / pow(2, self.combo_operand(program[self.ip+1])))
                    self.ip += 2
                case 1:
                    self.b = self.b ^ program[self.ip+1]
                    self.ip += 2
                case 2:
                    self.b = self.combo_operand(program[self.ip+1]) % 8
                    self.ip += 2
                case 3:
                    if self.a != 0:
                        self.ip = program[self.ip+1]
                    else:
                        self.ip += 2
                case 4:
                    self.b = self.b ^ self.c 
                    self.ip += 2
                case 5:
                    self.last_output.append(self.combo_operand(program[self.ip+1])%8)
                    self.ip += 2
                case 6:
                    self.b = int(self.a / pow(2, self.combo_operand(program[self.ip+1])))
                    self.ip += 2
                case 7:
                    self.c = int(self.a / pow(2, self.combo_operand(program[self.ip+1])))
                    self.ip += 2

        return self.last_output



## part 1

start_time = time.time()
result = 0

prog = ChronospacialComputer(register_a, register_b, register_c)
output = prog.run(bytecode)
print("Output: ", output)
result = len(output)


print("Result part 1: ", result)  # 7,3,0,5,7,1,4,0,5
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

print("Result part 2: ", int(result)) 
print("--- %s seconds ---" % (time.time() - start_time))