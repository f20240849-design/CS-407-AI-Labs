# Checkpoint Task 5: BFS vs A* Comparison & Map Topology Analysis

This document presents the empirical comparative evaluation of **Breadth-First Search (BFS)** versus **A* Search (Manhattan Heuristic)** on the original 17×9 warehouse map.

---

## 1. BFS vs A* Comparison Table

Data imported directly from [results/comparison.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/results/comparison.md):

| Metric | Breadth-First Search (BFS) | A* Search (Manhattan Heuristic) |
| :--- | :---: | :---: |
| **Solution Found** | Yes | Yes |
| **Path Length (Moves)** | 40 | 40 |
| **States Expanded** | 64 | 64 |

---

## 2. Questions & Answers

### (a) Did both algorithms find an optimal path?
Yes. Both BFS and A* found an optimal path of exactly **40 moves** between start `(1, 1)` and goal `(7, 15)`. BFS guarantees optimality on unweighted graphs because it explores nodes in increasing order of path depth $g(n)$. A* guarantees optimality because it uses the Manhattan distance heuristic, which is admissible ($h(n) \le h^*(n)$).

### (b) Did A* expand fewer states than BFS? Explain why.
No. On this specific warehouse map, A* expanded **64 states**, which is **identical** to the 64 states expanded by BFS. 

**Honest Topological Explanation**:
This warehouse map features a highly constrained, single corridor-like route with dead-end alcoves. Out of the 153 total grid cells ($17 \times 9$), exactly 64 cells are passable open space, and all 64 cells lie along the mandatory pathway connecting start `(1, 1)` to goal `(7, 15)`. Because the goal is located at the far bottom-right corner `(7, 15)` at the terminal end of this single winding corridor, **every single passable cell in the maze must be visited to reach the goal**. Thus, heuristic distance guidance cannot prune any branch, forcing both BFS and A* to explore all 64 reachable states.

### (c) How does the heuristic function reduce the search space in general?
In open or multi-path domains, the heuristic function $h(n)$ acts as a compass by estimating remaining distance to the goal. By adding $h(n)$ to $g(n)$, A* assigns lower $f(n)$ values to nodes that move spatially closer to the goal. Consequently, A* expands nodes expanding toward the target while deferring expansion of nodes heading in opposite or irrelevant directions, pruning large regions of the search space.

### (d) Under what map conditions does A* provide maximum efficiency gains over BFS?
A* provides maximum efficiency gains over BFS under the following domain conditions:
1. **Open, Unconstrained Grids / Large Branching Factor**: Wide open spaces where BFS expands an expanding concentric circle (or sphere) of states in all directions ($O(b^d)$).
2. **Multiple Parallel Paths**: Maps offering multiple alternative routes, allowing A* to prioritize the path leading straight toward the target.
3. **High Heuristic Accuracy**: Environments where Manhattan or Euclidean distance closely mirrors actual traversal cost without huge wall blockages perpendicular to goal direction.

---

## 3. Think About It

> **Question**: What information does A* use that BFS ignores, and how does this affect search efficiency across different domain topologies?

**Answer**:
BFS operates using **only historical path cost** $g(n)$ (node depth in unweighted graphs), treating all frontier nodes at depth $d$ equally regardless of whether they move closer to or further from the goal. 

A* incorporates **domain-specific future guidance** via the heuristic $h(n)$, evaluating nodes on total projected cost $f(n) = g(n) + h(n)$. 
- In **open topologies**, this future information concentrates search along a narrow cone toward the goal, dramatically reducing state expansions compared to BFS's radial expansion.
- In **single-corridor topologies** (like Map 1), spatial heuristic information is constrained by physical maze walls; when the physical path turns away from the goal to navigate around a wall, $h(n)$ increases while remaining the only valid option, neutralizing A*'s pruning advantage.

---

## Evidence

Output verified via `src/compare_bfs_astar.py` and recorded in [results/comparison.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/results/comparison.md):
```text
BFS -> Found: True, Length: 40, Expanded: 64
A*  -> Found: True, Length: 40, Expanded: 64
Paths match exactly: True
```
