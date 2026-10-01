# Prompt Documentation: Logical Planner (`prompts/planner_prompt.md`)

This file records the original prompt given in Task 2 of the laboratory exercise, alongside an improved production-grade prompt and engineering analysis of the differences.

---

## 1. Task 2 Verbatim Prompt

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

---

## 2. Improved Production-Grade Prompt

```text
I want to implement a robust, production-grade classical planning agent in Python 3.10+ using first-order proposition sets and Breadth-First Search (BFS).

Please structure the code cleanly across two files: `src/planner.py` and `tests/test_planner.py`.

### Architectural Specifications:
1. **State Representation**:
   - Represent states as Python `frozenset` objects containing string propositions (e.g., `frozenset({"At(Robot, A)", "At(Package, A)"})`) to enable hashability, immutability, and O(1) set operations under the Closed-World Assumption.

2. **Action Class**:
   - Define an `Action` class storing: `name` (str), `pos_pre` (frozenset), `neg_pre` (frozenset), `pos_eff` (frozenset), and `neg_eff` (frozenset).
   - Implement `applicable(state: frozenset) -> bool`: Return True iff `pos_pre <= state` AND `len(neg_pre & state) == 0`.
   - Implement `apply(state: frozenset) -> frozenset`: Return `(state - neg_eff) | pos_eff`. Raise `ValueError` if not applicable.

3. **Search Algorithm**:
   - Implement `bfs_plan(initial_state: frozenset, goal_state: frozenset, actions: List[Action]) -> Tuple[Optional[List[Action]], List[frozenset]]`.
   - Use `collections.deque` for FIFO queue management and a `visited` set of `frozensets` to prevent duplicate state expansion and infinite loops.
   - Goal check condition: `goal_state.issubset(current_state)`.
   - Handle unsolvable domains cleanly by returning `(None, [])`.

4. **Independent Verifier & Testing**:
   - In `tests/test_planner.py`, implement an independent function `validate_plan(initial_state, goal_state, plan, actions_dict)` that re-simulates state transitions step-by-step from `initial_state`, explicitly validating preconditions before each step and checking final goal satisfaction.
   - Include test suites for:
     a) Solvable warehouse problem (Robot transports package from A to C).
     b) Unsolvable problem (PickUp action removed; must detect "No plan found").
     c) Goal distinction test (Verify `At(Robot, C)` does NOT satisfy `At(Package, C)`).

5. **Documentation & Traceability**:
   - Annotate code with explicit markers for `[Preconditions]`, `[Effects]`, `[Goal]`, and `[BFS]`.
   - Print state transitions cleanly with step numbers and sorted proposition sets.
```

---

## 3. Engineering Commentary: Why the Improved Version is Better

| Evaluation Dimension | Original Task 2 Prompt | Improved Prompt |
| :--- | :--- | :--- |
| **Data Structures** | Mentions generic "set of logical propositions". LLM might use mutable `set()`, causing unhashable type errors when storing states in `visited`. | Explicitly requires `frozenset`, guaranteeing hashability for `visited` sets and BFS queues. |
| **Precondition Checking** | Mentions "preconditions satisfied". Might lead to loose checking. | Explicitly specifies set logic: `pos_pre <= state` and `len(neg_pre & state) == 0`. |
| **Verification & Quality** | Only asks for code generation. | Requests an **independent verifier function** and edge-case unit tests (unsolvable & goal distinction). |
| **Error Handling** | Does not specify runtime behavior for invalid actions. | Requires explicit `ValueError` raising on illegal transitions and clean `(None, [])` returns for unsolvable problems. |
| **Type Safety** | No type hints requested. | Enforces Python 3.10+ type annotations (`FrozenSet`, `List`, `Tuple`, `Optional`). |
