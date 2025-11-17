import argparse

from snake.game import Game, GameConf, GameMode


def main():
    dict_solver = {
        "greedy": "GreedySolver",
        "hamilton": "HamiltonSolver",
        "astar": "AStarSolver",
        "astar_safe": "AStarSafeSolver",
        "dqn": "DQNSolver",
        "dfs": "DFSSolver", 
    }

    dict_mode = {
        "normal": GameMode.NORMAL,
        "bcmk": GameMode.BENCHMARK,
        "train_dqn": GameMode.TRAIN_DQN,
        "train_dqn_gui": GameMode.TRAIN_DQN_GUI,
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
        from tools.stats_cli import run_benchmarks, display_table
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
        print(f"Solver: {conf.solver_name}   Mode: {conf.mode}")

        Game(conf).run()


if __name__ == "__main__":
    main()
