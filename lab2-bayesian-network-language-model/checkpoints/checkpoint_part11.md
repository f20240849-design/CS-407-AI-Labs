# Checkpoint Part XI: A Second-Order Bayesian Network

## Overview & Task Summary
Part XI extends the language model to a Second-Order Markov model (Trigram Model). Instead of assuming $P(X_t \mid X_1, \dots, X_{t-1}) \approx P(X_t \mid X_{t-1})$, the second-order model conditions on two preceding tokens:

$$P(X_t \mid X_1, \dots, X_{t-1}) \approx P(X_t \mid X_{t-2}, X_{t-1})$$

The corresponding joint probability factorisation for a sequence $(X_1, X_2, X_3, X_4)$ with double start context $(\langle\text{START}\rangle, \langle\text{START}\rangle)$ is:

$$P(X_1, X_2, X_3, X_4) = P(X_1 \mid \langle\text{START}\rangle, \langle\text{START}\rangle) \cdot P(X_2 \mid \langle\text{START}\rangle, X_1) \cdot P(X_3 \mid X_1, X_2) \cdot P(X_4 \mid X_2, X_3)$$

---

## Question 11 Answer

### Question:
*How does the second-order model differ from the first-order model in terms of:*
1. *the graph structure?*
2. *the conditional probability table?*
3. *the amount of context available for prediction?*
4. *the amount of data needed?*

### Complete Response:

#### 1. Graph Structure:
- **First-Order Graph**: A simple directed linear chain: $X_{t-1} \longrightarrow X_t$. Each node has a single parent ($\text{Parents}(X_t) = \{X_{t-1}\}$).
- **Second-Order Graph**: A directed graph where each node $X_t$ has **two incoming directed edges** from its two immediate predecessors:
  
  $$X_{t-2} \longrightarrow X_t \longleftarrow X_{t-1}$$

  The parent set is extended to $\text{Parents}(X_t) = \{X_{t-2}, X_{t-1}\}$.

#### 2. Conditional Probability Table (CPT):
- **First-Order CPT**: Matrix of shape $|V| \times |V|$ storing 2D entries $P(X_t = w_j \mid X_{t-1} = w_i)$.
- **Second-Order CPT**: 3D Tensor or nested map of shape $|V| \times |V| \times |V|$ storing entries $P(X_t = w_k \mid X_{t-2} = w_i, X_{t-1} = w_j)$.
- The total potential parameter space increases from $|V|^2$ to $|V|^3$.

#### 3. Amount of Context Available for Prediction:
- **First-Order Model**: 1 token of historical context window ($X_{t-1}$).
- **Second-Order Model**: 2 tokens of historical context window ($(X_{t-2}, X_{t-1})$).
- The model can disambiguate phrase choices that depend on 2-word combinations (e.g. distinguishing `ran to` $\to$ `park` from `sat on` $\to$ `mat`/`rug`).

#### 4. Amount of Data Needed:
- **First-Order Model**: Requires sufficient observations of token pairs ($C(w_i, w_j)$).
- **Second-Order Model**: Requires significantly more training data to reliably estimate triple counts ($C(w_i, w_j, w_k)$). Because context state space expands exponentially as $|V|^2$, small datasets lead to high data sparsity where most context tuples have 0 occurrences.

---

## Evidence Section

### Graph Structure Comparison Diagram:

```text
First-Order Bayesian Network:
[X_1] ---> [X_2] ---> [X_3] ---> [X_4]

Second-Order Bayesian Network:
[X_1] ---> [X_2] ---> [X_3] ---> [X_4]
  |          ^         ^          ^
  +----------+---------+          |
             +--------------------+
```
