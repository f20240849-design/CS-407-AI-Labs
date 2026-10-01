# Laboratory – Logical Reasoning for Planning (`lab3-logical-planning/`)

> **Core Concept:** **Logic + Search = Planning**  
> *The logical component determines what is possible ($S \models \text{Preconditions}(a)$); the search component determines what to try (BFS).*

---

## 1. Project Overview

This repository contains the complete implementation, test suite, prompt documentation, Prolog verifier, and task checkpoints for **Lab 3: Logical Reasoning for Planning**.

In classical AI planning, an agent transforms an initial world state $I$ into a goal state $G$ using a sequence of domain actions $A$. In this warehouse scenario:
- **Locations:** $A, B, C$ connected in a chain ($A \leftrightarrow B \leftrightarrow C$).
- **Initial State $I$:** $\{\text{At(Robot, A)}, \text{At(Package, A)}\}$.
- **Goal State $G$:** $\{\text{At(Package, C)}\}$.
- **Actions:** $\text{Move}(X, Y)$, $\text{PickUp}(\text{Package}, L)$, $\text{Drop}(\text{Package}, L)$.

The planning engine represents states as `frozenset` objects under the **Closed-World Assumption**, uses set operations to enforce preconditions and effects, and applies Breadth-First Search (BFS) to find optimal plans. An independent plan validator (`validate_plan`) and an optional Prolog rule engine (`planner.pl`) provide independent verification.

---

## 2. Table of Contents & File Manifest

All 18 files in this repository are hyperlinked below:

### 📍 Core Codebase & Tests
1. [src/planner.py](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/src/planner.py) – Proposition-based planning engine & BFS search algorithm.
2. [tests/test_planner.py](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/tests/test_planner.py) – Test suite (Tests A, B, C) & independent plan validator.
3. [results/test_output.txt](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/results/test_output.txt) – Actual test execution output log.
4. [prompts/planner_prompt.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/prompts/planner_prompt.md) – Task 2 verbatim prompt, improved prompt, and engineering notes.
5. [prolog/planner.pl](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/prolog/planner.pl) – SWI-Prolog knowledge base, movement rules, and deductive wet-road program.
6. [SUBMISSION_CHECKLIST.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/SUBMISSION_CHECKLIST.md) – Mapping of the 7 submission deliverables & LLM attribution.

### 📍 Task Checkpoints (`checkpoints/`)
7. [checkpoints/checkpoint_task0.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_task0.md) – Formal problem specification & initial action applicability.
8. [checkpoints/checkpoint_task1.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_task1.md) – Hand-built plan, state table ($S_0 \dots S_4$), & flaw analysis of example sequence.
9. [checkpoints/checkpoint_task2.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_task2.md) – Concept-to-code mapping table & classical planning assumptions.
10. [checkpoints/checkpoint_task3.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_task3.md) – Test results summary for Tests A, B, and C.
11. [checkpoints/checkpoint_task4.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_task4.md) – Completed planning flow diagram & Logic + Search synergy explanation.
12. [checkpoints/checkpoint_task5.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_task5.md) – LLM explanation vs. independent verification analysis.
13. [checkpoints/checkpoint_task6.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_task6.md) – Prolog `can_move` query results & rule analysis.
14. [checkpoints/checkpoint_task7.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_task7.md) – Prolog plan verification, Challenge evaluation, & Generate-Verify architecture.
15. [checkpoints/checkpoint_task8.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_task8.md) – Prolog wet-road derivation chain ($\text{Fact} \Rightarrow \text{Rule} \Rightarrow \text{Rule} \Rightarrow \text{Conclusion}$).
16. [checkpoints/checkpoint_prolog_reflection.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_prolog_reflection.md) – Prolog reflection questions (Q1–Q4).
17. [checkpoints/checkpoint_reflection.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_reflection.md) – General reflection questions (Q1–Q7).

---

## 3. How to Run the Code

### Prerequisites
- Python 3.8+ (No external third-party libraries required; uses Python standard library `collections`, `typing`, `sys`, `os`).
- SWI-Prolog (optional, for running `prolog/planner.pl`).

### Execution Commands

1. **Run the Standard BFS Planner:**
   ```bash
   python3 src/planner.py
   ```

2. **Run the Automated Test Suite & Independent Plan Verifier:**
   *(Updates `results/test_output.txt` automatically)*
   ```bash
   python3 tests/test_planner.py
   ```

3. **Run the Prolog Verifier (SWI-Prolog):**
   ```bash
   swipl prolog/planner.pl
   ```
   Inside the SWI-Prolog REPL, execute queries:
   ```prolog
   ?- can_move(a, b).
   ?- valid_move(a, c).
   ?- reduce_speed.
   ```
