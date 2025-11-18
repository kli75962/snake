import argparse

from snake.game import Game, GameConf, GameMode


def main():
    dict_solver = {
        "greedy": "GreedySolver",
        "hamilton": "HamiltonSolver",
        "dqn": "DQNSolver",
    }

    dict_mode = {
        "normal": GameMode.NORMAL,
        "bcmk": GameMode.BENCHMARK,
        "train_dqn": GameMode.TRAIN_DQN,
        "train_dqn_gui": GameMode.TRAIN_DQN_GUI,
    }

    dict_algorithms = {
        "bfs": "bfs",
        "astar": "astar",
        "dfs": "dfs",
    }

    parser = argparse.ArgumentParser(description="Run snake game agent.")
    parser.add_argument(
        "-s",
        default="hamilton",
        choices=dict_solver.keys(),
        help="name of the solver to direct the snake (default: hamilton)",
    )
    parser.add_argument(
        "-m",
        default="normal",
        choices=dict_mode.keys(),
        help="game mode (default: normal)",
    )
    parser.add_argument(
        "--shortalgr",
        default="bfs",
        choices=dict_algorithms.keys(),
        help="algorithm for finding shortest path (default: bfs)",
    )
    parser.add_argument(
        "--longalgr",
        default="bfs",
        choices=dict_algorithms.keys(),
        help="algorithm for finding longest path (default: bfs)",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="show GUI with all solvers' statistics",
    )
    parser.add_argument(
        "--stats-cli",
        action="store_true",
        help="display all solvers' statistics in command-line table format",
    )
    parser.add_argument(
        "-all",
        action="store_true",
        help="test all algorithm combinations across solvers (requires --stats-cli)",
    )
    parser.add_argument(
        "-e",
        "--episodes",
        type=int,
        default=10,
        help="number of episodes to run per solver for CLI statistics (default: 10)",
    )
    args = parser.parse_args()

    if args.stats:
        from snake.stats_gui import SolverStatsWindow
        window = SolverStatsWindow()
        window.mainloop()
    elif args.stats_cli:
        from tools.stats_cli import run_benchmarks, display_table, run_pathfinder_benchmarks, display_pathfinder_table
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
            print(f"Running benchmarks with {args.episodes} episodes per solver...\n")
            stats = run_benchmarks(episodes=args.episodes)
            print("\n" + "="*60)
            print("SNAKE SOLVER STATISTICS")
            print("="*60)
            display_table(stats)
    else:
        conf = GameConf()
        conf.solver_name = dict_solver[args.s]
        conf.mode = dict_mode[args.m]
        conf.short_algr = dict_algorithms[args.shortalgr]
        conf.long_algr = dict_algorithms[args.longalgr]
        print(f"Solver: {conf.solver_name}   Mode: {conf.mode}")
        print(f"Short algorithm: {conf.short_algr}   Long algorithm: {conf.long_algr}")

        Game(conf).run()


if __name__ == "__main__":
    main()
