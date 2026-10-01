# Submission Checklist: Lab 3 - Logical Reasoning for Planning

**Student Name:** AI Undergraduate Student  
**Repository Directory:** `lab3-logical-planning/`  

---

## 1. Submission Items Mapping Table

This checklist maps each of the 7 required submission items from Section 4 of the laboratory sheet to its exact file location in this repository.

| Submission Item Number | Required Deliverable | Repository File Path | Description of File Contents |
| :---: | :--- | :--- | :--- |
| **1** | **Problem Specification** | [checkpoint_task0.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_task0.md) | Formal specification of initial state $I$, goal $G$, and domain action schemas ($\text{Move}$, $\text{PickUp}$, $\text{Drop}$). |
| **2** | **Manually Constructed Plan** | [checkpoint_task1.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_task1.md) | Manual plan trace ($S_0 \dots S_4$), precondition checks, and critique of the lab sheet's invalid example. |
| **3** | **LLM Prompt Used** | [planner_prompt.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/prompts/planner_prompt.md) | Task 2 verbatim prompt, production prompt, and prompt engineering commentary. |
| **4** | **Generated Python Program** | [planner.py](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/src/planner.py) | Proposition-based planning engine using `frozenset` states, `Action` preconditions/effects, and BFS search. |
| **5** | **Test Results** | [test_output.txt](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/results/test_output.txt) | Complete log output from executing `tests/test_planner.py` across Tests A, B, C and the independent verifier. |
| **6** | **"Think About It" Answers** | [checkpoints/](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/) | Answers to all "Think About It" boxes in Tasks 0, 1, 2, 4, 7, and 8. |
| **7** | **Reflection on LLM Use** | [checkpoint_reflection.md](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/checkpoint_reflection.md) | Detailed answers to the 7 core reflection questions and optional Prolog reflection questions. |

---

## 2. LLM Assistance Attribution Table

| File Name | Human Contribution | LLM Assistance Contribution |
| :--- | :--- | :--- |
| [src/planner.py](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/src/planner.py) | Defined domain rules, specified `frozenset` data structures and set-math requirements. | Generated initial class boilerplate, BFS loop, and print formatting. |
| [tests/test_planner.py](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/tests/test_planner.py) | Designed test scenarios (Tests A, B, C) and independent verification logic (`validate_plan`). | Generated test function harness and file output logging setup. |
| [prolog/planner.pl](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/prolog/planner.pl) | Specified topological graph facts and wet-road deduction rules. | Formatted Horn clause syntax and sample query comments. |
| [checkpoints/](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/checkpoints/) | Analyzed state traces, authored first-person reflections, and performed manual proofs. | Assisted with markdown formatting and table rendering. |
