"""
Planner Engine for Logical Reasoning and Planning
Generated with LLM assistance (Gemini 3.6 Flash)

This module implements a classical proposition-based planning engine using Breadth-First Search (BFS).
States are represented as frozensets of logical propositions under the Closed-World Assumption.
"""

from collections import deque
from typing import List, Set, FrozenSet, Tuple, Optional


class Action:
    """
    Represents a planning action with precondition and effect sets.
    """
    def __init__(
        self,
        name: str,
        pos_pre: Set[str],
        neg_pre: Set[str],
        pos_eff: Set[str],
        neg_eff: Set[str]
    ):
        self.name = name
        self.pos_pre = frozenset(pos_pre)
        self.neg_pre = frozenset(neg_pre)
        self.pos_eff = frozenset(pos_eff)
        self.neg_eff = frozenset(neg_eff)

    # [Preconditions] Action Applicability Check: S |= Preconditions(a)
    def applicable(self, state: FrozenSet[str]) -> bool:
        """
        An action 'a' is applicable in state 'S' if:
        1. All positive preconditions are present in S (pos_pre <= S)
        2. No negative preconditions are present in S (len(neg_pre & S) == 0)
        """
        return self.pos_pre.issubset(state) and len(self.neg_pre.intersection(state)) == 0

    # [Effects] State Transition: S' = Apply(S, a)
    def apply(self, state: FrozenSet[str]) -> FrozenSet[str]:
        """
        Applies action effects to state S:
        1. Remove negative effects
        2. Add positive effects
        """
        if not self.applicable(state):
            raise ValueError(f"Action '{self.name}' is not applicable in state: {state}")
        
        # S' = (S \ neg_eff) U pos_eff
        new_state = (state - self.neg_eff) | self.pos_eff
        return frozenset(new_state)

    def __repr__(self) -> str:
        return self.name


# [BFS] Breadth-First Search Planning Algorithm
def bfs_plan(
    initial_state: FrozenSet[str],
    goal_state: FrozenSet[str],
    actions: List[Action]
) -> Tuple[Optional[List[Action]], List[FrozenSet[str]]]:
    """
    Finds a shortest sequence of actions from initial_state to goal_state using BFS.
    
    Returns:
        (plan, state_history) if a plan is found.
        (None, []) if no plan exists.
    """
    # [Goal] Check if initial state already satisfies goal
    if goal_state.issubset(initial_state):
        return [], [initial_state]

    # Queue stores tuples of: (current_state, action_path, state_history)
    queue = deque([(initial_state, [], [initial_state])])
    visited: Set[FrozenSet[str]] = {initial_state}

    while queue:
        current_state, plan_path, state_history = queue.popleft()

        # Explore all available actions
        for action in actions:
            # [Preconditions] Check if action can be executed in current state
            if action.applicable(current_state):
                # [Effects] Compute successor state
                next_state = action.apply(current_state)

                # [Goal] Check if successor state satisfies goal proposition set
                if goal_state.issubset(next_state):
                    final_plan = plan_path + [action]
                    final_history = state_history + [next_state]
                    return final_plan, final_history

                # Add to queue if state has not been visited before
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((
                        next_state,
                        plan_path + [action],
                        state_history + [next_state]
                    ))

    # "No plan found" detection
    return None, []


def print_plan_execution(
    initial_state: FrozenSet[str],
    plan: Optional[List[Action]],
    state_history: List[FrozenSet[str]]
) -> None:
    """
    Prints a readable summary of the plan and resulting state transitions.
    """
    print("=" * 60)
    print("PLANNING RESULTS")
    print("=" * 60)
    print(f"Initial State S0: {sorted(list(initial_state))}")
    print("-" * 60)

    if plan is None:
        print("RESULT: No plan found!")
        print("=" * 60)
        return

    print(f"RESULT: Found plan of length {len(plan)} actions.")
    print("-" * 60)

    for i, (action, state) in enumerate(zip(plan, state_history[1:]), start=1):
        print(f"Step {i}: Execute {action.name}")
        print(f"        State S{i}: {sorted(list(state))}")

    print("=" * 60)


def create_warehouse_actions() -> List[Action]:
    """
    Helper function to define the standard domain actions for the warehouse problem.
    Locations: A, B, C. Robot connections: A <-> B and B <-> C.
    """
    actions = []
    locations = ["A", "B", "C"]
    connections = [("A", "B"), ("B", "A"), ("B", "C"), ("C", "B")]

    # Move(X, Y) actions
    for x, y in connections:
        actions.append(Action(
            name=f"Move({x}, {y})",
            pos_pre={f"At(Robot, {x})"},
            neg_pre=set(),
            pos_eff={f"At(Robot, {y})"},
            neg_eff={f"At(Robot, {x})"}
        ))

    # PickUp(Package, L) actions
    for loc in locations:
        actions.append(Action(
            name=f"PickUp(Package, {loc})",
            pos_pre={f"At(Robot, {loc})", f"At(Package, {loc})"},
            neg_pre=set(),
            pos_eff={"Holding(Package)"},
            neg_eff={f"At(Package, {loc})"}
        ))

    # Drop(Package, L) actions
    for loc in locations:
        actions.append(Action(
            name=f"Drop(Package, {loc})",
            pos_pre={f"At(Robot, {loc})", "Holding(Package)"},
            neg_pre=set(),
            pos_eff={f"At(Package, {loc})"},
            neg_eff={"Holding(Package)"}
        ))

    return actions


if __name__ == "__main__":
    # Standard Warehouse Problem
    I = frozenset({"At(Robot, A)", "At(Package, A)"})
    G = frozenset({"At(Package, C)"})
    actions = create_warehouse_actions()

    plan, history = bfs_plan(I, G, actions)
    print_plan_execution(I, plan, history)
