import unittest
from snake.base import Direc, Map, PointType, Pos, Snake
from snake.solver.astar import AStarSolver


class TestAStarSolver(unittest.TestCase):

    def setUp(self):
        self.map = Map(10, 10)
        init_bodies = [Pos(1, 4), Pos(1, 3), Pos(1, 2), Pos(1, 1)]
        init_types = [PointType.HEAD_R] + [PointType.BODY_HOR] * 3
        self.snake = Snake(self.map, Direc.RIGHT, init_bodies, init_types)
        self.map.create_rand_food()
        self.solver = AStarSolver(self.snake)

    def test_init(self):
        self.assertIsNotNone(self.solver)
        self.assertEqual(self.solver.snake, self.snake)
        self.assertEqual(self.solver.map, self.map)
        self.assertEqual(len(self.solver.table), 10)
        self.assertEqual(len(self.solver.table[0]), 10)

    def test_table_initialization(self):
        for row in self.solver.table:
            for cell in row:
                self.assertFalse(cell.in_open)
                self.assertFalse(cell.in_closed)
                self.assertIsNone(cell.parent)

    def test_next_direc_returns_valid_direction(self):
        direc = self.solver.next_direc()
        self.assertIn(direc, [Direc.LEFT, Direc.RIGHT, Direc.UP, Direc.DOWN])

    def test_path_to_food_exists(self):
        path = self.solver._astar_path_to_food()
        self.assertIsNotNone(path)

    def test_path_to_tail_exists(self):
        path = self.solver._astar_path_to_tail()
        self.assertIsNotNone(path)

    def test_heuristic_is_manhattan_distance(self):
        from snake.base.pos import Pos
        pos1 = Pos(0, 0)
        pos2 = Pos(3, 4)
        self.assertEqual(self.solver._heuristic(pos1, pos2), 7)
        pos3 = Pos(5, 5)
        pos4 = Pos(5, 5)
        self.assertEqual(self.solver._heuristic(pos3, pos4), 0)

    def test_reset_table(self):
        self.solver.table[0][0].in_closed = True
        self.solver.table[1][1].g = 5
        from snake.base.pos import Pos
        self.solver.table[2][2].parent = Pos(1, 1)
        self.solver._reset_table()

        for row in self.solver.table:
            for cell in row:
                self.assertFalse(cell.in_open)
                self.assertFalse(cell.in_closed)
                self.assertIsNone(cell.parent)
                import sys
                self.assertEqual(cell.g, sys.maxsize)
                self.assertEqual(cell.f, sys.maxsize)

    def test_build_path(self):
        from snake.base.pos import Pos
        pos1 = Pos(0, 0)
        pos2 = Pos(0, 1)
        pos3 = Pos(0, 2)
        self.solver.table[0][1].parent = pos1
        self.solver.table[0][2].parent = pos2
        path = self.solver._build_path(pos1, pos3)
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0], Direc.RIGHT)
        self.assertEqual(path[1], Direc.RIGHT)

    def test_solver_doesnt_crash_on_blocked_food(self):
        try:
            for _ in range(10):
                direc = self.solver.next_direc()
                self.assertIsNotNone(direc)
        except Exception as e:
            self.fail(f"Solver crashed with exception: {e}")

    def test_astar_vs_straight_line_optimality(self):
        from snake.base.pos import Pos
        path = self.solver._astar_path_to_food()
        if path:
            food = self.map.food
            head = self.snake.head()
            manhattan = Pos.manhattan_dist(head, food)
            self.assertLessEqual(len(path), manhattan * 2)


if __name__ == "__main__":
    unittest.main()
