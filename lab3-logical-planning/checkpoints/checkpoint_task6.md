# Checkpoint Task 6: Prolog as a Plan Verifier

**Student Name:** AI Undergraduate Student  
**Lab Assignment:** Laboratory – Logical Reasoning for Planning  

---

## 1. Prolog Program & Query Results

The Prolog program [planner.pl](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/prolog/planner.pl) defines the warehouse topology as facts and movement rules:

```prolog
connected(a, b).
connected(b, a).
connected(b, c).
connected(c, b).

can_move(X, Y) :-
    connected(X, Y).
```

### Empirical Query Execution Log:

```prolog
?- can_move(a, b).
true.

?- can_move(a, c).
false.
```

---

## 2. Answers to Task 6 Questions

### Question (a): Why does Prolog return `true` for `can_move(a, b)`?
**Answer:**  
When Prolog evaluates `?- can_move(a, b).`, it unifies the goal with the head of the rule `can_move(X, Y)` with bindings $X = a$ and $Y = b$. This reduces the goal to proving the body atom `connected(a, b)`. Prolog searches its knowledge base, matches the explicit fact `connected(a, b).`, and successfully terminates with `true.`.

---

### Question (b): Why does Prolog not establish `can_move(a, c)`?
**Answer:**  
Prolog unifies `?- can_move(a, c).` with rule $X = a, Y = c$, reducing the query to checking `connected(a, c)`. 
Prolog searches the knowledge base, but **no fact `connected(a, c).` exists** (only $a \leftrightarrow b$ and $b \leftrightarrow c$ are declared).

Because Prolog operates under the **Closed-World Assumption** using **Negation as Failure (NAF)**, any proposition that cannot be proved from the knowledge base is inferred to be false. Therefore, the query fails and Prolog outputs `false.`.

---

### Question (c): What is the relationship between the Prolog rule `can_move(X, Y) :- connected(X, Y).` and the logical implication $\text{Connected}(X, Y) \rightarrow \text{CanMove}(X, Y)$?

**Answer:**  
In classical logic, the implication $\text{Connected}(X, Y) \rightarrow \text{CanMove}(X, Y)$ states that if location $X$ is connected to $Y$, then the robot can move from $X$ to $Y$. 

In Prolog, rules are written in reverse Horn clause notation:
$$\text{Head} :- \text{Body} \quad \equiv \quad \text{Body} \rightarrow \text{Head}$$

Thus, `can_move(X, Y) :- connected(X, Y).` is syntactically equivalent to $\text{Connected}(X, Y) \rightarrow \text{CanMove}(X, Y)$. Operationally, Prolog uses **backward chaining** (SLD resolution), working from the goal ($\text{Head}$) back to the premise ($\text{Body}$).

---

## 3. Evidence Trace

```text
Loading /Users/mittals/Desktop/AI Labs/lab3-logical-planning/prolog/planner.pl...
?- can_move(a, b).
true.

?- can_move(a, c).
false.
```
