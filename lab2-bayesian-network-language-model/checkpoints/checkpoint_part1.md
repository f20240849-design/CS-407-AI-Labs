# Checkpoint Part I: From Probability to Language

## Overview & Task Summary
Part I establishes the theoretical foundation connecting probability theory to autoregressive language modeling. Any sequence of words $X_1, X_2, \dots, X_T$ possesses a joint probability distribution $P(X_1, X_2, \dots, X_T)$. Using the general probability chain rule, this joint distribution can be factorized into a sequence of conditional probabilities without making any independence assumptions:

$$P(X_1, X_2, \dots, X_T) = P(X_1) \prod_{t=2}^{T} P(X_t \mid X_1, X_2, \dots, X_{t-1})$$

For the specific example sentence `"the cat sat on the mat"`, where:
- $X_1 = \text{the}$
- $X_2 = \text{cat}$
- $X_3 = \text{sat}$
- $X_4 = \text{on}$
- $X_5 = \text{the}$
- $X_6 = \text{mat}$

The full autoregressive chain-rule decomposition is:

$$P(X_1, \dots, X_6) = P(X_1) \cdot P(X_2 \mid X_1) \cdot P(X_3 \mid X_1, X_2) \cdot P(X_4 \mid X_1, X_2, X_3) \cdot P(X_5 \mid X_1, X_2, X_3, X_4) \cdot P(X_6 \mid X_1, \dots, X_5)$$

---

## Question 1 Answer

### Question:
*Why is this decomposition useful for generating text? Write a short explanation in your lab record.*

### Complete Response:
The chain-rule decomposition is fundamental to autoregressive text generation for three key reasons:

1. **Reduction of High-Dimensional Joint Space to Sequential Step Decisions**: 
   Directly estimating or sampling from a joint distribution $P(X_1, X_2, \dots, X_T)$ over all possible sentences of length $T$ is computationally intractable because the total number of possible sequences grows exponentially as $|V|^T$ (where $|V|$ is the vocabulary size). The chain rule breaks this intractable global problem into a sequence of tractable, local next-token predictions $P(X_t \mid X_1, \dots, X_{t-1})$.

2. **Enables Step-by-Step Causal Text Generation**: 
   By expressing sequence probability as a product of conditional distributions, text generation can proceed left-to-right (causally). At step $t$, the generator conditions on the already-generated context $(X_1, \dots, X_{t-1})$, samples the next token $X_t \sim P(X_t \mid X_1, \dots, X_{t-1})$, appends $X_t$ to the context, and repeats.

3. **Incremental Memory and State Updates**: 
   The model does not need to decide the entire sequence upfront. At each step, it incorporates newly generated history to dynamically revise the probability distribution for subsequent tokens.

---

## Evidence Section

### Mathematical Chain Rule Decomposition Step-by-Step:

```text
Step 1: P(X_1 = 'the')
Step 2: P(X_2 = 'cat' | X_1 = 'the')
Step 3: P(X_3 = 'sat' | X_1 = 'the', X_2 = 'cat')
Step 4: P(X_4 = 'on'  | X_1 = 'the', X_2 = 'cat', X_3 = 'sat')
Step 5: P(X_5 = 'the' | X_1 = 'the', X_2 = 'cat', X_3 = 'sat', X_4 = 'on')
Step 6: P(X_6 = 'mat' | X_1 = 'the', X_2 = 'cat', X_3 = 'sat', X_4 = 'on', X_5 = 'the')

Joint Product = P(X_1) * P(X_2|X_1) * P(X_3|X_1,X_2) * P(X_4|X_1..X_3) * P(X_5|X_1..X_4) * P(X_6|X_1..X_5)
```
