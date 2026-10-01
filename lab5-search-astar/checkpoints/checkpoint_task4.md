# Checkpoint Task 4: Code Mapping & Search Theory Analysis

This document maps theoretical search concepts directly to exact function names and line numbers in [src/astar.py](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py) and provides answers to conceptual questions (a)–(e).

---

## 1. Code Mapping Table ([src/astar.py](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py))

| Search Concept | Function Name | Exact Line Numbers in `src/astar.py` | Description / Implementation Detail |
| :--- | :--- | :--- | :--- |
| **State Representation** | `astar_search` | [L63, L92, L101](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L63) | 0-indexed integer coordinate tuples `(row, col)` representing agent location. |
| **Action & Transition** | `get_neighbors` | [L31–L47](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L31-L47) | Iterates over `[(-1,0), (1,0), (0,-1), (0,1)]` (Up, Down, Left, Right) to compute passable adjacent cells. |
| **Goal Test** | `astar_search` | [L83–L90](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L83-L90) | Checks `if current == goal:` when expanding node popped from frontier. |
| **Path Cost $g(n)$** | `astar_search` | [L67, L93, L96](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L67) | Dictionary `g_score` tracking accumulated step cost from start (`tentative_g = g_score[current] + 1`). |
| **Heuristic $h(n)$** | `manhattan_distance` | [L16–L18, L61, L98](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L16-L18) | Pluggable heuristic function computing $|r_1 - r_2| + |c_1 - c_2|$ estimated remaining cost to goal. |
| **Evaluation Function $f(n)$** | `astar_search` | [L62, L99](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L62) | Calculates total priority $f(n) = g(n) + h(n)$ for ordering nodes in priority queue. |
| **Frontier (Open List)** | `astar_search` | [L65, L73, L101](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L65) | Priority min-heap list `frontier` storing `(f, h, counter, node)` tuples managed via `heapq`. |
| **Visited States (Closed Set)** | `astar_search` | [L69, L76, L79](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L69) | Set `closed_set` tracking expanded states to prevent duplicate exploration. |
| **Path Reconstruction** | `astar_search` | [L68, L84–L90, L97](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L68) | Dictionary `parent` back-pointers traversed from `goal` to `start` when goal test passes. |

---

## 2. Conceptual Questions & Answers

### (a) How does $f(n) = g(n) + h(n)$ guide the search?
$f(n)$ balances past path cost ($g(n)$) against estimated future cost ($h(n)$). $g(n)$ keeps the search grounded by penalizing long, winding paths, while $h(n)$ provides a goal-directed bias towards the target coordinate. By expanding nodes with minimal $f(n)$ first, A* avoids exploring paths that are already known to be longer than the current best estimate to the goal.

### (b) What role does `heapq` play in prioritizing node expansion?
`heapq` implements a binary min-heap data structure that provides $O(1)$ time complexity for accessing the node with the lowest $f(n)$ value and $O(\log N)$ time for pushing new nodes or popping the minimum node. This guarantees that search expansion strictly adheres to best-first node ordering without requiring expensive $O(N)$ list sorts.

### (c) Why is a `closed_set` (visited set) necessary, and what happens without it?
A `closed_set` is necessary to prevent cyclic re-expansion of previously processed states. Without a `closed_set` on a grid with non-directional edges, the search algorithm would fall into infinite loops bouncing back and forth between adjacent states (e.g., $(1, 1) \leftrightarrow (1, 2)$) or exponentially re-expand identical subgraphs, causing infinite runtime or memory exhaustion.

### (d) How does parent pointer tracking enable path reconstruction?
During search expansion, whenever a shorter path to neighbor $n'$ is discovered from current node $n$, the algorithm stores `parent[n'] = n` ([L97](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L97)). Once the goal $G$ is reached, the path is reconstructed by following predecessor links backwards from $G$ to $s_0$ (`curr = parent[curr]`, [L88](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L88)) and reversing the list ([L89](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L89)).

### (e) What happens when a duplicate/stale node is popped from the priority queue?
Because Python's `heapq` does not support efficient in-place priority updates (`decrease-key`), finding a shorter path to a node already in the frontier results in pushing a new tuple with a smaller $f(n)$ value. Consequently, the old, higher-cost tuple remains in the queue as a "stale" entry. When popped later at [L73](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L73), the check `if current in closed_set:` at [L76](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py#L76) immediately detects that the node was already processed via the shorter path, executing `continue` to discard the stale pop without incrementing `states_expanded`.

---

## Evidence

Line numbers verified directly against [src/astar.py](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py). All functions compile and run cleanly in Python 3.
