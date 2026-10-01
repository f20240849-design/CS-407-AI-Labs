# Checkpoint Task 6: Heuristic Investigation & Admissibility Analysis

This document evaluates the performance of four heuristic functions on Map 1 using [src/heuristic_experiments.py](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/heuristic_experiments.py).

---

## 1. Rationale: Why Manhattan Distance is Appropriate for 4-Directional Movement

Manhattan distance $h_{\text{Manhattan}}(p_1, p_2) = |r_1 - r_2| + |c_1 - c_2|$ measures the exact grid distance between two points when movement is restricted strictly to 4 cardinal directions (Up, Down, Left, Right) without diagonal steps. 

On an obstacle-free 4-connected grid with unit step cost $c=1$, Manhattan distance equals the exact shortest path cost $h^*(n)$. When walls/obstacles are introduced, the actual shortest path cost can only increase ($h^*(n) \ge h_{\text{Manhattan}}(n)$). Thus, Manhattan distance is inherently **admissible** ($h(n) \le h^*(n)$) and **consistent** (monotonic), making it the mathematically ideal baseline heuristic for 4-directional grid search.

---

## 2. Experimental Results Table

Data imported directly from [results/heuristics.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/results/heuristics.md):

| Heuristic Variant | Formula / Description | Solution Found | Path Length (Moves) | States Expanded | Admissibility Status |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **$h_0 = 0$ (Dijkstra)** | $h(n) = 0$ | Yes | 40 | 64 | **Admissible** ($0 \le h^*(n)$) |
| **Manhattan Distance** | $\|r_1 - r_2\| + \|c_1 - c_2\|$ | Yes | 40 | 64 | **Admissible** ($h(n) \le h^*(n)$) |
| **Euclidean Distance** | $\sqrt{(r_1 - r_2)^2 + (c_1 - c_2)^2}$ | Yes | 40 | 64 | **Admissible** ($h_{\text{Euc}} \le h_{\text{Man}} \le h^*$) |
| **$2 \times \text{Manhattan}$** | $2 \cdot (|r_1 - r_2| + |c_1 - c_2|)$ | Yes | 40 | 64 | **Inadmissible** ($h(n) > h^*(n)$) |

---

## 3. Discussion of Admissibility & Empirical Findings

### Theoretical Admissibility Definition
A heuristic $h(n)$ is **admissible** if it never overestimates the true minimum cost to reach the goal from state $n$:
$$h(n) \le h^*(n) \quad \forall n \in S$$
- **$h(n) = 0$**: Admissible. $0 \le h^*(n)$ always holds since edge costs are non-negative.
- **Manhattan Distance**: Admissible. Represents minimum grid steps without obstacles.
- **Euclidean Distance**: Admissible. Straight-line distance is the shortest possible spatial distance in Euclidean space, satisfying $h_{\text{Euclidean}}(n) \le h_{\text{Manhattan}}(n) \le h^*(n)$.
- **$2 \times \text{Manhattan}$**: **Inadmissible**. For any state $n$ where $h^*(n) > 0$, multiplying by 2 causes $h(n) > h^*(n)$ (e.g., at start $s_0$, $h_{\text{Manhattan}} = 20$ while true cost $h^* = 40$; doubling gives $h = 40$, but near goal at distance 5, $2 \times 5 = 10 > 5$).

### Empirical Behavior on Map 1
On this specific warehouse map, **all four heuristic variants—including the inadmissible $2 \times \text{Manhattan}$ heuristic—returned an optimal path of length 40 and expanded 64 states**.

**Key Insight on Inadmissibility**:
Saying a heuristic is *inadmissible* means that A* is **no longer mathematically guaranteed** to find an optimal path in all possible graphs; it **does NOT mean it will always fail to find an optimal path**. 

On Map 1, because the maze topology provides only a single continuous corridor with no shorter shortcut bypasses, there are no suboptimal alternative paths for the greedy $2 \times \text{Manhattan}$ heuristic to be misdirected into choosing. Therefore, even though $2 \times \text{Manhattan}$ overestimates remaining costs, it still finds the optimal 40-move path.

---

## Evidence

Output verified via `src/heuristic_experiments.py` and logged in [results/heuristics.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/results/heuristics.md).
