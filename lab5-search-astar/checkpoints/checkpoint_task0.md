# Checkpoint Task 0: Problem Formulation

## Formal 6-Tuple Problem Formulation

| Component | Formal Notation / Mathematical Definition | Description in Warehouse Context |
| :--- | :--- | :--- |
| **State Space ($S$)** | $S = \{(r, c) \mid 0 \le r < R, 0 \le c < C, \text{grid}[r][c] \neq \text{'\#'}\}$ | The set of all valid, passable 2D grid coordinates $(r, c)$ in the warehouse. |
| **Action Space ($A$)** | $A = \{\text{Up}, \text{Down}, \text{Left}, \text{Right}\}$ | The 4-directional cardinal moves available to the robot: Up $(-1, 0)$, Down $(+1, 0)$, Left $(0, -1)$, Right $(0, +1)$. |
| **Transition Function ($T$)** | $T(s, a) = s' = (r + dr, c + dc)$ if $s' \in S$, else $s$ | Deterministic state transition resulting from executing action $a \in A$ at state $s$. If blocked by wall '\#', robot remains in $s$. |
| **Initial State ($s_0$)** | $s_0 = (1, 1)$ | The starting coordinate of the robot marked by 'S' in the grid. |
| **Goal Test ($G$)** | $G(s) = \text{True}$ if $s = (7, 15)$, else $\text{False}$ | Predicate returning True when the current state $s$ equals goal coordinate marked by 'G'. |
| **Step Cost ($c$)** | $c(s, a, s') = 1$ for all valid transitions | Uniform unit step cost of 1 for every single-cell move. |

---

## Task 0 Questions & Answers

### (a) How is the warehouse map represented as a search state space?
The warehouse map is represented as a 2D discrete coordinate grid where each state is a pair of 0-indexed integers $s = (r, c)$. Impassable obstacles (walls '#') are excluded from $S$, leaving only navigable cells (open space '.', start 'S', and goal 'G') as valid states in the search space graph.

### (b) What are the valid actions, and how do they change the agent's state?
The valid actions are $A = \{\text{Up}, \text{Down}, \text{Left}, \text{Right}\}$. Executing action $a \in A$ adds a direction vector $(dr, dc) \in \{(-1, 0), (1, 0), (0, -1), (0, 1)\}$ to the current position $(r, c)$, producing new state $s' = (r + dr, c + dc)$ provided $s' \in S$.

### (c) What is the initial state and goal condition for the given map?
- **Initial state ($s_0$)**: $(1, 1)$, corresponding to row 1, column 1 where character 'S' is located.
- **Goal condition ($G$)**: $s = (7, 15)$, corresponding to row 7, column 15 where character 'G' is located.

### (d) What is the path cost function?
The path cost function $g(n)$ is the sum of step costs along the sequence of actions from $s_0$ to state $n$. Since every single movement between adjacent passable cells has cost $c = 1$, the path cost $g(n)$ equals the number of moves (edge transitions) in the path.

---

## Think About It

> **Question**: Why is standard state representation as $(r, c)$ sufficient for this warehouse domain, and when would state representation need to expand (e.g., to include orientation or payload state)?

**Answer**:
A simple coordinate tuple $s = (r, c)$ is sufficient here because the agent is modeled as a point robot with instantaneous 4-directional turning (zero turn cost), unlimited carrying capacity, and no directional momentum or orientation constraints. 

State representation would need to expand under the following real-world engineering constraints:
1. **Robot Orientation & Turning Costs**: If turning left/right requires a discrete move or time cost, state must expand to $s = (r, c, \theta)$ where $\theta \in \{\text{N}, \text{S}, \text{E}, \text{W}\}$.
2. **Payload / Carrying Status**: If the robot must pick up an item at location $P$ before delivering it to goal $G$, state must expand to $s = (r, c, \text{has\_item})$ where $\text{has\_item} \in \{\text{True}, \text{False}\}$.
3. **Battery / Energy Limits**: If the robot has finite battery life requiring recharging stops, state must include current charge $s = (r, c, \text{battery\_level})$.

---

## Evidence

The map parsing logic in `src/astar.py` and `src/bfs.py` extracts $s_0$ and $G$ dynamically as verified by test output:
```text
Start Position: (1, 1), Goal Position: (7, 15)
Grid Dimensions: 17 columns x 9 rows (153 total cells, 64 navigable states)
```
