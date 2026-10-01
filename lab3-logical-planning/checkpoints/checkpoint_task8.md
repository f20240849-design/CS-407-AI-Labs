# Checkpoint Task 8: Connect Prolog to Logical Reasoning

**Student Name:** AI Undergraduate Student  
**Lab Assignment:** Laboratory – Logical Reasoning for Planning  

---

## 1. Prolog Deductive Reasoning Program

The domain rulebase defined in [planner.pl](file:///Users/mittals/Desktop/AI%20Labs/lab3-logical-planning/prolog/planner.pl) is:

```prolog
wet_road.

slippery :- 
    wet_road.

reduce_speed :- 
    slippery.
```

---

## 2. Query Execution & Results

### Query:
```prolog
?- reduce_speed.
true.
```

---

## 3. Formal Logical Derivation Chain

> **Required Format:** $\text{Fact} \Rightarrow \text{Rule 1} \Rightarrow \text{Rule 2} \Rightarrow \text{Conclusion}$

### Step-by-Step Derivation:

1. **Fact (Ground Truth Observation):**
   $$\text{wet\_road}$$

2. **Rule 1 (First Implication Application):**
   $$\text{wet\_road} \wedge (\text{wet\_road} \rightarrow \text{slippery}) \quad \Rightarrow \quad \text{slippery}$$
   *(By Modus Ponens, since `wet_road` is true, `slippery` is inferred to be true).*

3. **Rule 2 (Second Implication Application):**
   $$\text{slippery} \wedge (\text{slippery} \rightarrow \text{reduce\_speed}) \quad \Rightarrow \quad \text{reduce\_speed}$$
   *(By Modus Ponens, since `slippery` is true, `reduce_speed` is inferred to be true).*

4. **Conclusion:**
   $$\mathbf{reduce\_speed} \quad \equiv \quad \text{true}$$

---

## 4. Think About It: Prolog Inference vs. Classical Logic

### Core Mechanism:
$$\text{Facts} + \text{Rules} \rightarrow \text{Inference (Backward Chaining / SLD Resolution)} \rightarrow \text{Query Answer}$$

### Key Operational Distinctions:
While Prolog demonstrates rule-based deduction, it differs from classical logic in several operational ways:

1. **Direction of Execution (SLD Resolution):** Prolog evaluates queries backwards from the goal to the facts (Backward Chaining), matching goals against rule heads and resolving subgoals.
2. **Unification:** Prolog automatically matches terms and binds variables during resolution.
3. **Negation as Failure (NAF):** In classical logic, something unprovable is not necessarily false (it may be indeterminate). In Prolog, failing to prove a goal within the closed-world assumption causes it to evaluate as `false.`.
