"""
Unit Tests for Goal-Based Warehouse Agent
-----------------------------------------
Includes test cases for:
1. Original assignment map (valid path exists).
2. Trivial adjacent Start-Goal map.
3. Unreachable Goal map (surrounded by obstacles).
4. Safety constraint verification (no path cell is an obstacle '#').
5. Step distance verification (every step moves exactly 1 cell orthogonally).

Note on LLM Generation:
-----------------------
Code generated with assistance from LLM, verified using standard Python unittest framework.
"""

import unittest
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from warehouse_agent import WarehouseAgent, DEFAULT_MAP


class TestWarehouseAgent(unittest.TestCase):

    def test_original_map(self):
        """Test pathfinding on the default assignment map."""
        agent = WarehouseAgent(DEFAULT_MAP)
        path, directions, states_expanded = agent.find_path()

        self.assertIsNotNone(path, "Path should be found for the original map.")
        self.assertIsNotNone(directions, "Directions list should not be None.")
        self.assertEqual(path[0], agent.start_pos, "Path must start at S.")
        self.assertEqual(path[-1], agent.goal_pos, "Path must end at G.")
        self.assertGreater(len(directions), 0, "Directions list should not be empty.")
        self.assertGreater(states_expanded, 0, "States expanded should be > 0.")

    def test_trivial_adjacent_sg(self):
        """Test pathfinding when S and G are directly adjacent."""
        trivial_map = [
            "###",
            "#SG#",
            "###"
        ]
        agent = WarehouseAgent(trivial_map)
        path, directions, states_expanded = agent.find_path()

        self.assertIsNotNone(path)
        self.assertEqual(len(directions), 1)
        self.assertEqual(directions[0], "Right")
        self.assertEqual(path, [(1, 1), (1, 2)])

    def test_unreachable_goal(self):
        """Test behavior when goal G is completely walled off."""
        unreachable_map = [
            "######",
            "#S.#G#",
            "#..###",
            "######"
        ]
        agent = WarehouseAgent(unreachable_map)
        path, directions, states_expanded = agent.find_path()

        self.assertIsNone(path, "Path should be None when goal is unreachable.")
        self.assertIsNone(directions, "Directions should be None when goal is unreachable.")
        self.assertGreater(states_expanded, 0, "Search should still expand accessible states.")

    def test_no_obstacle_traversal(self):
        """Check that no coordinate in the solution path is an obstacle '#'."""
        agent = WarehouseAgent(DEFAULT_MAP)
        path, _, _ = agent.find_path()

        self.assertIsNotNone(path)
        for r, c in path:
            cell_char = agent.grid[r][c]
            self.assertNotEqual(
                cell_char, '#',
                f"Path contains obstacle '#' at position ({r}, {c})"
            )

    def test_valid_single_steps(self):
        """Check that every step in the path moves exactly one cell orthogonally."""
        agent = WarehouseAgent(DEFAULT_MAP)
        path, directions, _ = agent.find_path()

        self.assertIsNotNone(path)
        self.assertEqual(len(path) - 1, len(directions), "Path length - 1 must match directions count.")

        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i + 1]
            manhattan_dist = abs(r1 - r2) + abs(c1 - c2)
            self.assertEqual(
                manhattan_dist, 1,
                f"Step from {path[i]} to {path[i+1]} is not a single orthogonal move (distance={manhattan_dist})."
            )


if __name__ == "__main__":
    unittest.main()
