# Checkpoint: General Reflection Questions

**Student Name:** AI Undergraduate Student  
**Lab Assignment:** Laboratory – Logical Reasoning for Planning  

---

### Question 1: Why is it useful to specify action preconditions and effects before asking an LLM to write the planner?

**Answer:**  
Specifying action preconditions and effects before prompting an LLM establishes a clear, unambiguous formal contract for the problem domain. Without explicit specifications of positive/negative preconditions and effects, an LLM might invent ad-hoc state transitions, omit critical negative effects (e.g., forgetting to remove `At(Robot, A)` when moving to `B`), or use inconsistent data structures. Providing explicit specifications ensures the generated code correctly implements state applicability ($S \models \text{Preconditions}(a)$) and state transitions ($S' = (S \setminus \text{neg\_eff}) \cup \text{pos\_eff}$).

---

### Question 2: Give an example of an error that could occur if the planner failed to check an action's preconditions.

**Answer:**  
If the planner failed to check preconditions, it might execute `PickUp(Package, B)` while the package is actually located at location `A`. The planner would add `Holding(Package)` to the state without verifying that the robot and package share the same location (`At(Package, B)`). This creates physically impossible states where items are picked up remotely or teleport across locations, completely invalidating the plan.

---

### Question 3: Why is a plan that "looks reasonable" not necessarily a valid plan?

**Answer:**  
A plan can "look reasonable" to a human reading natural language because the sequence of action names matches a intuitive narrative—such as the lab sheet's candidate sequence: `Move(A, B) -> PickUp(Package, B) -> Move(B, C) -> Drop(Package, C)`. However, when formally traced step-by-step against state proposition sets, the package was left behind at location `A`, making `PickUp(Package, B)` illegal at step 2. A plan is valid only if **every** action's preconditions are mathematically satisfied in the exact state in which it is executed.

---

### Question 4: What did the LLM contribute to the implementation?

**Answer:**  
The LLM contributed the initial Python code implementation based on my specification prompt. Specifically, it generated the boilerplate structure for the `Action` class, implemented set-based applicability and state-transition methods, set up the `bfs_plan()` queue management loop, and provided the basic structure for the test script.

---

### Question 5: What did you have to verify independently?

**Answer:**  
I independently verified the generated system by:
1. Manually tracing the action preconditions and state proposition tables for the warehouse problem ($S_0 \dots S_4$).
2. Designing and executing three distinct test scenarios: Test A (solvable benchmark), Test B (unsolvable domain with missing PickUp), and Test C (goal distinction verifying `At(Robot, C)` $\neq$ `At(Package, C)`).
3. Writing an independent plan verifier function (`validate_plan` in `tests/test_planner.py`) that re-simulates state transitions step-by-step from $I$ without relying on the planner's internal state history.

---

### Question 6: In this laboratory, where is logical reasoning being used?

**Answer:**  
Logical reasoning is used at four key points:
1. **Applicability Checking:** Evaluating whether action preconditions are satisfied by the state set ($S \models \text{Preconditions}(a)$).
2. **State Transitions:** Applying propositional set subtraction and union under the Closed-World Assumption ($S' = (S \setminus \text{neg\_eff}) \cup \text{pos\_eff}$).
3. **Goal Entailment:** Checking whether goal propositions are a subset of the reached state ($G \subseteq S'$).
4. **Prolog Rule Deduction:** Proving topological connectivity and movement validity using Horn clause backward chaining in `planner.pl`.

---

### Question 7: How is planning related to the search algorithms studied in the previous module?

**Answer:**  
Planning is a specific application of graph search algorithms (like BFS). In general search, nodes represent arbitrary states and edges represent transitions. In classical planning:
- **States** are represented explicitly as sets of logical propositions.
- **Edges (Successors)** are generated dynamically by identifying applicable domain actions whose preconditions are logically satisfied.
- **Pathfinding** uses BFS to explore the state-space tree, ensuring the discovery of the shortest (optimal) sequence of actions from $I$ to $G$.
