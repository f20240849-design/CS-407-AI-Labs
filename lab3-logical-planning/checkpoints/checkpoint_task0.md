# Checkpoint Task 0: Understanding the Planning Problem

**Student Name:** AI Undergraduate Student  
**Lab Assignment:** Laboratory – Logical Reasoning for Planning  

---

## 1. Formal Problem Specification

### (a) Initial State ($I$)
$$I = \{\text{At(Robot, A)}, \text{At(Package, A)}\}$$

### (b) Goal State ($G$)
$$G = \{\text{At(Package, C)}\}$$

### (c) & (d) Domain Action Schemas (Preconditions and Effects)

1. **$\text{Move}(X, Y)$** (for connected locations $X \leftrightarrow Y \in \{(A,B), (B,A), (B,C), (C,B)\}$)
   - **Positive Preconditions:** $\{\text{At(Robot, } X)\}$
   - **Negative Preconditions:** $\emptyset$
   - **Positive Effects:** $\{\text{At(Robot, } Y)\}$
   - **Negative Effects:** $\{\text{At(Robot, } X)\}$

2. **$\text{PickUp}(\text{Package}, L)$** (for locations $L \in \{A, B, C\}$)
   - **Positive Preconditions:** $\{\text{At(Robot, } L), \text{At(Package, } L)\}$
   - **Negative Preconditions:** $\emptyset$
   - **Positive Effects:** $\{\text{Holding(Package)}\}$
   - **Negative Effects:** $\{\text{At(Package, } L)\}$

3. **$\text{Drop}(\text{Package}, L)$** (for locations $L \in \{A, B, C\}$)
   - **Positive Preconditions:** $\{\text{At(Robot, } L), \text{Holding(Package)}\}$
   - **Negative Preconditions:** $\emptyset$
   - **Positive Effects:** $\{\text{At(Package, } L)\}$
   - **Negative Effects:** $\{\text{Holding(Package)}\}$

---

## 2. Initial Action Applicability Analysis

Starting from state $I = \{\text{At(Robot, A)}, \text{At(Package, A)}\}$:

### Question 1: Is $\text{PickUp}(\text{Package, A})$ applicable?
**Answer:** **Yes, it is applicable.**  
**Explanation:** The preconditions for $\text{PickUp}(\text{Package, A})$ are $\text{At(Robot, A)}$ and $\text{At(Package, A)}$. Evaluating against state $I$:
- $\text{At(Robot, A)} \in I \quad \Rightarrow \quad \text{True}$
- $\text{At(Package, A)} \in I \quad \Rightarrow \quad \text{True}$

Since all positive preconditions are a subset of $I$ and there are no negative preconditions, $I \models \text{Preconditions}(\text{PickUp}(\text{Package, A}))$.

---

### Question 2: Is $\text{Drop}(\text{Package, C})$ applicable?
**Answer:** **No, it is not applicable.**  
**Explanation:** The preconditions for $\text{Drop}(\text{Package, C})$ are $\text{At(Robot, C)}$ and $\text{Holding(Package)}$. Evaluating against state $I$:
- $\text{At(Robot, C)} \in I \quad \Rightarrow \quad \text{False}$ (Robot is at A, not C)
- $\text{Holding(Package)} \in I \quad \Rightarrow \quad \text{False}$ (Robot is not holding the package)

Because neither precondition is satisfied in $I$, $I \not\models \text{Preconditions}(\text{Drop}(\text{Package, C}))$.

---

### Full List of Initially Applicable Actions from $I$
Out of all 10 defined domain actions, only **two** are initially applicable from $I$:
1. $\text{PickUp}(\text{Package, A})$
2. $\text{Move}(A, B)$

---

## 3. Think About It Reflection

> **Question:** An action should not be considered applicable merely because it appears in the list of available actions. Why?

**Reflection Answer:**  
In automated planning, available actions represent generic operators defined in the domain schema. However, physical real-world constraints dictate that an action can only be executed when the world is in a state that permits it. 

Logical reasoning enters planning at this exact point: before expanding a node during search, the agent must perform entailment checking ($S \models \text{Preconditions}(a)$). If an action's preconditions are not logically satisfied by the current state, attempting to execute that action is illegal and would result in execution failure or impossible state transitions.

---

## 4. Evidence Trace

```text
Evaluating Initial State I = {'At(Package, A)', 'At(Robot, A)'}

Action: PickUp(Package, A)
  Preconditions Needed : {'At(Package, A)', 'At(Robot, A)'}
  Subset of Initial I  : TRUE -> APPLICABLE

Action: Drop(Package, C)
  Preconditions Needed : {'At(Robot, C)', 'Holding(Package)'}
  Subset of Initial I  : FALSE -> NOT APPLICABLE
```
