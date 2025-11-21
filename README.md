# Snake

The project focuses on the artificial intelligence of the [Snake][snake-wiki] game. The snake's goal is to eat the food continuously and fill the map with its bodies as soon as possible. Originally, the project was [written in C++][snake-cpp]. It has now been rewritten in Python for a user-friendly GUI and the simplicity in algorithm implementations.

***[Algorithms >][doc-algorithms]***

## Features

- **Multiple solvers:** Hamiltonian cycle planner, a fast greedy path-finder, and an experimental Deep Q-Network (DQN) agent you can train yourself.
- **Configurable path-finding:** Mix and match shortest/longest path algorithms；`dijkstra` is supported for shortest paths, while longest paths use `bfs`/`astar`/`dfs`/`heuristic`.
- **Training-ready DQN pipeline:** Resume from previous checkpoints, log history, and visualize learning curves automatically.
- **Benchmark tooling:** Headless benchmark mode, CLI table summaries, and exhaustive algorithm-combination sweeps (including `dijkstra` when benchmarking shortest paths).
- **Statistics dashboards:** Tkinter GUI dashboard (`--stats`) and CLI reports (`--stats-cli`) for quick solver comparison.
- **Rich logging:** Every run saves to `logs/`, including solver stats, DQN checkpoints, and matplotlib history plots.
  
## Experiments

We use two metrics to evaluate the performance of an AI:

1. **Average Length:** Average length the snake has grown to (*max:* 64).
2. **Average Steps:** Average steps the snake has moved.

Test results (averaged over 1000 episodes):

| Solver | Demo (optimal) | Average Length | Average Steps |
| :----: | :------------: | :------------: | :-----------: |
|[Hamilton][doc-hamilton]|![][demo-hamilton]|63.93|717.83|
|[Greedy][doc-greedy]|![][demo-greedy]|60.15|904.56|
|[DQN][doc-dqn]<br>(experimental)|![][demo-dqn]|24.44|131.69|

## Installation

Requirements: Python 3.6+ with [Tkinter][doc-tkinter] installed.

```
pip install -r requirements.txt
python run.py [-h]
```

Run unit tests:

```
python -m pytest
```

## Quick Start

### Play with Default Solver (Hamilton)
```bash
python run.py
```

### Try Different Solvers
```bash
python run.py -s greedy        # Greedy solver
python run.py -s dqn           # DQN solver (machine learning)
```

### Customize Path-Finding Algorithms
Choose different algorithms for shortest and longest path finding:

```bash
# Default: bfs for shortest path, bfs for longest path
python run.py -s greedy

# Use A* for shortest paths, DFS for longest paths
python run.py -s greedy --shortalgr astar --longalgr dfs

# Use DFS for both shortest and longest paths
python run.py -s hamilton --shortalgr dfs --longalgr dfs

#Use greedy to control the snake's movement, and use Dijkstra when calculating the shortest path. 
python run.py -s greedy --shortalgr dijkstra
```

**Available algorithms:** `bfs`, `astar`, `dfs`,`dijkstra`

## Usage

### GUI Controls
- **SPACE**: Pause/Resume
- **ESC**: Exit

### Run Benchmarks
```bash
# Test performance without GUI
python run.py -s hamilton -m bcmk -e 100
```

### Run Tests
```bash
python -m pytest                    # Run all tests
python -m pytest tests/solver/      # Run solver tests only
```

### Show Statistics
```bash
# Standard mode: Compare solver performance
python run.py --stats-cli -e 10

# Compare all algorithm combinations
python run.py --stats-cli -all -e 5
```

### Algorithm Combination Benchmarking
Test how different algorithm combinations affect solver performance:

```bash
python run.py --stats-cli -all -e 3
```

This runs all algorithm combinations across both path-based solvers (Hamilton and Greedy), showing average path length and steps for each combination. Useful for understanding algorithm behavior and performance characteristics.

## License

See the [LICENSE](./LICENSE) file for license rights and limitations.


[snake-wiki]: https://en.wikipedia.org/wiki/Snake_(video_game)
[snake-cpp]: https://github.com/chuyangliu/snake/tree/7227f5e0f3185b07e9e3de1ac5c19a17b9de3e3c

[doc-tkinter]: https://docs.python.org/3/library/tkinter.html
[doc-algorithms]: ./docs/algorithms.md
[doc-greedy]: ./docs/algorithms.md#greedy-solver
[doc-hamilton]: ./docs/algorithms.md#hamilton-solver
[doc-dqn]: ./docs/algorithms.md#dqn-solver

[demo-hamilton]: ./docs/images/solver_hamilton.gif
[demo-greedy]: ./docs/images/solver_greedy.gif
[demo-dqn]: ./docs/images/solver_dqn.gif
