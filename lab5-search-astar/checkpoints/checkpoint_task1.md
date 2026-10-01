# Checkpoint Task 1: Agent Design (Pre-LLM Specification)

This document details my explicit architectural design for the A* search agent, created **before** constructing prompts for LLM code generation.

---

## Pre-LLM Agent Design (6 Core Specification Points)

### 1. State Representation
States are represented as 2-element tuple integers `(row, col)` using 0-indexed coordinates, where `(0, 0)` is the top-left corner of the grid map matrix. `row` increases downwards, and `col` increases rightwards.

### 2. Warehouse Representation
The warehouse grid is represented as a list of ASCII strings (`list[str]`). Wall cells `'#'` are impassable barriers. Navigable cells are open space `'.'`, start position `'S'`, and goal location `'G'`.

### 3. Valid Actions & Neighbor Generation
From any current state $(r, c)$, valid actions attempt movement to adjacent cells in 4 cardinal directions. Neighbor generation follows the strict deterministic ordering:
1. **Up**: `(r - 1, c)`
2. **Down**: `(r + 1, c)`
3. **Left**: `(r, c - 1)`
4. **Right**: `(r, c + 1)`

Movement is valid if and only if the candidate neighbor is within grid boundary bounds ($0 \le r < \text{rows}$, $0 \le c < \text{cols}$) and is not a wall (`grid[r][c] != '#'`).

### 4. Goal Recognition
Goal test is evaluated upon popping a node from the priority queue frontier. If `current_node == goal_node`, search immediately halts, triggers path reconstruction, and reports success.

### 5. Frontier Contents & Tie-Breaking
The priority queue frontier is implemented using Python's `heapq` module storing 4-tuples:
$$\text{frontier\_item} = (f(n), h(n), \text{counter}, n)$$
where:
- $f(n) = g(n) + h(n)$ is the priority key.
- $h(n)$ is the Manhattan distance heuristic $h((r_1, c_1), (r_2, c_2)) = |r_1 - r_2| + |c_1 - c_2|$.
- $\text{counter}$ is an auto-incrementing integer tie-breaker used when two nodes have identical $f(n)$ and $h(n)$ values, ensuring deterministic FIFO tie-breaking without attempting direct coordinate tuple comparisons.
- $n$ is the state coordinate `(row, col)`.

### 6. Path Reconstruction
A dictionary `parent = {start: None}` records the predecessor state for every reached node. When the goal is expanded, the agent backtracks from `goal` to `start` via parent pointers and reverses the list to form the forward path $[s_0, s_1, \dots, G]$.

---

## Output Metrics Reported by Program

The search program must return a structured 4-tuple: `(found, path, path_length, states_expanded)`:
1. **Solution Found (`found`)**: Boolean (`True` if goal reached, `False` if frontier empties without reaching goal).
2. **Path (`path`)**: Ordered list of `(row, col)` tuples from `start` to `goal` (empty list `[]` if no path).
3. **Path Length (`path_length`)**: Total edge count / move transitions $\text{len}(path) - 1$ (0 if no path).
4. **States Expanded (`states_expanded`)**: Total count of unique nodes popped from the frontier and added to `closed_set`. Duplicate/stale pops are skipped and not counted.

---

## Evidence

The design matches the implementation in `src/astar.py` [L1-L100](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L1-L100). When executed, the agent reports exact metrics:
```text
A* (Manhattan) -> Found: True, Length: 40, Expanded: 64
A* Path: [(1, 1), (1, 2), ..., (7, 15)]
```
