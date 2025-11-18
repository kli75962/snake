# Snake Game AI Solver

AI solver implementations for the Snake game. Multiple algorithms are available to control the snake's movement and maximize game performance.

***[Algorithms >][doc-algorithms]***

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

```bash
pip install -r requirements.txt
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
```

**Available algorithms:** `bfs`, `astar`, `dfs`

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

## Available Solvers

| Solver | Type | Speed | Reliability |
|--------|------|-------|-------------|
| Hamilton | Path-based | Fast | ⭐⭐⭐⭐⭐ |
| Greedy | Path-based | Medium | ⭐⭐⭐⭐ |
| DQN | Machine Learning | Medium | ⭐⭐ |

## License

See [LICENSE](./LICENSE) for details.