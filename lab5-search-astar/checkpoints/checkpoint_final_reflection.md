# Checkpoint: Final Reflection

This document contains my final reflective answers on problem formulation, algorithm behavior, LLM assistance, and engineering methodology.

---

## 1. Problem Formulation in Search Algorithms
Formulating a real-world problem into a formal 6-tuple state space ($S, A, T, s_0, G, c$) is the most critical phase of search engineering. I learned that how states and actions are represented determines both the computational complexity and the physical validity of the solution. By defining states as concise 0-indexed coordinate tuples `(row, col)` and enforcing 4-directional transitions with unit step costs, the complex continuous motion of a warehouse robot was cleanly abstracted into a discrete search graph. Proper problem formulation clarifies boundary constraints, goal conditions, and cost accounting long before writing any search code.

---

## 2. LLM Impact on Understanding A* and Heuristic Search
Using an LLM as an engineering assistant deepened my conceptual grasp of A* by forcing me to articulate exact algorithm mechanics in natural language prompts. To instruct the LLM effectively, I had to deeply understand priority queue tie-breaking, heuristic evaluation ($f = g + h$), parent pointer backtrack trees, and duplicate state suppression. Translating mathematical principles into explicit prompt constraints reinforced how $h(n)$ acts as a goal-oriented guide, while analyzing the LLM's generated code provided a clear, clean reference implementation to study and benchmark.

---

## 3. Advantages and Risks of AI Coding Assistants
The primary advantage of AI coding assistants is rapid development speed: LLMs eliminate boilerplate overhead, instantly construct structured test harnesses, and format experimental results into Markdown tables. However, the primary risk is blind trust without empirical verification. LLMs can generate plausible-looking algorithms that contain subtle non-determinism, incorrect tie-breaking, or flawed state counting. Relying on AI without writing rigorous test suites and manually verifying theoretical properties risks producing brittle, incorrect software.

---

## 4. Empirical Results vs. Theoretical Expectations
Comparing empirical test data with theoretical search principles yielded important insights regarding map topology. Theoretically, A* with an admissible heuristic is expected to expand significantly fewer states than uninformed BFS. Empirically, however, both BFS and A* expanded the exact same 64 states on Map 1 because the maze topology consists of a single mandatory corridor leading to the goal. Furthermore, while theoretical inadmissibility ($h(n) > h^*(n)$) permits A* to return suboptimal paths, the inadmissible $2 \times \text{Manhattan}$ heuristic still returned an optimal 40-move path due to the absence of shortcut branches. This highlighted that algorithm behavior in practice is heavily governed by the interaction between heuristic design and physical graph topology.

---

## 5. Advice for Students Using LLMs in CS Assignments
My core advice to fellow students is to **design before you prompt**. Never ask an LLM to "write A* search" from scratch without first defining your state space, coordinate conventions, tie-breaking rules, and data contracts. Treat the LLM as a high-speed translator that turns your detailed architectural specification into code, not as an oracle that thinks for you. Finally, always write automated verification tests and empirically inspect trace outputs—verifying line numbers, path lengths, and state expansion counts guarantees true understanding and submission confidence.
