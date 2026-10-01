"""
Test Suite and Independent Plan Verifier for Logical Planner
Generated with LLM assistance (Gemini 3.6 Flash)

This script runs three test scenarios and validates generated plans using an independent step-by-step simulator.
Execution output is printed to console and saved to results/test_output.txt.
"""

import sys
import os
from typing import List, FrozenSet, Optional, Dict

# Ensure src module is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.planner import Action, bfs_plan, create_warehouse_actions, print_plan_execution


def validate_plan(
    initial_state: FrozenSet[str],
    goal_state: FrozenSet[str],
    plan: Optional[List[Action]],
    actions_dict: Dict[str, Action]
) -> bool:
    """
    Independent Plan Verifier.
    Re-simulates the plan step-by-step starting from initial_state.
    Verifies:
    1. Every action exists in the domain.
    2. Every positive and negative precondition is satisfied before action execution.
    3. State transition applies correct negative and positive effects.
    4. Goal state propositions are a subset of the final state.
    """
    if plan is None:
        return False

    current_state = frozenset(initial_state)

    for i, action in enumerate(plan, start=1):
        # 1. Action lookup validation
        if action.name not in actions_dict:
            print(f"[VERIFIER FAIL] Step {i}: Action '{action.name}' is unknown.")
            return False

        domain_action = actions_dict[action.name]

        # 2. Check Preconditions independently
        if not domain_action.applicable(current_state):
            print(f"[VERIFIER FAIL] Step {i}: Preconditions for '{action.name}' NOT satisfied in state {sorted(list(current_state))}")
            print(f"               Missing Pos Pre: {sorted(list(domain_action.pos_pre - current_state))}")
            print(f"               Violated Neg Pre: {sorted(list(domain_action.neg_pre.intersection(current_state)))}")
            return False

        # 3. Apply state transition
        current_state = domain_action.apply(current_state)

    # 4. Final Goal Verification
    is_valid_goal = goal_state.issubset(current_state)
    if not is_valid_goal:
        print(f"[VERIFIER FAIL] Final state {sorted(list(current_state))} does NOT satisfy Goal {sorted(list(goal_state))}")
        return False

    return True


def run_test_a():
    print("=" * 70)
    print("TEST A: Solvable Problem (Original Warehouse Benchmark)")
    print("=" * 70)
    
    I = frozenset({"At(Robot, A)", "At(Package, A)"})
    G = frozenset({"At(Package, C)"})
    actions = create_warehouse_actions()
    actions_dict = {a.name: a for a in actions}

    print(f"Initial State I : {sorted(list(I))}")
    print(f"Goal State G    : {sorted(list(G))}")

    plan, history = bfs_plan(I, G, actions)
    print_plan_execution(I, plan, history)

    # Run Independent Verifier
    is_valid = validate_plan(I, G, plan, actions_dict)
    print(f"Independent Verification Result: {'PASSED (Valid Plan)' if is_valid else 'FAILED (Invalid Plan)'}\n")


def run_test_b():
    print("=" * 70)
    print("TEST B: Unsolvable Problem (No PickUp Actions Available)")
    print("=" * 70)

    I = frozenset({"At(Robot, A)", "At(Package, A)"})
    G = frozenset({"At(Package, C)"})
    
    # Filter out all PickUp actions
    all_actions = create_warehouse_actions()
    actions = [a for a in all_actions if not a.name.startswith("PickUp")]
    actions_dict = {a.name: a for a in actions}

    print(f"Initial State I : {sorted(list(I))}")
    print(f"Goal State G    : {sorted(list(G))}")
    print(f"Available Action Types: Move, Drop (PickUp excluded)")

    plan, history = bfs_plan(I, G, actions)
    print_plan_execution(I, plan, history)

    is_valid = validate_plan(I, G, plan, actions_dict)
    print(f"Independent Verification Result: {'PASSED (Correctly Rejected/No Plan)' if not is_valid else 'FAILED'}\n")


def run_test_c():
    print("=" * 70)
    print("TEST C: Irrelevant Moves & Goal Distinction (Robot at C != Package at C)")
    print("=" * 70)

    # Scenario: Robot moves A -> B -> C without picking up package
    I = frozenset({"At(Robot, A)", "At(Package, A)"})
    G = frozenset({"At(Package, C)"})
    
    all_actions = create_warehouse_actions()
    actions_dict = {a.name: a for a in all_actions}

    print(f"Initial State I : {sorted(list(I))}")
    print(f"Goal State G    : {sorted(list(G))}")

    # Hypothetical invalid plan where robot just moves to C without package
    invalid_plan = [
        actions_dict["Move(A, B)"],
        actions_dict["Move(B, C)"]
    ]

    print("\nEvaluating Candidate Plan: Move(A, B) -> Move(B, C)")
    print("Checking if robot reaching C satisfies goal At(Package, C)...")

    is_valid = validate_plan(I, G, invalid_plan, actions_dict)
    print(f"Candidate Plan Validation Result: {'VALID' if is_valid else 'INVALID (Robot at C does NOT equal Package at C)'}")

    print("\nRunning BFS Search on Full Action Set to ensure optimal solution ignores irrelevant loops:")
    plan, history = bfs_plan(I, G, all_actions)
    print_plan_execution(I, plan, history)
    
    is_valid_bfs = validate_plan(I, G, plan, actions_dict)
    print(f"Full BFS Independent Verification: {'PASSED (Valid Plan)' if is_valid_bfs else 'FAILED'}\n")


class DualLogger:
    """Tee logger to write to both stdout and test_output.txt"""
    def __init__(self, filepath: str):
        self.terminal = sys.stdout
        self.logfile = open(filepath, "w")

    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)

    def flush(self):
        self.terminal.flush()
        self.logfile.flush()

    def close(self):
        self.logfile.close()


if __name__ == "__main__":
    results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, "test_output.txt")

    logger = DualLogger(output_path)
    sys.stdout = logger

    try:
        run_test_a()
        run_test_b()
        run_test_c()
    finally:
        sys.stdout = logger.terminal
        logger.close()
    
    print(f"\nTest execution complete. Log saved to: {output_path}")
