# Prompts Used for A* Search Implementation

This document contains the exact prompts used during the engineering workflow to generate and refine the Python A* search algorithm.

---

## 1. Verbatim Example Prompt from Lab Sheet

> Write Python code for A* search on a 2D grid. The map is given as a list of strings with '#' for walls, '.' for open space, 'S' for start, 'G' for goal. Return the path from S to G and total cost.

---

## 2. Refined Prompt Based on Task 1 Agent Design

> Write a Python function `astar_search(grid, start, goal, heuristic_func=manhattan_distance)` that executes A* search on a 2D grid represented as a list of strings where '#' denotes walls, '.' open space, 'S' start, and 'G' goal.
> 
> Enforce the following strict determinism and architectural requirements:
> 1. Represent states as 0-indexed `(row, col)` tuples with `(0, 0)` at the top-left corner.
> 2. Neighbor generation must explore directions in the strict order: Up `(-1, 0)`, Down `(+1, 0)`, Left `(0, -1)`, Right `(0, +1)`.
> 3. Use Python's `heapq` module for the priority queue frontier. Store entries as 4-tuples: `(f_score, h_score, tie_breaker_counter, node)` where `tie_breaker_counter` is an incrementing integer to handle identical $f$ and $h$ values deterministically without comparing tuple nodes directly.
> 4. Maintain explicit $g(n)$, $h(n)$, and $f(n) = g(n) + h(n)$ cost structures, parent pointers for path reconstruction, and a `closed_set` for expanded states.
> 5. Skip stale/duplicate frontier pops of already-closed states without incrementing the states expanded count.
> 6. Return a tuple `(found, path, path_length, states_expanded)` where:
>    - `found` is a boolean (`True` if goal reached, `False` otherwise).
>    - `path` is a list of `(row, col)` coordinates from `start` to `goal`, or `[]` if no path exists.
>    - `path_length` is an integer count of moves (`len(path) - 1`), or `0` if no path exists.
>    - `states_expanded` is the total integer count of unique nodes popped from the frontier and added to the closed set.

---

## 3. Justification Note: Why the Refined Version is Superior

The refined prompt is significantly better than the basic sheet prompt for the following key engineering reasons:

1. **Deterministic Reproducibility**: By specifying the exact tie-breaking order (`tie_breaker_counter`), neighbor expansion sequence (Up, Down, Left, Right), and state expansion counting criteria, the code produces 100% deterministic, reproducible outputs across different Python environments and runs.
2. **Explicit Data Contracts & Interface**: The basic prompt returns arbitrary types and structures. The refined prompt mandates an explicit return signature `(found, path, path_length, states_expanded)` and standardized state representation `(row, col)` matching unit testing frameworks and comparison scripts.
3. **Pluggable Architecture**: The refined prompt introduces `heuristic_func` as a first-class parameter, enabling seamless switching between Manhattan, Euclidean, Zero ($h=0$), and Weighted heuristics without modifying algorithm core logic.
4. **Edge Case Handling**: It explicitly specifies how stale pops from the priority queue must be skipped and how unreachable goals must report `False` and terminate gracefully without infinite loops or runtime crashes.
