# Heuristic Investigation Results

This document details the comparative performance of A* Search using four different heuristic functions on the original 17×9 warehouse map.

## Performance Comparison Table

| Heuristic Variant | Solution Found | Path Length (Moves) | States Expanded | Admissibility Status |
| :--- | :---: | :---: | :---: | :--- |
| **h = 0 (Dijkstra)** | Yes | 40 | 64 | Admissible (h(n) = 0 <= h*(n)) |
| **Manhattan Distance** | Yes | 40 | 64 | Admissible (h(n) <= h*(n) for 4-dir move) |
| **Euclidean Distance** | Yes | 40 | 64 | Admissible (Straight-line <= Grid distance) |
| **2 × Manhattan Distance** | Yes | 40 | 64 | Inadmissible (Overestimates h*(n)) |

## Experimental Findings & Discussion

1. **Path Optimality Across All Variants**:
   - All four heuristics produced an optimal path of length **40** moves.
   - Even the inadmissible heuristic ($2 \times \text{Manhattan}$) returned an optimal path on this map. Inadmissibility ($h(n) > h^*(n)$) guarantees that A* *may* return a suboptimal path in general, but does not force it to do so when alternative pathways are constrained or absent.

2. **States Expanded Behavior**:
   - Every variant expanded exactly **64 states**.
   - **Explanation**: In this specific 17×9 maze topology, every passable cell lies along a mandatory single corridor or inside dead-end branches attached to that corridor. Because the goal $G$ at `(7, 15)` is positioned at the terminal end of the corridor, search algorithms must explore all 64 reachable grid cells before confirming goal reachability.

3. **Theoretical Implications**:
   - **$h(n) = 0$**: Equivalent to Dijkstra's algorithm / Uniform-Cost Search. Admissible and consistent.
   - **Manhattan Distance**: Perfect admissible heuristic for 4-directional grid movement without obstacles; remains admissible with obstacles.
   - **Euclidean Distance**: Admissible straight-line distance ($h_{Euclidean} \le h_{Manhattan} \le h^*$), but less informative than Manhattan on 4-connected grids.
   - **$2 \times \text{Manhattan}$**: Greedy/weighted A* behavior. Overestimates true cost ($h(n) = 2 \cdot h^*(n) > h^*(n)$), violating admissibility, but retains optimality here due to topological corridor constraints.
