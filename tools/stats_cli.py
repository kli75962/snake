import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from snake.game import Game, GameConf, GameMode
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

def run_benchmarks(episodes=10, solvers=None):
    solvers_available = {
        "hamilton": "HamiltonSolver",
        "greedy": "GreedySolver",
        "astar": "AStarSolver",
        "astar_safe": "AStarSafeSolver",
        "dqn": "DQNSolver",
    }
    
    if solvers is None:
        solvers_to_run = solvers_available
    else:
        solvers_to_run = {k: v for k, v in solvers_available.items() if k in solvers}
    
    stats = {}
    total_solvers = len(solvers_to_run)
    
    for idx, (solver_key, solver_name) in enumerate(solvers_to_run.items(), 1):
        print(f"[{idx}/{total_solvers}] Running {solver_name}... ", end="", flush=True)
        try:
            conf = GameConf()
            conf.solver_name = solver_name
            conf.mode = GameMode.BENCHMARK
            game = Game(conf)
            total_length = 0
            total_steps = 0
            steps_limit = 5000
            for ep in range(episodes):
                while True:
                    game._game_main_normal()
                    if game._map.is_full():
                        break
                    if game._snake.dead:
                        break
                    if game._snake.steps >= steps_limit:
                        break
                
                total_length += game._snake.len()
                total_steps += game._snake.steps
                game._reset()
            
            avg_length = total_length / episodes if episodes > 0 else 0
            avg_steps = total_steps / episodes if episodes > 0 else 0
            
            stats[solver_name] = {
                "avg_length": avg_length,
                "avg_steps": avg_steps,
                "episodes": episodes,
            }
            
            print(f"Done! (Avg Length: {avg_length:.2f}, Avg Steps: {avg_steps:.0f})")
            
        except Exception as e:
            print(f"Error: {e}")
            stats[solver_name] = {
                "avg_length": "Error",
                "avg_steps": "Error",
                "episodes": episodes,
            }
    return stats

def display_table(stats):
    headers = ["Solver Name", "Average Length", "Average Steps", "Episodes"]
    rows = []
    for solver_name, data in stats.items():
        avg_length = data["avg_length"]
        avg_steps = data["avg_steps"]
        episodes = data["episodes"]
        
        if isinstance(avg_length, str):
            avg_length_str = avg_length
        else:
            avg_length_str = f"{avg_length:.2f}"
        
        if isinstance(avg_steps, str):
            avg_steps_str = avg_steps
        else:
            avg_steps_str = f"{avg_steps:.0f}"
        
        rows.append([solver_name, avg_length_str, avg_steps_str, episodes])
    
    if HAS_TABULATE:
        table = tabulate(rows, headers=headers, tablefmt="grid")
        print("\n" + table + "\n")
    else:
        print()
        _print_table_manual(headers, rows)
        print()

def _print_table_manual(headers, rows):
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))
    for row in rows:
        row_str = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(row_str)

def main():
    parser = argparse.ArgumentParser(
        description="Run benchmarks for all snake solvers and display statistics."
    )
    parser.add_argument(
        "-e",
        "--episodes",
        type=int,
        default=10,
        help="Number of episodes to run per solver (default: 10)",
    )
    parser.add_argument(
        "-s",
        "--solvers",
        nargs="+",
        choices=["hamilton", "greedy", "astar", "astar_safe", "dqn"],
        help="Specific solvers to benchmark (default: all)",
    )
    
    args = parser.parse_args()
    print(f"Running benchmarks with {args.episodes} episodes per solver...\n")
    stats = run_benchmarks(episodes=args.episodes, solvers=args.solvers)
    print("\n" + "="*60)
    print("SNAKE SOLVER STATISTICS")
    print("="*60)
    display_table(stats)

if __name__ == "__main__":
    main()
