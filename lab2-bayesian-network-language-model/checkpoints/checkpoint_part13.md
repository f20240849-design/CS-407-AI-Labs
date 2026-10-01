# Checkpoint Part XIII: Comparing the Two Models

## Overview & Task Summary
Part XIII presents an empirical and theoretical comparison of the First-Order (Bigram) and Second-Order (Trigram) models based on experimental metrics calculated by `src/compare_models.py`.

---

## Empirical Comparison Metrics

| Metric | First-Order (Bigram) | Second-Order (Trigram) | Difference / Impact |
| :--- | :--- | :--- | :--- |
| **Context Length** | 1 token | 2 tokens | Double context window |
| **Total Context Tuple Space ($|V|^k$)** | 12 states | 144 states | **12x expansion** in context state space |
| **Observed Context States** | 11 states | 15 states | Only 4 additional context states observed |
| **Zero-Probability Context States** | **1 state (8.3%)** | **129 states (89.6%)** | **Severe data sparsity in Trigram** |
| **Non-Zero CPT Parameters** | **14 parameters** | **19 parameters** | 5 additional conditional parameters |
| **Generation Diversity (Unique/20)** | **10/20 (50%)** | **5/20 (25%)** | Trigram diversity drops due to corpus memorization |

---

## Question 12 Answer

### Question:
*Why does increasing the amount of context potentially improve prediction? Why can it simultaneously make the model harder to estimate from limited data? Relate your answer to the size of the conditional probability table.*

### Complete Response:

#### 1. Why Increasing Context Improves Prediction:
Extending context length from $X_{t-1}$ to $(X_{t-2}, X_{t-1})$ provides richer structural and semantic information. 
In the bigram model, given current word `the`, the model cannot determine whether the preceding verb was `sat on` or `ran to`. It assigns equal probability mass to `mat`, `rug`, and `park`, leading to ungrammatical outputs like `ran to the mat`. 
In the trigram model, conditioning on `('to', 'the')` uniquely isolates `park` ($P=1.0$), eliminating invalid combinations and improving prediction accuracy and coherence.

#### 2. Why Increasing Context Makes Estimation Harder (Curse of Dimensionality):
Simultaneously, increasing context length causes an exponential expansion in the size of the Conditional Probability Table. 
For a vocabulary of size $|V|$, a $k$-order model requires a CPT table with $|V|^k$ context rows and $|V|^{k+1}$ potential cell entries:
- Bigram CPT size ($k=1$): $12^1 = 12$ context states.
- Trigram CPT size ($k=2$): $12^2 = 144$ context states.
- 4-gram CPT size ($k=3$): $12^3 = 1,728$ context states.

#### 3. Mathematical Impact on Data Estimation:
As context state space grows exponentially ($|V|^k$), the amount of training data required to observe each context tuple multiple times grows exponentially. 
With limited training data (6 sentences), 129 out of 144 trigram context tuples (89.6%) are never observed in training data. Their transition probabilities default to 0.0 or trigger fallback policies, making the model overly rigid, unable to generalize, and prone to memorizing training sentences.

---

## Evidence Section

Refer to the generated markdown report in [results/comparison.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/results/comparison.md).
