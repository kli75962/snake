"""A* pathfinding algorithm solver for the Snake game.

This solver uses A* algorithm to find optimal paths considering both
the actual distance traveled and a heuristic estimate to the goal.
It provides a good balance between optimality and efficiency.
"""

import sys
from collections import deque
from heapq import heappop, heappush

from snake.base.pos import Pos
from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver


class _AStarCell:
    """Cell used in A* pathfinding algorithm."""

    def __init__(self):
        self.reset()

    def __str__(self):
        return f"{{ g: {self.g}  f: {self.f}  parent: {str(self.parent)} }}"

    __repr__ = __str__

    def reset(self):
        self.g = sys.maxsize  # Cost from start to current node
        self.f = sys.maxsize  # g + h (heuristic)
        self.parent = None
        self.in_open = False
        self.in_closed = False


class AStarSolver(BaseSolver):
    """A* algorithm-based solver.

    This solver uses A* pathfinding to navigate the snake. It considers:
    1. Finding optimal paths to food using A* with Manhattan distance heuristic
    2. Safety checks before committing to a path
    3. Fallback to tail-following when no safe path to food exists
    4. Emergency evasion when no other options are available

    The A* algorithm is more efficient than BFS (used in PathSolver) because
    it uses a heuristic function to prioritize exploring more promising paths.
    """

    def __init__(self, snake):
        super().__init__(snake)
        self._table = [
            [_AStarCell() for _ in range(snake.map.num_cols)]
            for _ in range(snake.map.num_rows)
        ]
        self._path_solver = PathSolver(snake)

    @property
    def table(self):
        return self._table

    def next_direc(self):
        """Determine the next direction for the snake to move.

        Aggressive A* strategy (FAST, less safe):
        1. Always go directly to food using A*
        2. Only if no path to food, follow tail
        3. Emergency fallback
        
        This prioritizes speed over safety!
        """
        head = self.snake.head()

        # Step 1: Try A* path to food - GO FOR IT!
        path_to_food = self._astar_path_to_food()
        if path_to_food:
            return path_to_food[0]  # No safety check, just go!

        # Step 2: If can't reach food, follow tail
        self._path_solver.snake = self.snake
        path_to_tail = self._path_solver.longest_path_to_tail()
        if len(path_to_tail) > 1:
            return path_to_tail[0]

        # Step 3: Emergency - move to safest adjacent position
        direc, max_dist = self.snake.direc, -1
        for adj in head.all_adj():
            if self.map.is_safe(adj):
                dist = Pos.manhattan_dist(adj, self.map.food)
                if dist > max_dist:
                    max_dist = dist
                    direc = head.direc_to(adj)

        return direc

    def _astar_path_to_food(self):
        """Find path to food using A* algorithm.

        Returns:
            deque: Path directions to food, or empty deque if no path exists.
        """
        return self._astar_search(self.map.food)

    def _astar_path_to_tail(self):
        """Find path to tail using A* algorithm (for reference, not used).

        Returns:
            deque: Path directions to tail, or empty deque if no path exists.
        """
        return self._astar_search(self.snake.tail())

    def _astar_search(self, destination):
        """A* pathfinding algorithm implementation.

        Args:
            destination (Pos): Target position to reach.

        Returns:
            deque: Path of directions from head to destination.
        """
        self._reset_table()

        head = self.snake.head()
        start_cell = self._table[head.x][head.y]
        start_cell.g = 0
        start_cell.f = self._heuristic(head, destination)

        # Priority queue: (f_score, counter, position)
        # Counter ensures FIFO ordering for equal f_scores
        open_set = []
        counter = 0
        heappush(open_set, (start_cell.f, counter, head))
        start_cell.in_open = True

        while open_set:
            _, _, current = heappop(open_set)
            current_cell = self._table[current.x][current.y]

            # Mark as visited
            current_cell.in_open = False
            current_cell.in_closed = True

            # Goal reached
            if current == destination:
                return self._build_path(head, destination)

            # Explore neighbors
            for neighbor in current.all_adj():
                if not self._is_valid_astar(neighbor):
                    continue

                neighbor_cell = self._table[neighbor.x][neighbor.y]

                # Skip if already evaluated
                if neighbor_cell.in_closed:
                    continue

                # Calculate tentative g score
                tentative_g = current_cell.g + 1

                # Discover a new node or find a better path
                if not neighbor_cell.in_open or tentative_g < neighbor_cell.g:
                    neighbor_cell.parent = current
                    neighbor_cell.g = tentative_g
                    neighbor_cell.f = tentative_g + self._heuristic(neighbor, destination)

                    if not neighbor_cell.in_open:
                        counter += 1
                        heappush(open_set, (neighbor_cell.f, counter, neighbor))
                        neighbor_cell.in_open = True

        return deque()  # No path found

    def _heuristic(self, pos, goal):
        """Heuristic function for A* (Manhattan distance).

        Args:
            pos (Pos): Current position.
            goal (Pos): Goal position.

        Returns:
            int: Estimated cost from pos to goal.
        """
        return Pos.manhattan_dist(pos, goal)

    def _is_valid_astar(self, pos):
        """Check if a position is valid for A* exploration.

        Args:
            pos (Pos): Position to check.

        Returns:
            bool: True if position can be explored.
        """
        return self.map.is_safe(pos)

    def _reset_table(self):
        """Reset all cells in the table for a new search."""
        for row in self._table:
            for cell in row:
                cell.reset()

    def _build_path(self, start, end):
        """Build path from start to end by backtracking through parents.

        Args:
            start (Pos): Starting position.
            end (Pos): Ending position.

        Returns:
            deque: Path of directions from start to end.
        """
        path = deque()
        current = end

        while current != start:
            parent = self._table[current.x][current.y].parent
            if parent is None:
                return deque()  # Invalid path
            path.appendleft(parent.direc_to(current))
            current = parent

        return path
