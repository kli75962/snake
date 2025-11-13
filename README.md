# Snake

The project focuses on the artificial intelligence of the [Snake][snake-wiki] game. The snake's goal is to eat the food continuously and fill the map with its bodies as soon as possible. Originally, the project was [written in C++][snake-cpp]. It has now been rewritten in Python for a user-friendly GUI and the simplicity in algorithm implementations.

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

```
pip install -r requirements.txt
python run.py [-h]
```

Run unit tests:

```
python -m pytest
```

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

# Solver Statistics CLI Guide

This guide explains how to use the command-line interface to display statistics for all solvers.

## Usage

### Option 1: Using the standalone CLI tool

Run the standalone stats CLI directly from the `tools/` directory:

```bash
python tools/stats_cli.py [options]
```

**Options:**
- `-e, --episodes EPISODES`: Number of episodes to run per solver (default: 10)
- `-s, --solvers SOLVER1 SOLVER2 ...`: Run only specific solvers (default: all)

**Examples:**

Display statistics for all solvers with 10 episodes each:
```bash
python tools/stats_cli.py
```

Display statistics for all solvers with 5 episodes each:
```bash
python tools/stats_cli.py --episodes 5
```

Display statistics for only Hamilton and Greedy solvers:
```bash
python tools/stats_cli.py --solvers hamilton greedy
```

Display statistics for specific solvers with custom episode count:
```bash
python tools/stats_cli.py --episodes 3 --solvers hamilton astar_safe
```

### Option 2: Using the main run.py script

You can also use the `--stats-cli` option with `run.py`:

```bash
python run.py --stats-cli [options]
```

**Options:**
- `-e, --episodes EPISODES`: Number of episodes to run per solver (default: 10)

**Examples:**

Display statistics with default 10 episodes:
```bash
python run.py --stats-cli
```

Display statistics with 5 episodes per solver:
```bash
python run.py --stats-cli --episodes 5
```

## Available Solvers

The following solvers are available for benchmarking:

- `hamilton`: Hamilton Solver (optimal path)
- `greedy`: Greedy Solver
- `astar`: A* Solver
- `astar_safe`: A* Safe Solver
- `dqn`: DQN Solver (Deep Q-Network - may have compatibility issues)

## Output

The tool displays results in a table format with the following columns:

| Column | Description |
|--------|-------------|
| Solver Name | Name of the solver |
| Average Length | Average snake length achieved (max: 64) |
| Average Steps | Average number of steps taken |
| Episodes | Number of episodes run |

## Example Output

```
Running benchmarks with 2 episodes per solver...

[1/5] Running HamiltonSolver... Done! (Avg Length: 64.00, Avg Steps: 700)
[2/5] Running GreedySolver... Done! (Avg Length: 62.00, Avg Steps: 750)
[3/5] Running AStarSolver... Done! (Avg Length: 30.00, Avg Steps: 200)
[4/5] Running AStarSafeSolver... Done! (Avg Length: 62.00, Avg Steps: 700)
[5/5] Running DQNSolver... Error: ...

============================================================
SNAKE SOLVER STATISTICS
============================================================

Solver Name     | Average Length | Average Steps | Episodes
-----------------------------------------------------------
HamiltonSolver  | 64.00          | 700           | 2       
GreedySolver    | 62.00          | 750           | 2       
AStarSolver     | 30.00          | 200           | 2       
AStarSafeSolver | 62.00          | 700           | 2       
DQNSolver       | Error          | Error         | 2
```

## Notes

- The DQN Solver may have TensorFlow compatibility issues on some systems.
- Each episode runs until the snake either fills the map, dies, or reaches a 5000-step limit.
- Results will vary between runs due to the randomized nature of food placement.
