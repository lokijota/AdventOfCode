# Advent Of Code 2025

Coding in Python 3.14.0. Trying uv (https://docs.astral.sh/uv/) as a package manager. 

# uv

Setup steps:

- Installed as per guidance on `uv` docs.
- Created a folder for AOC 2025 and cd'd into it
- Updated the contents of `pyproject.toml`
- `uv init` to create the project in the current
- `uv add numpy` to add python packages
- `source .venv/bin/activate` to activate the environment (needed before running the code)
- If there is an error with Vs Code not using the right Python environment, do: View > Command Pallete > Python: Select Interpreter.

# Notes on the execises

- **Day 01**: Simple, with modulus calculations
- **Day 02**: Simple, they key thing here for part 2 was to use an auxiliary structure to note where to search for repeated sequences. Could be faster, but even so it's under 2 secs.
- **Day 03**: Did a first implementation that did loops, but this didn't work for the second part. Final implementation is fast for both cases (same code, one variable configuration is different), and essentially uses the max of a progressing slice to find each of the highest digits. A few ms run-time for both cases.
- **Day 04**: Happy with this one. Each part runs under 0.02s. Use an auxiliary bidim array with +2 dimension to avoid borders, and that array has the number of surrounding rolls. For part 2 I just have to consecutively substract to this, using a large number to mark already removed rolls. Quick and elegant (using more memory, though)
- **Day 05**: Again the topic of ranges. Simple and fast. Could probably also have used https://pypi.org/project/portion/ again, but not worth it.
- **Day 06**: Part 1 simple, part 2 also simple but somewhat annoying. I'm sure there's a cleaner way to do it, still execition time is miliseconds.
- **Day 07**: The Tachyons one with the beam splitter. Second part felt more complicated than it is really, and also runs in ms times.


Also: coding in vscode using **vim**, for old-times sake.