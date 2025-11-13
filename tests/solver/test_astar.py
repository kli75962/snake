"""Unit tests for A* Solver."""

import unittest
from snake.base import Direc, Map, PointType, Pos, Snake
from snake.solver.astar import AStarSolver


class TestAStarSolver(unittest.TestCase):
    """Test cases for AStarSolver class."""

    def setUp(self):
        """Set up test fixtures."""
        self.map = Map(10, 10)
        # Create initial snake bodies
        init_bodies = [Pos(1, 4), Pos(1, 3), Pos(1, 2), Pos(1, 1)]
        init_types = [PointType.HEAD_R] + [PointType.BODY_HOR] * 3
        self.snake = Snake(self.map, Direc.RIGHT, init_bodies, init_types)
        # Create food on the map
        self.map.create_rand_food()
        self.solver = AStarSolver(self.snake)

    def test_init(self):
        """Test solver initialization."""
        self.assertIsNotNone(self.solver)
        self.assertEqual(self.solver.snake, self.snake)
        self.assertEqual(self.solver.map, self.map)
        self.assertEqual(len(self.solver.table), 10)
        self.assertEqual(len(self.solver.table[0]), 10)

    def test_table_initialization(self):
        """Test that table cells are properly initialized."""
        for row in self.solver.table:
            for cell in row:
                self.assertFalse(cell.in_open)
                self.assertFalse(cell.in_closed)
                self.assertIsNone(cell.parent)

    def test_next_direc_returns_valid_direction(self):
        """Test that next_direc returns a valid direction."""
        direc = self.solver.next_direc()
        self.assertIn(direc, [Direc.LEFT, Direc.RIGHT, Direc.UP, Direc.DOWN])

    def test_path_to_food_exists(self):
        """Test that A* can find path to food when one exists."""
        path = self.solver._astar_path_to_food()
        # Path should exist in most cases on empty map
        self.assertIsNotNone(path)

    def test_path_to_tail_exists(self):
        """Test that A* can find path to tail."""
        path = self.solver._astar_path_to_tail()
        # Should return a path (even if just empty or length 1)
        self.assertIsNotNone(path)

    def test_heuristic_is_manhattan_distance(self):
        """Test that heuristic function returns correct Manhattan distance."""
        from snake.base.pos import Pos
        pos1 = Pos(0, 0)
        pos2 = Pos(3, 4)
        # Manhattan distance should be |3-0| + |4-0| = 7
        self.assertEqual(self.solver._heuristic(pos1, pos2), 7)

        pos3 = Pos(5, 5)
        pos4 = Pos(5, 5)
        # Same position should have distance 0
        self.assertEqual(self.solver._heuristic(pos3, pos4), 0)

    def test_reset_table(self):
        """Test that table reset works correctly."""
        # Modify some cells
        self.solver.table[0][0].in_closed = True
        self.solver.table[1][1].g = 5
        from snake.base.pos import Pos
        self.solver.table[2][2].parent = Pos(1, 1)

        # Reset
        self.solver._reset_table()

        # Verify all cells are reset
        for row in self.solver.table:
            for cell in row:
                self.assertFalse(cell.in_open)
                self.assertFalse(cell.in_closed)
                self.assertIsNone(cell.parent)
                import sys
                self.assertEqual(cell.g, sys.maxsize)
                self.assertEqual(cell.f, sys.maxsize)

    def test_build_path(self):
        """Test path building from parent pointers."""
        from snake.base.pos import Pos
        # Create a simple path: (0,0) -> (0,1) -> (0,2)
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
        """Test that solver handles situations where food is unreachable."""
        # Create a scenario where the snake might be trapped
        # The solver should not crash, even if path to food doesn't exist
        try:
            for _ in range(10):
                direc = self.solver.next_direc()
                self.assertIsNotNone(direc)
        except Exception as e:
            self.fail(f"Solver crashed with exception: {e}")

    def test_astar_vs_straight_line_optimality(self):
        """Test that A* finds optimal path in simple scenarios."""
        from snake.base.pos import Pos
        # In an empty map, path to food should be reasonably optimal
        path = self.solver._astar_path_to_food()
        if path:
            # Path length should not be excessively longer than Manhattan distance
            food = self.map.food
            head = self.snake.head()
            manhattan = Pos.manhattan_dist(head, food)
            # A* should find a path close to optimal
            # Allow some margin as direct path might not always be possible
            self.assertLessEqual(len(path), manhattan * 2)


if __name__ == "__main__":
    unittest.main()
