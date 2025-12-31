# Advent Of Code 2015

Coding in Python 3.14.0. Trying uv (https://docs.astral.sh/uv/) as a package manager. 

# uv

Setup steps:

- Installed as per guidance on `uv` docs.
- Created a folder for AOC 2015 and cd'd into it
- `uv init` to create the project in the current
- Updated the contents of `pyproject.toml`
- `uv add numpy` to add python packages
- `source .venv/bin/activate` to activate the environment (needed before running the code)
- If there is an error with Vs Code not using the right Python environment, do: View > Command Pallete > Python: Select Interpreter.

# Notes on the execises

- **Day 01**: Ultra simple. After doing 2023-2025, this first day of the first year feels too simple.
- **Day 02**: Also simple, just some arithmetic. Darn GH Copilt has been trained on the solutions, hate this crap.
- **Day 03**: Simple with sets.
- **Day 04**: I just used Python's `hashlib` and brute-forced it. There's probably a better way by reverse engineering MD5's formula. Part 2 runs in under 5 seconds.
- **Day 05**: Quick with string manipulation in Python and convenient calls like `any`

Also: coding in vscode using **vim**, for old-times sake.