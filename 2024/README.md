# Advent Of Code 2024

Coding in Python 3.1, in VSCode with Vim (decided to go back to Uni days, because why not)

- *Day 01*: simple challenge, more of a warm-up
- *Day 02*: first part simple, second part just thinking of edge cases confused me. Not pretty code but works.
- *Day 03*: simple challenge with regex
- *Day 04*: counting XMAS/MAS in a map. First part done in a non-smart but still quick way
- *Day 05*: first part very simple, used sets and pairwise. Second part slightly harder but the first naïve implementation of just swapping order worked well and is very fast. Unexpected.
- *Day 06*: this is the one with the guard walking around a map and finding loops. Second part runs in 8 secs, I'm sure it could be much faster.
- *Day 07*: this is the one where there's a variable number of loops. The second part takes 16 seconds which is too long. I used an `itertools.product` to generate combinations and then just did 3 loops. This is inneficient and means that several computations are repeated for every combination, which is - I think - why it takes so long.
- *Day 08*: Was fearing being slow but ended up not being the case, runs under 0.00x seconds. Using the right data structures made it simple, and used operator.add/sub as parameters to a function to avoid duplicated code. Harder to understand the problem statement than it was to code.


Also: coding in vscode using vim, for old-times sake.