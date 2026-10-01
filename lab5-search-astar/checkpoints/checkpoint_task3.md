# Checkpoint Task 3: Empirical Test Suite Verification

This document presents the detailed execution results for Tests 1 through 4 using the test harness [tests/test_search.py](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/tests/test_search.py).

---

## Test Results Breakdown

### Test 1: Original Warehouse Map (17×9 Maze)
- **Map Structure**: 17 columns × 9 rows maze grid with start at `(1, 1)` and goal at `(7, 15)`.
- **Solution Found**: `True`
- **Path Length (Moves)**: `40`
- **States Expanded**: `64`
- **Path**: `[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (4, 13), (3, 13), (3, 12), (3, 11), (3, 10), (3, 9), (3, 8), (3, 7), (2, 7), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15)]`
- **Expected Behavior**: Agent navigates around wall barriers to reach `(7, 15)` along the optimal route.
- **Status**: `PASS`

---

### Test 2: Trivial Map
- **Map Structure**: `#####` / `#SG##` / `#####` with start at `(1, 1)` and goal at `(1, 2)`.
- **Solution Found**: `True`
- **Path Length (Moves)**: `1`
- **States Expanded**: `2` (Expands `(1, 1)`, then expands `(1, 2)`)
- **Path**: `[(1, 1), (1, 2)]`
- **Expected Behavior**: Immediately discovers adjacent goal in 1 move with minimal state expansions.
- **Status**: `PASS`

---

### Test 3: Unreachable Goal Map
- **Map Structure**: `#######` / `#S....#` / `###.###` / `#...#G#` / `#######` with goal wall-bounded.
- **Solution Found**: `False`
- **Path Length (Moves)**: `0`
- **States Expanded**: `9` (Expands all 9 reachable states in start component before frontier empties)
- **Path**: `[]`
- **Expected Behavior**: Gracefully exhausts frontier without crashing, reports `found=False`, and returns length 0.
- **Status**: `PASS`

---

### Test 4: Multi-Path Map (Optimality Check)
- **Map Structure**: Grid with top path (cost 4) and bottom path (cost 6) between start `(1, 1)` and goal `(1, 5)`.
- **A* Result**: Solution Found=`True`, Path Length=`4`, States Expanded=`5`, Path=`[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]`.
- **BFS Result**: Solution Found=`True`, Path Length=`4`, States Expanded=`9`, Path=`[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]`.
- **Optimality Check**: A* returns path length 4, which equals the BFS shortest path length 4. Furthermore, A* expands fewer states (5 vs 9) due to heuristic goal bias towards the top path.
- **Expected Behavior**: A* finds the globally optimal shortest path.
- **Status**: `PASS`

---

## Summary Matrix

| Test ID | Map Description | Expected Outcome | Actual Outcome | Path Length | States Expanded | Test Status |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **Test 1** | Original 17x9 Maze | Optimal Path Found | Path Found | 40 | 64 | **PASS** |
| **Test 2** | Trivial Direct Goal | Single Step Found | Path Found | 1 | 2 | **PASS** |
| **Test 3** | Unreachable Goal | Graceful Failure | Failure Reported | 0 | 9 | **PASS** |
| **Test 4** | Multi-Path Map | Shortest Path | Shortest Path | 4 | 5 | **PASS** |

---

## Evidence

Full console output log captured in [results/test_output.txt](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/results/test_output.txt).
