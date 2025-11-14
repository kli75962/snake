"""
Statistics GUI for comparing different snake solvers.
"""

import tkinter as tk
from tkinter import ttk
import threading

from snake.game import Game, GameConf, GameMode


class SolverStatsWindow(tk.Tk):
    """Window for displaying solver statistics."""
    
    SOLVERS = [
        ("Hamilton", "HamiltonSolver"),
        ("Greedy", "GreedySolver"),
        ("A* Fast", "AStarSolver"),
        ("A* Safe", "AStarSafeSolver"),
    ]
    
    def __init__(self):
        super().__init__()
        
        self.title("Snake Solver Statistics")
        self.geometry("700x500")
        self.resizable(False, False)
        
        # Variables
        self.episodes_var = tk.StringVar(value="10")
        self.running = False
        self.results = {}
        
        self._create_widgets()
        
    def _create_widgets(self):
        # Title
        title_label = tk.Label(
            self, 
            text="Snake Solver Statistics", 
            font=("Arial", 18, "bold"),
            pady=20
        )
        title_label.pack()
        
        # Settings frame
        settings_frame = tk.Frame(self, pady=10)
        settings_frame.pack()
        
        tk.Label(settings_frame, text="Episodes per solver:", font=("Arial", 11)).grid(row=0, column=0, padx=5)
        episodes_entry = tk.Entry(settings_frame, textvariable=self.episodes_var, width=10, font=("Arial", 11))
        episodes_entry.grid(row=0, column=1, padx=5)
        
        # Run button
        self.run_button = tk.Button(
            settings_frame,
            text="Run Benchmarks",
            command=self._run_benchmarks,
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        )
        self.run_button.grid(row=0, column=2, padx=10)
        
        # Status label
        self.status_label = tk.Label(
            self,
            text="Ready",
            font=("Arial", 10),
            fg="gray"
        )
        self.status_label.pack(pady=5)
        
        # Results table
        table_frame = tk.Frame(self, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Create treeview
        columns = ("solver", "avg_length", "avg_steps", "episodes")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        # Define headings
        self.tree.heading("solver", text="Solver Name")
        self.tree.heading("avg_length", text="Avg Length")
        self.tree.heading("avg_steps", text="Avg Steps")
        self.tree.heading("episodes", text="Episodes")
        
        # Define column widths
        self.tree.column("solver", width=200, anchor="w")
        self.tree.column("avg_length", width=150, anchor="center")
        self.tree.column("avg_steps", width=150, anchor="center")
        self.tree.column("episodes", width=150, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Footer
        footer_label = tk.Label(
            self,
            text="Note: Higher average length is better (max: 64)",
            font=("Arial", 9),
            fg="gray"
        )
        footer_label.pack(pady=10)
        
    def _run_benchmarks(self):
        """Run benchmarks in a separate thread."""
        if self.running:
            return
            
        try:
            episodes = int(self.episodes_var.get())
            if episodes <= 0:
                raise ValueError()
        except ValueError:
            self.status_label.config(text="Invalid episode count!", fg="red")
            return
        
        self.running = True
        self.run_button.config(state=tk.DISABLED)
        self.status_label.config(text="Running benchmarks...", fg="blue")
        
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Run in thread to avoid freezing GUI
        thread = threading.Thread(target=self._benchmark_thread, args=(episodes,))
        thread.daemon = True
        thread.start()
        
    def _benchmark_thread(self, episodes):
        """Run benchmarks for all solvers."""
        for i, (display_name, solver_name) in enumerate(self.SOLVERS):
            self.status_label.config(text=f"Testing {display_name}... ({i+1}/{len(self.SOLVERS)})")
            
            try:
                total_length = 0
                total_steps = 0
                
                for ep in range(episodes):
                    conf = GameConf()
                    conf.solver_name = solver_name
                    conf.mode = GameMode.BENCHMARK
                    
                    game = Game(conf)
                    game.run()
                    
                    total_length += game.snake.steps
                    total_steps += game.episode_step
                
                avg_length = total_length / episodes
                avg_steps = total_steps / episodes
                
                # Add to table
                self.tree.insert("", tk.END, values=(
                    display_name,
                    f"{avg_length:.2f}",
                    f"{avg_steps:.2f}",
                    episodes
                ))
                
            except Exception as e:
                self.tree.insert("", tk.END, values=(
                    display_name,
                    "Error",
                    str(e)[:20],
                    episodes
                ))
        
        # Finished
        self.status_label.config(text="Benchmarks completed!", fg="green")
        self.run_button.config(state=tk.NORMAL)
        self.running = False


if __name__ == "__main__":
    window = SolverStatsWindow()
    window.mainloop()
