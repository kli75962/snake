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
|[Hamilton][doc-hamilton]|![][demo-hamilton]|63.94|722.41|
|[Greedy][doc-greedy]|![][demo-greedy]|60.10|1027.21|
|[A* (Safe)][doc-astar]|-|59.89|780.55|
|[A* (Fast)][doc-astar]|-|25.48|151.83|
|[DQN][doc-dqn]<br>(experimental)|![][demo-dqn]|24.44|131.69|

**Note:** A* (Safe) provides the best balance between speed and safety. A* (Fast) prioritizes speed over survival.

## Installation

Requirements: Python 3.6+ with [Tkinter][doc-tkinter] installed.

```bash
pip install -r requirements.txt
```

**Note:** The DQN solver now works with TensorFlow 2.x (including Keras 3). All solvers are fully functional!

## Usage

### Running the Game with GUI

Run a specific solver with GUI:

```bash
# Hamilton solver (default, guaranteed completion)
python run.py

# Greedy solver (traditional approach)
python run.py -s greedy

# A* Safe solver (best balance of speed and safety) ⭐
python run.py -s astar_safe

# A* Fast solver (maximum speed, low survival)
python run.py -s astar

# DQN solver (experimental, requires TF 2.10.x)
python run.py -s dqn -m train_dqn

python run.py -s dqn
```

**Note about DQN:** The DQN (Deep Q-Network) solver uses machine learning and requires training before it can play well. Without training, it will make random moves and die quickly. See "Training DQN" section below for instructions.

**GUI Controls:**
- **SPACE**: Pause/Resume
- **ESC**: Exit

### Running Benchmarks (No GUI)

Test solver performance without GUI:

```bash
# Benchmark mode - you'll be prompted for number of episodes
python run.py -s hamilton -m bcmk

# Example: Test 1000 episodes
echo 1000 | python run.py -s hamilton -m bcmk
```
### Training DQN

Train the DQN (Deep Q-Network) solver:

**Important:** DQN is a machine learning model that learns by playing many games. Initial performance will be poor until it learns effective strategies.

#### Training Commands

```bash
# Train without GUI (faster, recommended for long training)
python run.py -s dqn -m train_dqn

# Train with GUI (watch it learn in real-time with 4 plots)
python run.py -s dqn -m train_dqn_gui
```

#### Training Process

1. **Memory Filling Phase** (0-100,000 steps)
   - Agent plays randomly to fill replay memory buffer
   - You'll see logs: `mem_cnt: 5000`, `mem_cnt: 10000`, etc.
   - No learning occurs during this phase

2. **Training Phase** (100,000+ steps)
   - Agent starts learning from experiences
   - Checkpoints auto-save every 5,000 steps
   - Training history saved as `.npy` files in `logs/`
   - Expected training time: 6-12 hours for good performance

#### Monitoring Training

**View real-time plots** (if using `train_dqn_gui`):
- Loss: Neural network training loss
- Snake Step: Steps per episode over time
- Reward: Cumulative reward per episode
- Snake Length: Snake length achieved per episode

**View saved training plots:**
```bash
# Plot history from saved data (after stopping training)
python tools\plot_dqn_history.py 1 15506

# Replace 15506 with your last training step number
# Check logs/ folder for history-*-1-XXXXX.npy files to find the step number
```

**Check training progress:**
```bash
# View last 20 lines of log file with live updates
Get-Content logs\snake.log -Tail 20 -Wait
```

#### Stopping and Resuming Training

**To stop training:**
- Press `Ctrl+C` in terminal
- Or close the GUI window (if using `train_dqn_gui`)
- Training history automatically saves before exit

**To resume from a checkpoint:**
1. Check for checkpoint files: `logs/solver-net-*.data-*`, `logs/solver-var-*.json`
2. Find the step number from the checkpoint filename
3. Edit `snake/solver/dqn/__init__.py`, line 96:
   ```python
   self._restore_step = 10000  # Change from 0 to your checkpoint step
   ```
4. Run training command again

**Benchmark:** 24.44 avg length achieved at 3M steps

### Running Tests

Run unit tests:

```bash
# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/solver/test_astar.py
```

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

## License

See the [LICENSE](./LICENSE) file for license rights and limitations.


[snake-wiki]: https://en.wikipedia.org/wiki/Snake_(video_game)
[snake-cpp]: https://github.com/chuyangliu/snake/tree/7227f5e0f3185b07e9e3de1ac5c19a17b9de3e3c

[doc-tkinter]: https://docs.python.org/3/library/tkinter.html
[doc-algorithms]: ./docs/algorithms.md
[doc-greedy]: ./docs/algorithms.md#greedy-solver
[doc-hamilton]: ./docs/algorithms.md#hamilton-solver
[doc-astar]: ./docs/algorithms.md#astar-solver
[doc-dqn]: ./docs/algorithms.md#dqn-solver

[demo-hamilton]: ./docs/images/solver_hamilton.gif
[demo-greedy]: ./docs/images/solver_greedy.gif
[demo-dqn]: ./docs/images/solver_dqn.gif
