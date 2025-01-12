# Part 2

*NOTE** 

Ended up solving this by visual inspection of the results, with some graphs to help, and some code to identify likely errors based on the structure.

 Looking at the largest correct sequence we have, z06, starting from the end to the beggining:
    - Level 0 has
        - 1 XOR
    - Level 1
        - XOR from the source variables x/y06
        - OR (of two ANDs)
    - Level 2 has:
        - 2 AND (one of them, of variables x/y05)
    - Level 3 has:
        - XOR from the variables x/y05
        - OR (of two AND)
    - Level 4:
        2 AND (one of them, of variables x/y04)
    - ...
    - Level 11
        - 1 XOR (of x/y01)
        - 1 AND (of x/y00)

In other words:
- Starts with a XOR 
- depois tem sequências que repetem aos pares (XOR/OR seguido de AND/AND)
- acaba com xor/and


For the sequence z06:
- the depth is 9
- The pattern is the same


Depth:
- z00: 1
- z01: 2
- z02: 4
- z03: 6
- z04: 8
- z05: 10
- z06: 12 

TBD: add the images as screenshots to explain

## Other notes:

- The outputs zXX are not reentrant, i.e., they are not inputs to anything else
- To correctly calculate output bit zNN, that bit has to depend on all input bits x00-xNN and y00-xNN
- Bit z07 depends only on 3x y07 and 1x x07. It should be possible to find all nodes that depend on both x00-x06 and y00-y06 in a redundant way
    - How to define "redundant" here? What to look for exactly?
    - It has to be something that can be be re-wired to fix this z07 output. But it may break others.

- x00-x44 and y00-y44 have all the same structure: 1 output, and used twice as inputs. The inputs are ALWAYS:
    - xNN AND yNN -> something + xNN XOR yNN -> something
    - A visual representation may yeld the answer! Or using substitutions and building the expression.
- zNN are always only and output, and are not reentrant
- of the remaining gates (intermediate), 88 are used once as input to other shape gate, and the other 88 are used twice as inputs. Interesting that there are 45 input values (eg x00 to x44) and two variables (x and y), which makes sense.

-