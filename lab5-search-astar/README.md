# Lab 5: Search and A* (Using an LLM as an Engineering Assistant)

Welcome to the **Lab 5: Search and A*** repository for undergraduate AI studies. This project implements, tests, and evaluates classical state-space search algorithms (Breadth-First Search and A* Search) using Python 3 and an LLM-assisted software engineering workflow.

---

## Repository Overview

This repository demonstrates the formal problem formulation, design, implementation, and empirical evaluation of search algorithms on 2D grid warehouse maps. The codebase evaluates BFS and A* across multiple heuristics ($h=0$, Manhattan distance, Euclidean distance, $2 \times \text{Manhattan}$ distance) and verifies shortest-path optimality, state expansion counts, and heuristic admissibility.

---

## Quick Start & Run Instructions (Python 3 Only)

No external third-party dependencies are required. Built entirely using Python 3 standard libraries (`heapq`, `collections`, `math`, `sys`, `os`).

### 1. Run Core Search Test Suite
Executes Tests 1–4 and generates `results/test_output.txt`:
```bash
python3 tests/test_search.py
```

### 2. Run BFS vs A* Comparison
Solves Map 1 using BFS and A* and generates `results/comparison.md`:
```bash
python3 src/compare_bfs_astar.py
```

### 3. Run Heuristic Experiments
Evaluates 4 heuristic functions on Map 1 and generates `results/heuristics.md`:
```bash
python3 src/heuristic_experiments.py
```

---

## Directory Structure

```text
lab5-search-astar/
├── README.md
├── SUBMISSION_CHECKLIST.md
├── src/
│   ├── astar.py
│   ├── bfs.py
│   ├── compare_bfs_astar.py
│   └── heuristic_experiments.py
├── tests/
│   └── test_search.py
├── results/
│   ├── test_output.txt
│   ├── comparison.md
│   └── heuristics.md
├── prompts/
│   └── astar_prompt.md
└── checkpoints/
    ├── checkpoint_task0.md
    ├── checkpoint_task1.md
    ├── checkpoint_task2.md
    ├── checkpoint_task3.md
    ├── checkpoint_task4.md
    ├── checkpoint_task5.md
    ├── checkpoint_task6.md
    ├── checkpoint_task7.md
    └── checkpoint_final_reflection.md
```

---

## Table of Contents & Direct File Links

### Core Source Code (`src/`)
- [src/astar.py](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/astar.py): A* Search algorithm with `heapq`, Manhattan heuristic default, explicit $g/h/f$ costs, closed set, parent pointers, path reconstruction, determinism header, and pluggable heuristic function support.
- [src/bfs.py](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/bfs.py): Breadth-First Search implementation with `collections.deque` and matching output contract.
- [src/compare_bfs_astar.py](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/compare_bfs_astar.py): Programmatic benchmark script generating `results/comparison.md`.
- [src/heuristic_experiments.py](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/src/heuristic_experiments.py): Benchmark script evaluating 4 heuristic variants and generating `results/heuristics.md`.

### Test Suite (`tests/`)
- [tests/test_search.py](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/tests/test_search.py): Test harness running Test 1 (Original Map), Test 2 (Trivial Map), Test 3 (Unreachable Goal), and Test 4 (Multi-Path Map Optimality).

### Execution Results (`results/`)
- [results/test_output.txt](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/results/test_output.txt): Verified console trace output from `tests/test_search.py`.
- [results/comparison.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/results/comparison.md): Markdown benchmark table comparing BFS vs A*.
- [results/heuristics.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/results/heuristics.md): Markdown comparison table across $h=0$, Manhattan, Euclidean, and $2 \times \text{Manhattan}$.

### Prompts Documentation (`prompts/`)
- [prompts/astar_prompt.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/prompts/astar_prompt.md): Contains verbatim sheet prompt, refined Task 1 prompt, and prompt engineering justification.

### Checkpoints & Deliverables (`checkpoints/`)
- [checkpoints/checkpoint_task0.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/checkpoints/checkpoint_task0.md): Task 0 Problem Formulation table ($S, A, T, s_0, G, c$), (a)–(d) questions, and Think About It.
- [checkpoints/checkpoint_task1.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/checkpoints/checkpoint_task1.md): Task 1 Pre-LLM Agent Design (6 design points + 4 reported metrics).
- [checkpoints/checkpoint_task2.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/checkpoints/checkpoint_task2.md): Task 2 Code Generation, Prompt References, and Acceptance Notes.
- [checkpoints/checkpoint_task3.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/checkpoints/checkpoint_task3.md): Task 3 Tests 1–4 Execution Analysis and Optimality Verification.
- [checkpoints/checkpoint_task4.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/checkpoints/checkpoint_task4.md): Task 4 Line-Number Code Mapping to `src/astar.py` and Conceptual Q&A (a)–(e).
- [checkpoints/checkpoint_task5.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/checkpoints/checkpoint_task5.md): Task 5 BFS vs A* Table, Q&A (a)–(d), Think About It, and Single-Corridor Explanation.
- [checkpoints/checkpoint_task6.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/checkpoints/checkpoint_task6.md): Task 6 Manhattan Rationale, Heuristic Results Table, Admissibility Breakdown, and Inadmissibility Analysis.
- [checkpoints/checkpoint_task7.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/checkpoints/checkpoint_task7.md): Task 7 LLM Evaluation (8 Q&A) and 5-Part Workflow Distinction.
- [checkpoints/checkpoint_final_reflection.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/checkpoints/checkpoint_final_reflection.md): Final Reflection Answers across 5 core topics.

### Root Submission Index
- [SUBMISSION_CHECKLIST.md](file:///Users/mittals/Desktop/AI%20Labs/lab5-search-astar/SUBMISSION_CHECKLIST.md): 8-item submission checklist mapping requirements to files, commands, and LLM attribution.
