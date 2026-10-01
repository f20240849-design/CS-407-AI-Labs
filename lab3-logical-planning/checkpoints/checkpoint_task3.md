# Checkpoint Task 3: Test the Generated Planner

**Student Name:** AI Undergraduate Student  
**Lab Assignment:** Laboratory – Logical Reasoning for Planning  

---

## 1. Summary of Empirical Test Results

The generated planner was evaluated against three distinct test scenarios implemented in [test_planner.py](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/tests/test_planner.py). Execution logs were captured directly in [test_output.txt](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/results/test_output.txt).

### Comprehensive Results Table

| Test Identifier | Initial State ($I$) | Goal State ($G$) | Plan Found? | Resulting Plan Sequence | Independent Verifier Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Test A: Solvable Benchmark** | `At(Robot, A)`, `At(Package, A)` | `At(Package, C)` | **YES** | `[PickUp(Package, A), Move(A, B), Move(B, C), Drop(Package, C)]` | **PASSED** (Valid 4-step optimal plan) |
| **Test B: Unsolvable Domain** | `At(Robot, A)`, `At(Package, A)` | `At(Package, C)` | **NO** | `None` ("No plan found!") | **PASSED** (Correctly detected unsolvability) |
| **Test C: Goal Distinction** | `At(Robot, A)`, `At(Package, A)` | `At(Package, C)` | Evaluated `Move(A, B) -> Move(B, C)` | `Move(A, B) -> Move(B, C)` yields `At(Robot, C)` without package | **PASSED** (Candidate rejected as invalid; BFS returned valid plan) |

---

## 2. Detailed Analysis of Each Test Case

### Test A: Solvable Warehouse Benchmark
- **Objective:** Verify that the BFS planner finds a complete, valid plan for the standard problem.
- **Outcome:** The planner identified the optimal 4-step sequence: `PickUp(Package, A) -> Move(A, B) -> Move(B, C) -> Drop(Package, C)`.
- **Verification:** The independent validator re-simulated state transitions step-by-step from $S_0$ to $S_4$ and confirmed that all action preconditions were satisfied and the final state contains `At(Package, C)`.

### Test B: Unsolvable Domain (No PickUp Action)
- **Objective:** Verify that the planner detects when no plan exists instead of looping infinitely.
- **Outcome:** All `PickUp` actions were removed. The robot moved between connected nodes $A \leftrightarrow B \leftrightarrow C$, but could never transition the package out of $A$. BFS exhausted all reachable states and terminated cleanly, returning `None` ("No plan found!").
- **Verification:** The validator confirmed that no sequence of available moves could satisfy `At(Package, C)`.

### Test C: Irrelevant Move Actions & Goal Distinction
- **Objective:** Ensure that the robot reaching location $C$ (`At(Robot, C)`) is **not** treated as equivalent to the package reaching location $C$ (`At(Package, C)`).
- **Outcome:** The candidate plan `Move(A, B) -> Move(B, C)` resulted in state $S_2 = \{\text{At(Robot, C)}, \text{At(Package, A)}\}$. The independent validator checked if $G = \{\text{At(Package, C)}\} \subseteq S_2$, found it false, and rejected the candidate plan.
- **Verification:** Demonstrates that set-based proposition checking prevents false positives where robot position is confused with package position.

---

## 3. Evidence Trace from `results/test_output.txt`

```text
TEST A: Solvable Problem (Original Warehouse Benchmark)
RESULT: Found plan of length 4 actions.
Independent Verification Result: PASSED (Valid Plan)

TEST B: Unsolvable Problem (No PickUp Actions Available)
RESULT: No plan found!
Independent Verification Result: PASSED (Correctly Rejected/No Plan)

TEST C: Irrelevant Moves & Goal Distinction (Robot at C != Package at C)
Evaluating Candidate Plan: Move(A, B) -> Move(B, C)
[VERIFIER FAIL] Final state ['At(Package, A)', 'At(Robot, C)'] does NOT satisfy Goal ['At(Package, C)']
Candidate Plan Validation Result: INVALID (Robot at C does NOT equal Package at C)
```
