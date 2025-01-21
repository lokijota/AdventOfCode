# Advent Of Code 2024

Coding in Python 3.1, in VSCode with Vim (decided to go back to Uni days, because why not)

- **Day 01**: simple challenge, more of a warm-up
- **Day 02**: first part simple, second part just thinking of edge cases confused me. Not pretty code but works.
- **Day 03**: simple challenge with regex. As usual used https://regex101.com/ to test them out.
- **Day 04**: counting XMAS/MAS in a map. First part done in a non-smart but still quick way
- **Day 05**: order pages according to certain rules. First part very simple, used sets and pairwise. Second part slightly harder but the first naïve implementation of just swapping order worked well and is very fast. Unexpected.
- **Day 06**: this is the one with the guard walking around a map and finding loops. Second part runs in 8 secs, I'm sure it could be much faster.
- **Day 07**: this is the one where there's a variable number of loops. The second part takes 16 seconds which is too long. I used an `itertools.product` to generate combinations and then just did 3 loops. This is inneficient and means that several computations are repeated for every combination, which is - I think - why it takes so long.
- **Day 08**: Was fearing being slow but ended up not being the case, runs under 0.00x seconds. Using the right data structures made it simple, and used operator.add/sub as parameters to a function to avoid duplicated code. Harder to understand the problem statement than it was to code.
- **Day 09**: file system defrag. Thought about doing something smart with a FAT but ended up just using a np.array and doing it brute force. First part is sub-second, second part 12.5 seconds. Nothing spectacular here.
- **Day 10**: the "smartest" thing here is just using a tuple of 5 elements including the current height, the current coordinates and the position of the 0 that started the trail. This allows to handle the repetitions of part 1 (when it converges in 8 or 9) and replace a set with a list to handle the part 2.
- **Day 11**: happy with this one. Used hashtables to register frequencies of numbers (order is irrelevant), and both parts were solved with the same code in under 0.0x secs.

...

- **Day 24**: This was the binary adder one. Solved it visually using a library to help with visualization, after a lot of data exploration. Frustrated I didn't solve it with code.
- **Day 25**: Trivial, just one part

The hardest one for me this year was probably the robots-pressing-keyboards one. My brain got into inception and it was hard to think about it. In the end it runs fast, even if with too much code.

Also: coding in vscode using **vim**, for old-times sake.