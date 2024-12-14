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

## read data

## global variables

with open('ch14/input.txt') as f:
    lines = f.read().splitlines()

## parse data
robots = []
for robot in lines:
    position, velocity = robot.removeprefix("p=").split(" v=")
    px, py = position.split(",")
    vx, vy = velocity.split(",")

    robots.append((int(px),int(py),int(vx),int(vy)))

## functions

def count_and_print(robots, print_map):
    map = np.zeros((height, width), dtype=int)

    for robot in robots:
        map[robot[1], robot[0]] += 1

    if print_map == True:
        with np.printoptions(threshold=np.inf, linewidth=np.inf):
            for rows in map:
                for cols in rows:
                    if cols > 0:
                        print("#", end="")
                    else:
                        print(" ", end="")
                print()

        #  print(map)
    # print(f"# Robots: {sum(sum(map))}")

    count_top_left = np.sum(map[0:int(height/2), 0:int(width/2)])
    count_top_right = np.sum(map[0:int(height/2), int(width/2)+1:]) 

    count_bottom_left  = np.sum(map[int(height/2)+1:, 0:int(width/2)])
    count_botton_right = np.sum(map[int(height/2)+1:, int(width/2)+1:]) 

    return count_top_left, count_top_right, count_bottom_left, count_botton_right

## part 1

start_time = time.time()
result = 0

# Predict the motion of the robots in your list within a space which is 101 tiles wide and 103 tiles tall.
# What will the safety factor be after exactly 100 seconds have elapsed?
width = 101 #11
height = 103 #7
n_seconds = 100

moved_robots = []

for robot in robots:
    px, py, vx, vy = robot
    target_x = (px + vx*n_seconds)%width
    target_y = (py + vy*n_seconds)%height

    moved_robots.append((target_x, target_y))

result = math.prod(count_and_print(moved_robots, False))
 
print("Result part 1: ", result) # 211692000
print("--- %s seconds ---" % (time.time() - start_time))

## part 2

start_time = time.time()
result = 0
min_safety = 211692000 # solution of previous one

for n_seconds in range(1, 10000):
    # print(f"Seconds:{n_seconds} ")

    moved_robots = []
    for robot in robots:
        px, py, vx, vy = robot
        target_x = (px + vx*n_seconds)%width
        target_y = (py + vy*n_seconds)%height

        moved_robots.append((target_x, target_y))

    safety = math.prod(count_and_print(moved_robots, False))
    if safety < min_safety:
        min_safety = safety
        result = n_seconds
        count_and_print(moved_robots, True)
        # input(f"press key after {n_seconds}, min={min_safety}")

# This can be solved with math with the Chinese Remainder Theorem:
# https://youtu.be/MdePzlQtnCc

# 6587
print("Result part 2: ", int(result)) #
print("--- %s seconds ---" % (time.time() - start_time))