import copy
import itertools
import math
import matplotlib.pyplot as plt
import numpy as np
import random
import re
import sys
import time
from collections import deque, Counter
from tqdm import tqdm
# from operator import add, sub
# import networkx as nx
import schemdraw
from schemdraw import logic
from schemdraw.parsing import logicparse


## read data

with open('ch24/input.txt') as f:
    lines = f.read().split("\n\n")

## parse data

circuit = {}
variables = []
values_to_add_bin = {}
values_to_add_bin["x"] = []
values_to_add_bin["y"] = []
output_bits = 0

for inputs in lines[0].split("\n"):
    input_var, input_val = inputs.split(": ")
    circuit[input_var] = [int(input_val), "input", "noop", "noop"]
    values_to_add_bin[input_var[0]].insert(0, input_val) # added for part 2

for operations in lines[1].split("\n"):
    operation, output = operations.split(" -> ")
    operation = operation.split(" ")
    circuit[output] = [None, operation[1], operation[0], operation[2]]
    # added for part 2
    variables.append(output)
    if output.startswith("z") and int(output[1:]) > output_bits:
        output_bits = int(output[1:])


## functions and classes
loop_detector = dict()
calculation_loop_error = False

def calculate(var, circuit, depth=0):
    global calculation_loop_error

    # if var in loop_detector and depth > 20:
    if depth > 20:
        calculation_loop_error = True
        return 0
    
    # loop_detector[var] = True
    if circuit[var][0] is not None:
        return circuit[var][0]
    
    depth += 1
    if circuit[var][1] == "AND":
        circuit[var][0] = calculate(circuit[var][2], circuit, depth) & calculate(circuit[var][3], circuit, depth)
        return circuit[var][0]

    if circuit[var][1] == "XOR":
        circuit[var][0] = calculate(circuit[var][2], circuit, depth) ^ calculate(circuit[var][3], circuit, depth)
        return circuit[var][0]

    circuit[var][0] = calculate(circuit[var][2], circuit, depth) | calculate(circuit[var][3], circuit, depth)
    return circuit[var][0]

def trace_dependencies_variable(circuit, variable, only_inputs = True):
    deps = [] # set()

    if variable.startswith("x") or variable.startswith("y"):
        deps.append(variable)
    else:
        if only_inputs == False:
            deps.extend([circuit[variable][2], circuit[variable][2]])

        deps.extend(trace_dependencies_variable(circuit, circuit[variable][2]))
        deps.extend(trace_dependencies_variable(circuit, circuit[variable][3]))

    return deps

def trace_dependencies(circuit, output_variables):
    dependencies = {}

    for output_var in output_variables:
        if output_var.startswith("z"):
            dependencies[output_var] = trace_dependencies_variable(circuit, output_var)

    return dependencies

def find_incorrect_dependencies(output_var_deps):
    bad_dependencies = {}

    for output_var_dep in output_var_deps.keys():
        bit_nb = int(output_var_dep[1:])

        # the output of bit N must read from both x[N..0] and y[N..0] inputs (all of them)
        for src_bit_nb in range(bit_nb, -1, -1):
            src_bit_nb_str = f'{src_bit_nb:02}'

            # z45 is a final carry over, there is no x45/y45
            if bit_nb == 45 and src_bit_nb == 45:
                continue

            if "x" + src_bit_nb_str not in output_var_deps[output_var_dep] or "y" + src_bit_nb_str not in output_var_deps[output_var_dep]:
                bad_dependencies[output_var_dep] = set()
                break

        # are we reading from bits higher up in the source?
        for dep_input in output_var_deps[output_var_dep]:
            dep_bit_nb = int(dep_input[1:])

            if dep_bit_nb > bit_nb:
                if output_var_dep not in bad_dependencies:
                    bad_dependencies[output_var_dep] = set()
                bad_dependencies[output_var_dep].add(dep_input)

    return bad_dependencies

def count_frequencies(circuit):

    frequencies = {}
    for k,v in circuit.items():
        if k not in frequencies:
            frequencies[k] = [1, 0] # 1 output, 0 inputs
        else:
            frequencies[k] = [ frequencies[k][0]+1, frequencies[k][1] ]

        if v[1] == "input":
            continue

        left_gate = v[2]
        right_gate = v[3]

        if left_gate not in frequencies:
            frequencies[left_gate] = [0,1]
        else:
            frequencies[left_gate] = [ frequencies[left_gate][0], frequencies[left_gate][1]+1 ]

        if right_gate not in frequencies:
            frequencies[right_gate] = [0,1]
        else:
            frequencies[right_gate] = [ frequencies[right_gate][0], frequencies[right_gate][1]+1 ]


    return frequencies

def get_logic_expression(circuit, gate):

    if gate.startswith("x") or gate.startswith("y"):
        return gate
    
    else:
        return f"({get_logic_expression(circuit, circuit[gate][2])} {circuit[gate][1]} {get_logic_expression(circuit, circuit[gate][3])})" 


## part 1

start_time = time.time()
result = 0

start_var = 0
values = []
while True:
    current_var = f'z{start_var:02}'
    if current_var not in circuit:
        break

    values.insert(0, calculate(current_var, circuit))
    start_var += 1

result = "".join([str(x) for x in values])
result = int(result, 2)

print("Result part 1: ", result) # 59364044286798 in 0.00012 seconds
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0

circuit["z07"], circuit["gmt"] = circuit["gmt"], circuit["z07"] # fixes error in z07/z08
circuit["qjj"], circuit["cbj"] = circuit["cbj"], circuit["qjj"] # fixes error in z11/z12
circuit["z18"], circuit["dmn"] = circuit["dmn"], circuit["z18"] # fixes error in z18/z19
circuit["z35"], circuit["cfk"] = circuit["cfk"], circuit["z35"] # fixes error in z18/z19

# response for part 2:
# cbj,cfk,dmn,gmt,qjj,z07,z18,z35

def fill_structure(circuit: dict, structure: dict, gate_name: str, depth = 0):
    # build a structure by level to make it easier to verify
    if gate_name.startswith("x") or gate_name.startswith("y"):
        return

    if depth == len(structure):
        structure[depth] = [(f"{depth}", "too many gates")]

    current_gate = circuit[gate_name]
    structure[depth].append((current_gate[1], current_gate[2], current_gate[3], "-> " + gate_name))
    structure[depth].sort(key=lambda tup: tup[0]) # just to simplify the testing

    fill_structure(circuit, structure, current_gate[2], depth+1)
    fill_structure(circuit, structure, current_gate[3], depth+1)

def check_structure(structure, output_var_num):
    circuit_errors = []

    for j in range(0, len(structure)):

        if len(structure[j]) == 0:
            circuit_errors.append((j, "missing"))
            continue

        if j == 0:
            if structure[j][0][0] != "XOR":
                circuit_errors.append((j, structure[j][0], "expected XOR"))
            
            if len(structure[j]) > 1:
                circuit_errors.append((f"{j}", f"too many gates at this level: {len(structure)}, expected 1" ))
            
        elif j == len(structure)-1:
            if structure[j][0][0] != "AND":
                circuit_errors.append((j, structure[j][0], "expected AND"))
            if structure[j][1][0] != "XOR":
                circuit_errors.append((j, structure[j][1], "expected XOR"))

            if len(structure[j]) > 2:
              circuit_errors.append((f"{j}", f"too many gates at this level: {len(structure)}, expected 2"))
        elif j%2 == 1:
            if structure[j][0][0] != "OR":
                circuit_errors.append((j, structure[j][0], "expected OR"))
            if structure[j][1][0] != "XOR":
                circuit_errors.append((j, structure[j][1], f"expected XOR({output_var_num-int(j/2)})"))

            if len(structure[j]) > 2:
              circuit_errors.append((f"{j}", f"too many gates at this level: {len(structure)}, expected 2"))
        else:
            if structure[j][0][0] != "AND":
                circuit_errors.append((j, structure[j][0], f"expected AND({output_var_num-int(j/2)})"))
            if structure[j][1][0] != "AND":
                circuit_errors.append((j, structure[j][1], f"expected AND({output_var_num-int(j/2)})"))
            
            if len(structure[j]) > 2:
                circuit_errors.append((f"{j}", f"too many gates at this level: {len(structure)}, expected 2"))

    # return what's wrong
    return circuit_errors


# build a dictionary that for each depth (where 0 is the level of the source), 
# has the gates at that level (and names of gates)
bad_outputs = []
all_errors = dict()
for output_var_num in range(35, 45): # note: 45 has a different structure as there's no input xy45
    structure = dict()

    # initialize placeholder for outputs
    for init_index in range(0, output_var_num*2):
        structure[init_index] = list()

    output_node_name = f'z{output_var_num:02}'
    fill_structure(circuit, structure, output_node_name)
    # print(structure)

    # now check if this structure is well built
    errors =  check_structure(structure, output_var_num)
    print(errors)
    all_errors[output_var_num] = errors

    if len(errors) > 0:
        bad_outputs.append(output_var_num)

print(f"Wrongly constructed outputs: {len(bad_outputs)}, {bad_outputs}")


# even with the increased recursion limit, the code hangs at z12, z13 in the logicparse()
# but this helped in earlier stages to understand the structure and identify the first two errors
sys.setrecursionlimit(10000)
for n in range(0, 46):
    output_node_name = f'z{n:02}'

    with schemdraw.Drawing() as drawing:
        
        the_expression = get_logic_expression(circuit, output_node_name).lower()
        logicparse(f"{the_expression}", outlabel=output_node_name)

with schemdraw.Drawing():
    for k,v in circuit.items():
        if not k.startswith("z"):
            continue
    
        the_expression = get_logic_expression(circuit, k)

        logicparse(f"{the_expression}", outlabel=k)

result = "cbj,cfk,dmn,gmt,qjj,z07,z18,z35"
print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))


