/*
  Prolog Logical Verifier for Planning Agent
  Generated with LLM assistance (Gemini 3.6 Flash)

  This knowledge base defines warehouse topological connections,
  movement validation rules, and a simple deductive rule system.
*/

% ==============================================================================
% Task 6 & 7: Warehouse Connection Topology
% ==============================================================================

% Facts: Bidirectional physical connections between locations
connected(a, b).
connected(b, a).
connected(b, c).
connected(c, b).

% Task 6 Rule: Robot movement possibility rule
can_move(X, Y) :-
    connected(X, Y).

% Task 7 Rule: Independent move validation rule
valid_move(X, Y) :-
    connected(X, Y).


% ==============================================================================
% Task 8: Deductive Logical Reasoning System (Wet Road Domain)
% ==============================================================================

% Fact: Ground truth observation
wet_road.

% Rule 1: Wet road implies slippery road
slippery :-
    wet_road.

% Rule 2: Slippery road implies speed reduction
reduce_speed :-
    slippery.


% ==============================================================================
% Interactive Queries & Expected Verification Results
% ==============================================================================
/*
  To run these queries in SWI-Prolog, load the file using:
  ?- [planner].

  ------------------------------------------------------------------------------
  Task 6 Queries:
  ------------------------------------------------------------------------------
  Query 1: Can the robot move directly from location A to B?
  ?- can_move(a, b).
  Result: true.

  Query 2: Can the robot move directly from location A to C?
  ?- can_move(a, c).
  Result: false.

  ------------------------------------------------------------------------------
  Task 7 Queries (Checking Proposed Plan Steps):
  ------------------------------------------------------------------------------
  Query 3: Is Move(a, b) valid?
  ?- valid_move(a, b).
  Result: true.

  Query 4: Is Move(b, c) valid?
  ?- valid_move(b, c).
  Result: true.

  Query 5 (Challenge): Is Move(a, c) valid?
  ?- valid_move(a, c).
  Result: false.

  ------------------------------------------------------------------------------
  Task 8 Query:
  ------------------------------------------------------------------------------
  Query 6: Does the system deduce that speed should be reduced?
  ?- reduce_speed.
  Result: true.
*/
