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
    
    def reset(self, register_a, register_b, register_c):
        self.a = register_a
        self.b = register_b
        self.c = register_c
        self.ip = 0
        self.last_output = [ ]
    
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
        # formulas = []
        # current_formula = ""

        digit = 0

        while self.ip < len(program):

            # heuristic
            # if len(self.last_output) > 16:
            #     break

            match program[self.ip]:
                case 0:

                    # current_formula += f"0: a = int({self.a} / pow(2, {self.combo_operand(program[self.ip+1])})); \n"
                    self.a = int(self.a / pow(2, self.combo_operand(program[self.ip+1])))
                    # current_formula += f"  a={self.a}, b={self.b}, c={self.c}; \n"
                    self.ip += 2
                case 1:
                    # current_formula += f"1: b = {self.b} ^ {program[self.ip+1]}; \n"
                    self.b = self.b ^ program[self.ip+1]
                    # current_formula += f"  a={self.a}, b={self.b}, c={self.c}; \n"
                    self.ip += 2
                case 2:
                    # current_formula += f"2: b = {self.combo_operand(program[self.ip+1])} % 8; \n"
                    self.b = self.combo_operand(program[self.ip+1]) % 8
                    # current_formula += f"  a={self.a}, b={self.b}, c={self.c}; \n"
                    self.ip += 2
                case 3:
                    if self.a != 0:
                        # current_formula += f"3: ip = {program[self.ip+1]}; \n"
                        self.ip = program[self.ip+1]
                    else:
                        self.ip += 2
                case 4:
                    # current_formula += f"4: b = {self.b} ^ {self.c}; \n"
                    self.b = self.b ^ self.c 
                    # current_formula += f"  a={self.a}, b={self.b}, c={self.c}; \n"
                    self.ip += 2
                case 5:
                    # current_formula += f"print: {self.combo_operand(program[self.ip+1])} % 8; \n"
                    # current_formula += f"  a={self.a}, b={self.b}, c={self.c}; \n"
                    # formulas.append(current_formula)
                    # current_formula = ""
                    self.last_output.append(self.combo_operand(program[self.ip+1])%8)

                    # optimize for part 2
                    # if self.last_output[-1] != program[digit]:
                    #     return self.last_output 
                    digit += 1


                    self.ip += 2
                case 6:
                    # current_formula += f"6: b = int({self.a} / pow(2, {self.combo_operand(program[self.ip+1])})); \n"
                    self.b = int(self.a / pow(2, self.combo_operand(program[self.ip+1])))
                    # current_formula += f"  a={self.a}, b={self.b}, c={self.c}; \n"
                    self.ip += 2
                case 7:
                    # current_formula += f"7: c = int({self.a} / pow(2, {self.combo_operand(program[self.ip+1])})); \n"
                    self.c = int(self.a / pow(2, self.combo_operand(program[self.ip+1])))
                    # current_formula += f"  a={self.a}, b={self.b}, c={self.c}; \n"
                    self.ip += 2

        return self.last_output #, formulasp

        
    def run_opt(self, program, at_digit, expected_value):
        digit = 0

        while self.ip < len(program):

            # heuristic
            # if len(self.last_output) > 16:
            #     break

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
                    val = self.combo_operand(program[self.ip+1])%8

                    # optimize for part 2
                    if digit == at_digit and val != expected_value:
                        # end calculation
                        return self.last_output 

                    # self.last_output.append(self.combo_operand(program[self.ip+1])%8)
                    self.last_output.append(val)

                    digit += 1
                    self.ip += 2
                case 6:
                    self.b = int(self.a / pow(2, self.combo_operand(program[self.ip+1])))
                    self.ip += 2
                case 7:
                    self.c = int(self.a / pow(2, self.combo_operand(program[self.ip+1])))
                    self.ip += 2

        return self.last_output #, formulasp

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

prog = ChronospacialComputer(register_a, register_b, register_c)

# 35184372088832 is when the outputs start having 16 digits. determined by knowing the formula 8^n
# JOTATODO: ^ explain how I got to this formula
prev_output = []
count_pos = list(np.zeros(16, dtype=int))
sequences_per_digit_pos = dict()

steps_per_sequence_digit = dict()

for j in range(0,16):
    sequences_per_digit_pos[j] = [1]

    steps_per_sequence_digit[j] = pow(8,j) 
    # note: first sequence-digit change is 8^j * 2, subsequent ones are 8^j

#limits for 16-17 digits, between 8^15 and 8^16
# lower_bound =  35184372088832
# upper_bound = 281474976710656

lower_bound = 0
upper_bound = 316659348799487
ranges_to_explore = deque()
ranges_to_explore.append([lower_bound, upper_bound])

found = False
current_digit = 15

while not found:

    ranges_q = deque()
    while len(ranges_to_explore) > 0:

        rte = ranges_to_explore.popleft()
        lower_bound = rte[0]
        upper_bound = rte[0]
        
        # divide the space in spans
        for r in range(0,8*8):
            if r == 0:
                span = [lower_bound, lower_bound + steps_per_sequence_digit[current_digit-1]*2-1]
            else:
                span = [lower_bound + steps_per_sequence_digit[current_digit-1]*2 + steps_per_sequence_digit[current_digit-1]*(r-1), \
                        lower_bound + steps_per_sequence_digit[current_digit-1]*2 + steps_per_sequence_digit[current_digit-1]*r-1]

            ranges_q.append(span)

    print(f"Ranges generated: {len(ranges_q)}, matches from this onward: {current_digit}, elapsed: {time.time() - start_time}")

    # now calculate and see the output, for each of the ranges
    while len(ranges_q) > 0:
        r = ranges_q.popleft()
        prog.reset(r[0], register_b, register_c)
        output = prog.run(bytecode) #, current_digit, bytecode[current_digit])
        
        if len(output) != 16:
            continue

        if output[current_digit:] == bytecode[current_digit:]: # and output_u[current_digit:] == bytecode[current_digit:]:
            # lower_bound = r[0]
            # upper_bound = r[1]
            ranges_to_explore.append([r[0], r[1]])

            # print(f"Match from character {current_digit}: {output}, a = {r[0]}")

            # if current_digit == 0:
            #     print(f"Found it: a = {r[0]}")
            #     found = True
            #     break

    if len(ranges_to_explore) > 0:
        current_digit -= 1
    else:
        print("WOOOPS NOTHING FOUND")

    # if we're already looking at the last 4 digits let's do it a different way and check ALL of them
    if current_digit == 4:
        while len(ranges_to_explore) > 0:
            rte = ranges_to_explore.popleft()
            # lower_bound = rte[0]
            # upper_bound = rte[0]

            for j in range(rte[0], rte[1]+1):
                prog.reset(j, register_b, register_c)
                output = prog.run_opt(bytecode, 0, 2)
        
                if output == bytecode:
                    result = j
                    print("Found it: a=", j)
                    print("Result part 2: ", result) 
                    print("--- %s seconds ---" % (time.time() - start_time))
                    break
                    input("Press any key to make coffee...")
        
                # if len(output) != 16:
                    # continue

    print("   Matching ranges:", len(ranges_to_explore))


# 202972175280682
print("Result part 2: ", int(result)) 
print("--- %s seconds ---" % (time.time() - start_time))