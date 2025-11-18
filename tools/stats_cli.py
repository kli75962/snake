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

def run_pathfinder_benchmarks(episodes=5):
    """Benchmark all solvers with different pathfinder algorithm combinations."""
    solvers = ["hamilton", "greedy"]  # Only path-based solvers support custom algorithms
    algorithms = ["bfs", "astar", "dfs"]
    
    results = {}
    total_combinations = len(solvers) * len(algorithms) * len(algorithms)
    current = 0
    
    for solver_name in solvers:
        for short_alg in algorithms:
            for long_alg in algorithms:
                current += 1
                print(f"[{current}/{total_combinations}] {solver_name} "
                      f"(short={short_alg}, long={long_alg})... ", end="", flush=True)
                try:
                    conf = GameConf()
                    conf.solver_name = solver_name.capitalize() + "Solver"
                    conf.short_algr = short_alg
                    conf.long_algr = long_alg
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
                    
                    key = f"{solver_name}|{short_alg}|{long_alg}"
                    results[key] = {
                        "solver": solver_name.capitalize(),
                        "short_alg": short_alg,
                        "long_alg": long_alg,
                        "avg_length": avg_length,
                        "avg_steps": avg_steps,
                    }
                    
                    print(f"✓ (Len: {avg_length:.1f}, Steps: {avg_steps:.0f})")
                    
                except Exception as e:
                    error_msg = str(e)
                    if "not supported" in error_msg.lower():
                        print(f"✗ Not Supported: {error_msg}")
                    else:
                        print(f"✗ Error: {error_msg[:60]}")
                    key = f"{solver_name}|{short_alg}|{long_alg}"
                    results[key] = {
                        "solver": solver_name.capitalize(),
                        "short_alg": short_alg,
                        "long_alg": long_alg,
                        "avg_length": "N/A",
                        "avg_steps": "N/A",
                    }
    
    return results

def display_pathfinder_table(results):
    """Display results in a formatted table organized by solver."""
    # Group results by solver
    by_solver = {}
    for key, data in results.items():
        solver = data["solver"]
        if solver not in by_solver:
            by_solver[solver] = []
        by_solver[solver].append(data)
    
    # Display table for each solver
    for solver in sorted(by_solver.keys()):
        print(f"\n{'='*90}")
        print(f"{solver} Solver - Path Finder Algorithm Comparison")
        print(f"{'='*90}")
        
        headers = ["Shortest Alg", "Longest Alg", "Avg Length", "Avg Steps"]
        rows = []
        
        for data in sorted(by_solver[solver], key=lambda x: (x["short_alg"], x["long_alg"])):
            # Skip A* for longest path (not supported in Hamilton solver)
            if data["long_alg"] == "astar" and solver == "Hamilton":
                continue
            
            avg_length = data["avg_length"]
            avg_steps = data["avg_steps"]
            
            if isinstance(avg_length, str):
                avg_length_str = avg_length
                avg_steps_str = avg_steps
            else:
                avg_length_str = f"{avg_length:.2f}"
                avg_steps_str = f"{avg_steps:.0f}"
            
            rows.append([
                data["short_alg"],
                data["long_alg"],
                avg_length_str,
                avg_steps_str,
            ])
        
        if HAS_TABULATE:
            table = tabulate(rows, headers=headers, tablefmt="grid")
            print(table)
        else:
            _print_table_manual(headers, rows)

def main():
    parser = argparse.ArgumentParser(
        description="Run benchmarks for all snake solvers and display statistics."
    )
    parser.add_argument(
        "-e",
        "--episodes",
        type=int,
        default=None,
        help="Number of episodes to run per solver (default: 10 for standard, 5 for -all)",
    )
    parser.add_argument(
        "-s",
        "--solvers",
        nargs="+",
        choices=["hamilton", "greedy", "astar", "astar_safe", "dqn"],
        help="Specific solvers to benchmark (for standard mode only)",
    )
    parser.add_argument(
        "-all",
        action="store_true",
        help="Test all algorithm combinations across solvers"
    )
    
    args = parser.parse_args()
    
    if args.all:
        episodes = args.episodes if args.episodes is not None else 5
        print("="*90)
        print("ALGORITHM COMBINATION BENCHMARK")
        print(f"Testing all algorithm combinations across solvers ({episodes} episodes each)")
        print("="*90)
        print("\nProgress:")
        results = run_pathfinder_benchmarks(episodes=episodes)
        display_pathfinder_table(results)
        print(f"\n{'='*90}")
        print("Benchmark Complete!")
        print("="*90)
    else:
        episodes = args.episodes if args.episodes is not None else 10
        print(f"Running benchmarks with {episodes} episodes per solver...\n")
        stats = run_benchmarks(episodes=episodes, solvers=args.solvers)
        print("\n" + "="*60)
        print("SNAKE SOLVER STATISTICS")
        print("="*60)
        display_table(stats)

if __name__ == "__main__":
    main()
