# Checkpoint Task 1: Construct a Plan by Hand

**Student Name:** AI Undergraduate Student  
**Lab Assignment:** Laboratory – Logical Reasoning for Planning  

---

## 1. Analysis of the Example Sequence from the Lab Sheet

The lab sheet suggests considering the candidate action sequence:
$$\text{Move}(A, B) \rightarrow \text{PickUp}(\text{Package, B}) \rightarrow \text{Move}(B, C) \rightarrow \text{Drop}(\text{Package, C})$$

### **Critique & Flaw Demonstration:**
This candidate sequence is **INVALID**. 

**Why it fails:**
1. In state $S_0 = \{\text{At(Robot, A)}, \text{At(Package, A)}\}$, executing $\text{Move}(A, B)$ shifts the robot to $B$, producing state $S_1 = \{\text{At(Robot, B)}, \text{At(Package, A)}\}$.
2. The next action proposed is $\text{PickUp}(\text{Package, B})$. The preconditions for this action are $\text{At(Robot, B)}$ and $\text{At(Package, B)}$.
3. Looking at $S_1$, $\text{At(Robot, B)} \in S_1$ is True, but **$\text{At(Package, B)} \notin S_1$** (the package is still at location $A$).
4. Because $\text{At(Package, B)}$ is unsatisfied, $S_1 \not\models \text{Preconditions}(\text{PickUp}(\text{Package, B}))$. The planner cannot execute this step!

---

## 2. Correct Hand-Constructed Plan

To successfully move the package from location $A$ to location $C$, the robot must pick up the package at location $A$ **before** traveling to location $B$.

### Valid Action Sequence:
1. $a_1 = \text{PickUp}(\text{Package, A})$
2. $a_2 = \text{Move}(A, B)$
3. $a_3 = \text{Move}(B, C)$
4. $a_4 = \text{Drop}(\text{Package, C})$

---

## 3. Step-by-Step State Transition Table & Precondition Proofs

| State | Action Applied ($a_i$) | Preconditions Required ($\text{Pre}(a_i)$) | Preconditions Satisfied? | Resulting State Propositions ($S_i$) |
| :--- | :--- | :--- | :--- | :--- |
| **$S_0$** | *(Initial State)* | N/A | N/A | `At(Robot, A)`, `At(Package, A)` |
| **$S_1$** | $\text{PickUp}(\text{Package, A})$ | `At(Robot, A)`, `At(Package, A)` | **YES** ($\text{Pre} \subseteq S_0$) | `At(Robot, A)`, `Holding(Package)` |
| **$S_2$** | $\text{Move}(A, B)$ | `At(Robot, A)` | **YES** ($\text{Pre} \subseteq S_1$) | `At(Robot, B)`, `Holding(Package)` |
| **$S_3$** | $\text{Move}(B, C)$ | `At(Robot, B)` | **YES** ($\text{Pre} \subseteq S_2$) | `At(Robot, C)`, `Holding(Package)` |
| **$S_4$** | $\text{Drop}(\text{Package, C})$ | `At(Robot, C)`, `Holding(Package)` | **YES** ($\text{Pre} \subseteq S_3$) | `At(Robot, C)`, `At(Package, C)` |

---

## 4. Goal Satisfaction Verification

- **Goal Proposition Set ($G$):** $\{\text{At(Package, C)}\}$
- **Final State ($S_4$):** $\{\text{At(Robot, C)}, \text{At(Package, C)}\}$

**Proof of Termination:**
$$G \subseteq S_4 \quad \Rightarrow \quad \{\text{At(Package, C)}\} \subseteq \{\text{At(Robot, C)}, \text{At(Package, C)}\} \quad \Rightarrow \quad \mathbf{True}$$

The hand-constructed 4-step plan is fully valid and achieves the goal.

---

## 5. Evidence Trace from Program Simulation

```text
Step 1: Execute PickUp(Package, A)
        State S1: ['At(Robot, A)', 'Holding(Package)']
Step 2: Execute Move(A, B)
        State S2: ['At(Robot, B)', 'Holding(Package)']
Step 3: Execute Move(B, C)
        State S3: ['At(Robot, C)', 'Holding(Package)']
Step 4: Execute Drop(Package, C)
        State S4: ['At(Package, C)', 'At(Robot, C)']
```
