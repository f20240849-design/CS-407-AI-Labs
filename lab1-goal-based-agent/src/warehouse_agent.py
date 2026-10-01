"""
Warehouse Agent Implementation
------------------------------
This module implements a Goal-Based Agent for autonomous warehouse navigation.
The agent operates on a 2D grid environment containing obstacles ('#'), a starting
location ('S'), and a goal location ('G').

Algorithm Selection:
-------------------
Breadth-First Search (BFS) is chosen for this goal-based agent.
Why BFS is appropriate:
1. Completeness: BFS guarantees finding a solution if one exists on a finite grid.
2. Optimality: Because every step (move) has an equal cost of 1 grid unit, BFS
   guarantees finding the shortest collision-free path from S to G.
3. Goal-Based Architecture: The agent explicitly maintains the target goal state (G),
   evaluates candidate states against this goal, and plans a path of actions (Up, Down,
   Left, Right) to reach it.

Note on LLM Generation:
-----------------------
Code generated with assistance from LLM, verified and structured for standard Python 3.
"""

from collections import deque
from typing import List, Tuple, Optional, Dict, Set


DEFAULT_MAP = [
    "#####################",
    "#S....#............G#",
    "#.##....##########..#",
    "#....##.............#",
    "#.######.###.#.###..#",
    "#........#..........#",
    "#####################"
]


class WarehouseAgent:
    """
    Goal-Based Agent for navigating a 2D warehouse grid map.
    """

    # Movement directions: (delta_row, delta_col) and action names
    OFFSETS: Dict[str, Tuple[int, int]] = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    def __init__(self, grid_map: Optional[List[str]] = None):
        """
        Initialize the agent with a grid map.
        
        :param grid_map: List of strings representing the grid layout.
        """
        self.grid = [list(row) for row in (grid_map if grid_map is not None else DEFAULT_MAP)]
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.height > 0 else 0
        self.start_pos: Optional[Tuple[int, int]] = None
        self.goal_pos: Optional[Tuple[int, int]] = None
        
        self._parse_map()

    def _parse_map(self) -> None:
        """Locate start ('S') and goal ('G') positions in the grid."""
        for r in range(self.height):
            for c in range(self.width):
                char = self.grid[r][c]
                if char == 'S':
                    self.start_pos = (r, c)
                elif char == 'G':
                    self.goal_pos = (r, c)
        
        if self.start_pos is None:
            raise ValueError("Map missing starting position 'S'.")
        if self.goal_pos is None:
            raise ValueError("Map missing goal position 'G'.")

    def is_valid_cell(self, row: int, col: int) -> bool:
        """Check if coordinates are within bounds and not an obstacle ('#')."""
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col] != '#'
        return False

    def find_path(self) -> Tuple[Optional[List[Tuple[int, int]]], Optional[List[str]], int]:
        """
        Find a collision-free path from S to G using Breadth-First Search (BFS).

        :return: Tuple containing:
                 - path: List of (row, col) coordinates from S to G (or None if no path exists)
                 - directions: List of action strings ["Up", "Right", ...] (or None)
                 - states_expanded: Total number of states (cells) expanded during search
        """
        start = self.start_pos
        goal = self.goal_pos

        # Queue storing (current_row, current_col)
        queue: deque = deque([start])
        
        # Parent mapping: (r, c) -> ((parent_r, parent_c), direction_from_parent)
        parent: Dict[Tuple[int, int], Tuple[Optional[Tuple[int, int]], Optional[str]]] = {
            start: (None, None)
        }
        
        visited: Set[Tuple[int, int]] = {start}
        states_expanded = 0

        path_found = False

        while queue:
            curr_r, curr_c = queue.popleft()
            states_expanded += 1

            if (curr_r, curr_c) == goal:
                path_found = True
                break

            # Explore 4 orthogonal neighbors
            for action_name, (dr, dc) in self.OFFSETS.items():
                nr, nc = curr_r + dr, curr_c + dc
                if self.is_valid_cell(nr, nc) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = ((curr_r, curr_c), action_name)
                    queue.append((nr, nc))

        if not path_found:
            return None, None, states_expanded

        # Reconstruct path and actions
        path_coords: List[Tuple[int, int]] = []
        directions: List[str] = []
        
        curr: Optional[Tuple[int, int]] = goal
        while curr is not None:
            path_coords.append(curr)
            prev_node, action = parent[curr]
            if action is not None:
                directions.append(action)
            curr = prev_node

        path_coords.reverse()
        directions.reverse()

        return path_coords, directions, states_expanded

    def render_map_with_path(self, path: List[Tuple[int, int]]) -> str:
        """
        Generate a text visualization of the grid map overlaid with the path.
        Path cells (excluding S and G) are rendered as '*'.
        """
        grid_copy = [row[:] for row in self.grid]
        path_set = set(path)
        
        for r, c in path_set:
            if (r, c) != self.start_pos and (r, c) != self.goal_pos:
                grid_copy[r][c] = '*'
                
        return "\n".join("".join(row) for row in grid_copy)


def main():
    print("=" * 60)
    print("       Goal-Based Agent Warehouse Pathfinding Demo")
    print("=" * 60)

    agent = WarehouseAgent()
    path, directions, states_expanded = agent.find_path()

    if path is not None and directions is not None:
        print(f"\n[+] Solution Found!")
        print(f"Path Length (steps): {len(directions)}")
        print(f"Total Nodes/States Expanded: {states_expanded}")
        print("\nDirection Sequence:")
        print(" -> ".join(directions))
        print("\nCoordinate Path (Row, Column):")
        print(path)
        print("\nWarehouse Map with Solution Path ('*' marks path):")
        print(agent.render_map_with_path(path))
    else:
        print("\n[-] No collision-free path exists from S to G.")
        print(f"States Expanded: {states_expanded}")
    print("=" * 60)


if __name__ == "__main__":
    main()
