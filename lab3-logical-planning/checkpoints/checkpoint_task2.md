# Checkpoint Task 2: Ask an LLM to Implement the Planner

**Student Name:** AI Undergraduate Student  
**Lab Assignment:** Laboratory – Logical Reasoning for Planning  

---

## 1. Prompt Specification

The prompt used to construct the planning engine is recorded in [planner_prompt.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/prompts/planner_prompt.md).

```text
I want to implement a simple planning agent in Python.
Represent a state as a set of logical propositions.
Each action should contain:
• a name;
• positive preconditions;
• negative preconditions;
• positive effects;
• negative effects.
An action is applicable if all of its preconditions are satisfied by the current state.
When an action is applied:
1. remove its negative effects from the state;
2. add its positive effects to the state.
Use breadth-first search to find a sequence of actions that achieves a specified goal.
The program should also:
• detect when no plan exists;
• print the resulting sequence of actions;
• print the states reached after each action.
Explain the implementation and identify any assumptions you make.
```

The generated code is saved in [planner.py](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/src/planner.py).

---

## 2. Specification-to-Code Mapping Table (Think About It)

| Core Specification Concept | Python Implementation Method / Function | Code Location | Logical Description |
| :--- | :--- | :--- | :--- |
| **Preconditions** | `Action.applicable(state)` | [planner.py:L26-L32](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/src/planner.py#L26-L32) | Evaluates whether $S \models \text{Preconditions}(a)$ by checking `pos_pre.issubset(state)` and `len(neg_pre & state) == 0`. |
| **Effects** | `Action.apply(state)` | [planner.py:L35-L45](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/src/planner.py#L35-L45) | Computes $S' = (S \setminus \text{neg\_eff}) \cup \text{pos\_eff}$ using Python set subtraction and union. |
| **Goal** | `bfs_plan()` Goal Check | [planner.py:L60-L62, L78-L82](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/src/planner.py#L60-L62) | Checks if goal propositions are satisfied in state $S$: `goal_state.issubset(current_state)`. |
| **BFS Search** | `bfs_plan()` Loop | [planner.py:L49-L95](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/src/planner.py#L49-L95) | Explores action sequences level-by-level using `collections.deque` and `visited` set of `frozensets`. |

---

## 3. Underlying Planning Assumptions

The planner implementation relies on the following fundamental classical planning assumptions:

1. **Closed-World Assumption (CWA):** Any proposition not explicitly present in a state set is assumed to be **false**.
2. **Deterministic Actions:** Action execution is guaranteed to succeed and results in an exact, predictable successor state without uncertainty.
3. **Full Observability:** The agent has complete and accurate knowledge of the current state of the world at all times.
4. **Static Environment:** The world changes **only** as a direct result of the robot's actions. No external agents or dynamic events occur concurrently.
5. **Discrete Step & Uniform Cost:** Time is discretized into action steps, and every action has an equal step cost of 1.

---

## 4. Evidence Trace

```text
Class Action:
  - applicable(): pos_pre.issubset(state) and len(neg_pre.intersection(state)) == 0
  - apply(): (state - neg_eff) | pos_eff

Function bfs_plan():
  - Queue stores: (current_state, plan_path, state_history)
  - Visited set stores: frozenset of propositions
  - Goal check: goal_state.issubset(next_state)
```
