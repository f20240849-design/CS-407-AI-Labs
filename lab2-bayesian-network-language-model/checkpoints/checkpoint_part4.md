# Checkpoint Part IV: Constructing the Conditional Probability Table

## Overview & Task Summary
Part IV constructs the First-Order Conditional Probability Table (CPT) $P(X_t \mid X_{t-1})$ using Maximum Likelihood Estimation (MLE) from transition counts:

$$P(w_j \mid w_i) = \frac{C(w_i, w_j)}{\sum_{k} C(w_i, w_k)}$$

where $C(w_i, w_j)$ is the frequency of word $w_j$ directly following word $w_i$ in the dataset.

---

## Question 3 Answer

### Question:
*Construct the conditional probability distribution $P(\text{next word} \mid \text{current word})$ for at least the following words: `the`, `cat`, `dog`, `sat`, `ran`. Identify any zero-probability transitions.*

### Complete Response:

#### 1. Transition Distribution for `the`:
Total observed occurrences of `the` as preceding context: **12**
- $C(\text{the}, \text{cat}) = 3 \implies P(\text{cat} \mid \text{the}) = \frac{3}{12} = 0.2500$
- $C(\text{the}, \text{dog}) = 3 \implies P(\text{dog} \mid \text{the}) = \frac{3}{12} = 0.2500$
- $C(\text{the}, \text{mat}) = 2 \implies P(\text{mat} \mid \text{the}) = \frac{2}{12} \approx 0.1667$
- $C(\text{the}, \text{park}) = 2 \implies P(\text{park} \mid \text{the}) = \frac{2}{12} \approx 0.1667$
- $C(\text{the}, \text{rug}) = 2 \implies P(\text{rug} \mid \text{the}) = \frac{2}{12} \approx 0.1667$
- **Zero-Probability Transitions from `the`**: `sat`, `ran`, `on`, `to`, `the`, `<START>`, `<END>` ($P = 0.0$).

#### 2. Transition Distribution for `cat`:
Total observed occurrences of `cat` as preceding context: **3**
- $C(\text{cat}, \text{sat}) = 2 \implies P(\text{sat} \mid \text{cat}) = \frac{2}{3} \approx 0.6667$
- $C(\text{cat}, \text{ran}) = 1 \implies P(\text{ran} \mid \text{cat}) = \frac{1}{3} \approx 0.3333$
- **Zero-Probability Transitions from `cat`**: `the`, `dog`, `mat`, `rug`, `park`, `on`, `to`, `<START>`, `<END>` ($P = 0.0$).

#### 3. Transition Distribution for `dog`:
Total observed occurrences of `dog` as preceding context: **3**
- $C(\text{dog}, \text{sat}) = 2 \implies P(\text{sat} \mid \text{dog}) = \frac{2}{3} \approx 0.6667$
- $C(\text{dog}, \text{ran}) = 1 \implies P(\text{ran} \mid \text{dog}) = \frac{1}{3} \approx 0.3333$
- **Zero-Probability Transitions from `dog`**: `the`, `cat`, `mat`, `rug`, `park`, `on`, `to`, `<START>`, `<END>` ($P = 0.0$).

#### 4. Transition Distribution for `sat`:
Total observed occurrences of `sat` as preceding context: **4**
- $C(\text{sat}, \text{on}) = 4 \implies P(\text{on} \mid \text{sat}) = \frac{4}{4} = 1.0000$
- **Zero-Probability Transitions from `sat`**: All tokens other than `on` ($P = 0.0$).

#### 5. Transition Distribution for `ran`:
Total observed occurrences of `ran` as preceding context: **2**
- $C(\text{ran}, \text{to}) = 2 \implies P(\text{to} \mid \text{ran}) = \frac{2}{2} = 1.0000$
- **Zero-Probability Transitions from `ran`**: All tokens other than `to` ($P = 0.0$).

---

## Evidence Section

### Complete CPT Matrix for All Contexts:

| Context ($w_i$) | Next Token ($w_j$) | Count $C(w_i, w_j)$ | Total $\sum C$ | Conditional Probability $P(w_j \mid w_i)$ |
| :--- | :--- | :--- | :--- | :--- |
| `<START>` | `the` | 6 | 6 | **1.0000** |
| `the` | `cat` | 3 | 12 | **0.2500** |
| `the` | `dog` | 3 | 12 | **0.2500** |
| `the` | `mat` | 2 | 12 | **0.1667** |
| `the` | `park` | 2 | 12 | **0.1667** |
| `the` | `rug` | 2 | 12 | **0.1667** |
| `cat` | `sat` | 2 | 3 | **0.6667** |
| `cat` | `ran` | 1 | 3 | **0.3333** |
| `dog` | `sat` | 2 | 3 | **0.6667** |
| `dog` | `ran` | 1 | 3 | **0.3333** |
| `sat` | `on` | 4 | 4 | **1.0000** |
| `ran` | `to` | 2 | 2 | **1.0000** |
| `on` | `the` | 4 | 4 | **1.0000** |
| `to` | `the` | 2 | 2 | **1.0000** |
| `mat` | `<END>` | 2 | 2 | **1.0000** |
| `rug` | `<END>` | 2 | 2 | **1.0000** |
| `park` | `<END>` | 2 | 2 | **1.0000** |
