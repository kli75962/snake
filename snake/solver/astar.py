import sys
from collections import deque
from heapq import heappop, heappush

from snake.base.pos import Pos
from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver


class _AStarCell:

    def __init__(self):
        self.reset()

    def __str__(self):
        return f"{{ g: {self.g}  f: {self.f}  parent: {str(self.parent)} }}"

    __repr__ = __str__

    def reset(self):
        self.g = sys.maxsize
        self.f = sys.maxsize
        self.parent = None
        self.in_open = False
        self.in_closed = False


class AStarSolver(BaseSolver):
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
        head = self.snake.head()

        path_to_food = self._astar_path_to_food()
        if path_to_food:
            return path_to_food[0]

        self._path_solver.snake = self.snake
        path_to_tail = self._path_solver.longest_path_to_tail()
        if len(path_to_tail) > 1:
            return path_to_tail[0]

        direc, max_dist = self.snake.direc, -1
        for adj in head.all_adj():
            if self.map.is_safe(adj):
                dist = Pos.manhattan_dist(adj, self.map.food)
                if dist > max_dist:
                    max_dist = dist
                    direc = head.direc_to(adj)
        return direc

    def _astar_path_to_food(self):
        return self._astar_search(self.map.food)

    def _astar_path_to_tail(self):
        return self._astar_search(self.snake.tail())

    def _astar_search(self, destination):
        self._reset_table()

        head = self.snake.head()
        start_cell = self._table[head.x][head.y]
        start_cell.g = 0
        start_cell.f = self._heuristic(head, destination)
        open_set = []
        counter = 0
        heappush(open_set, (start_cell.f, counter, head))
        start_cell.in_open = True

        while open_set:
            _, _, current = heappop(open_set)
            current_cell = self._table[current.x][current.y]
            current_cell.in_open = False
            current_cell.in_closed = True
            if current == destination:
                return self._build_path(head, destination)

            for neighbor in current.all_adj():
                if not self._is_valid_astar(neighbor):
                    continue
                neighbor_cell = self._table[neighbor.x][neighbor.y]

                if neighbor_cell.in_closed:
                    continue
                tentative_g = current_cell.g + 1

                if not neighbor_cell.in_open or tentative_g < neighbor_cell.g:
                    neighbor_cell.parent = current
                    neighbor_cell.g = tentative_g
                    neighbor_cell.f = tentative_g + self._heuristic(neighbor, destination)
                    if not neighbor_cell.in_open:
                        counter += 1
                        heappush(open_set, (neighbor_cell.f, counter, neighbor))
                        neighbor_cell.in_open = True
        return deque()

    def _heuristic(self, pos, goal):
        return Pos.manhattan_dist(pos, goal)

    def _is_valid_astar(self, pos):
        return self.map.is_safe(pos)

    def _reset_table(self):
        for row in self._table:
            for cell in row:
                cell.reset()

    def _build_path(self, start, end):
        path = deque()
        current = end
        while current != start:
            parent = self._table[current.x][current.y].parent
            if parent is None:
                return deque()  # Invalid path
            path.appendleft(parent.direc_to(current))
            current = parent
        return path
