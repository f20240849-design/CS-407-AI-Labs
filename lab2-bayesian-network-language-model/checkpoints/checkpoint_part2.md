# Checkpoint Part II: A Bayesian Network for Text

## Overview & Task Summary
Part II formulates the autoregressive language model as a Directed Acyclic Graph (DAG), specifically a Bayesian Network. In a general Bayesian network, the joint probability is:

$$P(X_1, X_2, \dots, X_T) = \prod_{t=1}^{T} P(X_t \mid \text{Parents}(X_t))$$

For a first-order Markov language model represented by the chain network:

$$X_1 \longrightarrow X_2 \longrightarrow X_3 \longrightarrow \dots \longrightarrow X_T$$

Each word variable $X_t$ has exactly one parent node: $\text{Parents}(X_t) = \{X_{t-1}\}$.

---

## Question 2 Answer

### Question:
*What independence assumption is being made by this network? Express your answer using probability notation.*

### Complete Response:
The network makes the **First-Order Markov Independence Assumption** (also known as local conditional independence).

### Formal Definition in Probability Notation:
For any token position $t > 1$, the probability of token $X_t$ given all preceding tokens $(X_1, X_2, \dots, X_{t-1})$ is conditionally independent of all tokens prior to $X_{t-1}$:

$$P(X_t \mid X_1, X_2, \dots, X_{t-1}) = P(X_t \mid X_{t-1})$$

Equivalently, using the conditional independence notation $(A \perp B \mid C)$:

$$(X_t \perp \{X_1, X_2, \dots, X_{t-2}\} \mid X_{t-1}) \quad \forall t \ge 3$$

### Factorized Joint Distribution Under Assumption:
Applying this assumption simplifies the exact chain-rule factorisation into:

$$P(X_1, X_2, \dots, X_T) = P(X_1) \prod_{t=2}^{T} P(X_t \mid X_{t-1})$$

For a sequence of four tokens $(X_1, X_2, X_3, X_4)$:

$$P(X_1, X_2, X_3, X_4) = P(X_1) \cdot P(X_2 \mid X_1) \cdot P(X_3 \mid X_2) \cdot P(X_4 \mid X_3)$$

---

## Evidence Section

### Graph Structure & Dependency Mapping:

```text
[X_1] ---> [X_2] ---> [X_3] ---> [X_4] ---> ... ---> [X_T]

Parent Sets:
Parents(X_1) = {}
Parents(X_2) = {X_1}
Parents(X_3) = {X_2}        (X_3 is conditionally independent of X_1 given X_2)
Parents(X_4) = {X_3}        (X_4 is conditionally independent of X_1, X_2 given X_3)
Parents(X_t) = {X_{t-1}}    (X_t is conditionally independent of X_1..X_{t-2} given X_{t-1})
```
