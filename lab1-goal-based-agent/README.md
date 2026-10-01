# Goal-Based Warehouse Agent (Lab 1)

This repository contains the complete solution for **Laboratory Exercise 1: Constructing a Goal-Based Agent using a Large Language Model**. The goal of the agent is to find an optimal collision-free path for an autonomous warehouse vehicle navigating from a start position (`S`) to a destination goal (`G`) on a 2D grid containing fixed obstacles (`#`).

---

## Lab Objectives

1. Explain the operation of a goal-based intelligent agent.
2. Use a Large Language Model (LLM) to assist with software development.
3. Generate, execute, and test Python code produced by an LLM.
4. Improve software through iterative prompt engineering.
5. Critically evaluate the strengths and limitations of LLM-assisted software engineering.

---

## Repository Structure

```text
lab1-goal-based-agent/
├── README.md           # Main project overview & instructions
├── checkpoint.md       # Consolidated lab submission document (Tasks 1-3, Testing, LLM Reflection)
└── src/                # Single folder for all source code, tests, runner & output
    ├── warehouse_agent.py  # Pure Python 3 BFS Goal-Based Agent
    ├── test_agent.py       # Unit test suite (5 test scenarios)
    ├── run_all.py          # Execution runner script
    └── output.txt          # Real captured execution log
```

---

## Table of Contents & File Links

- **Lab Submission Document**:
  - [`checkpoint.md`](file:///Users/mittals/Desktop/AI%20Labs/lab1-goal-based-agent/checkpoint.md) - Consolidated submission detailing Task 1 (Understanding), Task 2 (Design & Diagram), Task 3 (Prompts V1/V2 & Questions), Testing Log, and LLM Reflection (LO5).
- **Source Code, Testing & Execution Output (`src/`)**:
  - [`src/warehouse_agent.py`](file:///Users/mittals/Desktop/AI%20Labs/lab1-goal-based-agent/src/warehouse_agent.py) - Pure Python 3 implementation of Goal-Based Agent using BFS.
  - [`src/test_agent.py`](file:///Users/mittals/Desktop/AI%20Labs/lab1-goal-based-agent/src/test_agent.py) - Unit test suite covering original map, adjacent S-G, unreachable goal, obstacle assertions, and step distance integrity.
  - [`src/run_all.py`](file:///Users/mittals/Desktop/AI%20Labs/lab1-goal-based-agent/src/run_all.py) - Execution runner script that executes unit tests and agent demo.
  - [`src/output.txt`](file:///Users/mittals/Desktop/AI%20Labs/lab1-goal-based-agent/src/output.txt) - Genuine captured execution results log.

---

## How to Run (Python 3 Only, Standard Library)

No external libraries are required. Run commands from the `lab1-goal-based-agent/` root folder:

### 1. Run the Warehouse Agent Demo directly:
```bash
python3 src/warehouse_agent.py
```

### 2. Run the Unit Test Suite:
```bash
python3 src/test_agent.py
```

### 3. Run All Tests and Save Output to `src/output.txt`:
```bash
python3 src/run_all.py
```

---

## How to Download / Archive

To archive the entire repository as a single downloadable file:
```bash
zip -r lab1-goal-based-agent.zip lab1-goal-based-agent/
```
