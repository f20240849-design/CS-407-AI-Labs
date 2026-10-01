# Search Algorithm Comparison: BFS vs A*

This document presents the empirical comparison between **Breadth-First Search (BFS)** and **A* Search (Manhattan Heuristic)** on the original 17×9 warehouse map.

## Empirical Comparison Table

| Metric | Breadth-First Search (BFS) | A* Search (Manhattan) |
| :--- | :--- | :--- |
| **Solution Found** | Yes | Yes |
| **Path Length (Moves)** | 40 | 40 |
| **States Expanded** | 64 | 64 |

## Path Verification

- **BFS Path**: `[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (4, 13), (3, 13), (3, 12), (3, 11), (3, 10), (3, 9), (3, 8), (3, 7), (2, 7), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15)]`
- **A* Path**: `[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (4, 13), (3, 13), (3, 12), (3, 11), (3, 10), (3, 9), (3, 8), (3, 7), (2, 7), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15)]`
- **Paths Identical**: True

## Analysis of Results

1. **Optimality**: Both BFS and A* (with an admissible Manhattan heuristic) successfully find the optimal shortest path of length **40** moves.
2. **State Expansions**: On this specific warehouse map, both algorithms expand exactly **64 states**. This occurs because the warehouse map consists of a highly constrained single corridor with dead-end alcoves. Since the start is at `(1, 1)` and the goal is at `(7, 15)`, every reachable cell on the map (64 cells total) must be explored to reach the goal, regardless of heuristic guidance.
3. **Efficiency**: While A* utilizes goal directionality via $h(n)$, grid constraint topology dominates search space exploration in single-corridor mazes.
