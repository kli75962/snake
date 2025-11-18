import random
import sys
from collections import deque
from heapq import heappop, heappush

from snake.base import Direc, PointType
from snake.solver.base import BaseSolver


class _TableCell:
    def __init__(self):
        self.reset()

    def __str__(self):
        return (
            f"{{ dist: {self.dist}  parent: {str(self.parent)}  visit: {self.visit} }}"
        )

    __repr__ = __str__

    def reset(self):
        # Shortest path
        self.parent = None
        self.dist = sys.maxsize
        # Longest path
        self.visit = False


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


class PathSolver(BaseSolver):
    def __init__(self, snake, short_algr="bfs", long_algr="heuristic"):
        super().__init__(snake)
        self.short_algr = short_algr
        self.long_algr = long_algr
        self._table = [
            [_TableCell() for _ in range(snake.map.num_cols)]
            for _ in range(snake.map.num_rows)
        ]
        self._astar_table = [
            [_AStarCell() for _ in range(snake.map.num_cols)]
            for _ in range(snake.map.num_rows)
        ]

    @property
    def table(self):
        return self._table

    def shortest_path_to_food(self):
        return self.path_to(self.map.food, "shortest")

    def longest_path_to_tail(self):
        return self.path_to(self.snake.tail(), "longest")

    def path_to(self, des, path_type):
        ori_type = self.map.point(des).type
        self.map.point(des).type = PointType.EMPTY
        if path_type == "shortest":
            path = self._find_shortest_path(des)
        elif path_type == "longest":
            path = self._find_longest_path(des)
        self.map.point(des).type = ori_type  # Restore origin type
        return path

    def _find_shortest_path(self, des):
        """Route shortest path finding based on algorithm selection."""
        if self.short_algr == "astar":
            return self._astar_search(des)
        elif self.short_algr == "dfs":
            return self._dfs_path_to(des)
        elif self.short_algr == "bfs":
            return self._bfs_shortest_path(des)
        else:
            raise ValueError(f"Unsupported shortest path algorithm: {self.short_algr}. Use 'bfs', 'astar', or 'dfs'.")

    def _find_longest_path(self, des):
        """Route longest path finding based on algorithm selection, using base algorithm + heuristic extension."""
        # Select base path finder based on long_algr
        if self.long_algr == "astar":
            base_path = self._astar_search(des)
        elif self.long_algr == "dfs":
            base_path = self._dfs_path_to(des)
        elif self.long_algr == "bfs":
            base_path = self._bfs_shortest_path(des)
        elif self.long_algr == "heuristic":
            # For 'heuristic', use A* as base (since it uses Manhattan heuristic) + extension
            base_path = self._astar_search(des)
        else:
            raise ValueError(f"Unsupported longest path algorithm: {self.long_algr}. Use 'bfs', 'astar', 'dfs', or 'heuristic'.")

        # Apply heuristic extension to the base path
        return self._extend_path(base_path, des)

    def shortest_path_to(self, des):
        """Find the shortest path from the snake's head to the destination using BFS.

        Args:
            des (snake.base.pos.Pos): The destination position on the map.

        Returns:
            A collections.deque of snake.base.direc.Direc indicating the path directions.
        """
        return self._bfs_shortest_path(des)

    def _bfs_shortest_path(self, des):
        """Find the shortest path from the snake's head to the destination.

        Args:
            des (snake.base.pos.Pos): The destination position on the map.

        Returns:
            A collections.deque of snake.base.direc.Direc indicating the path directions.
        """
        self._reset_table()

        head = self.snake.head()
        self._table[head.x][head.y].dist = 0
        queue = deque()
        queue.append(head)

        while queue:
            cur = queue.popleft()
            if cur == des:
                return self._build_path(head, des)

            # Arrange the order of traverse to make the path as straight as possible
            if cur == head:
                first_direc = self.snake.direc
            else:
                first_direc = self._table[cur.x][cur.y].parent.direc_to(cur)
            adjs = cur.all_adj()
            random.shuffle(adjs)
            for i, pos in enumerate(adjs):
                if first_direc == cur.direc_to(pos):
                    adjs[0], adjs[i] = adjs[i], adjs[0]
                    break

            # Traverse adjacent positions
            for pos in adjs:
                if self._is_valid(pos):
                    adj_cell = self._table[pos.x][pos.y]
                    if adj_cell.dist == sys.maxsize:
                        adj_cell.parent = cur
                        adj_cell.dist = self._table[cur.x][cur.y].dist + 1
                        queue.append(pos)

        return deque()

    def longest_path_to(self, des):
        """Find the longest path from the snake's head to the destination.

        Args:
            des (snake.base.pos.Pos): The destination position on the map.

        Returns:
            A collections.deque of snake.base.direc.Direc indicating the path directions.
        """
        return self._find_longest_path(des)

    def _extend_path(self, path, des):
        """Apply heuristic extension to a base path to make it longer."""
        if not path:
            return deque()

        self._reset_table()
        cur = head = self.snake.head()

        # Set all positions on the base path to 'visited'
        self._table[cur.x][cur.y].visit = True
        for direc in path:
            cur = cur.adj(direc)
            self._table[cur.x][cur.y].visit = True

        # Extend the path between each pair of the positions
        idx, cur = 0, head
        while idx < len(path):
            cur_direc = path[idx]
            nxt = cur.adj(cur_direc)

            if cur_direc == Direc.LEFT or cur_direc == Direc.RIGHT:
                tests = [Direc.UP, Direc.DOWN]
            elif cur_direc == Direc.UP or cur_direc == Direc.DOWN:
                tests = [Direc.LEFT, Direc.RIGHT]

            extended = False
            for test_direc in tests:
                cur_test = cur.adj(test_direc)
                nxt_test = nxt.adj(test_direc)
                if self._is_valid(cur_test) and self._is_valid(nxt_test):
                    self._table[cur_test.x][cur_test.y].visit = True
                    self._table[nxt_test.x][nxt_test.y].visit = True
                    path.insert(idx, test_direc)
                    path.insert(idx + 2, Direc.opposite(test_direc))
                    extended = True
                    break

            if not extended:
                cur = nxt
                idx += 1

        return path

    def _reset_table(self):
        for row in self._table:
            for col in row:
                col.reset()

    def _reset_astar_table(self):
        for row in self._astar_table:
            for col in row:
                col.reset()

    def _build_path(self, src, des):
        path = deque()
        tmp = des
        while tmp != src:
            parent = self._table[tmp.x][tmp.y].parent
            path.appendleft(parent.direc_to(tmp))
            tmp = parent
        return path

    def _build_astar_path(self, src, des):
        path = deque()
        current = des
        while current != src:
            parent = self._astar_table[current.x][current.y].parent
            if parent is None:
                return deque()
            path.appendleft(parent.direc_to(current))
            current = parent
        return path

    def _astar_search(self, destination):
        """Find path using A* algorithm."""
        self._reset_astar_table()

        head = self.snake.head()
        start_cell = self._astar_table[head.x][head.y]
        start_cell.g = 0
        start_cell.f = self._heuristic(head, destination)
        open_set = []
        counter = 0
        heappush(open_set, (start_cell.f, counter, head))
        start_cell.in_open = True

        while open_set:
            _, _, current = heappop(open_set)
            current_cell = self._astar_table[current.x][current.y]
            current_cell.in_open = False
            current_cell.in_closed = True
            if current == destination:
                return self._build_astar_path(head, destination)

            for neighbor in current.all_adj():
                if not self._is_valid_astar(neighbor):
                    continue
                neighbor_cell = self._astar_table[neighbor.x][neighbor.y]

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

    def _dfs_path_to(self, destination):
        """Find path using DFS algorithm."""
        visited = set()
        path = deque()

        def dfs(current):
            if current == destination:
                return True
            visited.add(current)

            for next_pos in current.all_adj():
                if self.map.is_safe(next_pos) and next_pos not in visited:
                    if dfs(next_pos):
                        path.appendleft(current.direc_to(next_pos))
                        return True
            return False

        head = self.snake.head()
        if dfs(head):
            return path
        return deque()

    def _heuristic(self, pos, goal):
        """Manhattan distance heuristic for A*."""
        from snake.base.pos import Pos
        return Pos.manhattan_dist(pos, goal)

    def _is_valid_astar(self, pos):
        """Check if position is valid for A*."""
        return self.map.is_safe(pos)

    def _is_valid(self, pos):
        return self.map.is_safe(pos) and not self._table[pos.x][pos.y].visit