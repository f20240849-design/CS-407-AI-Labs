# Checkpoint Part VII: Test the Probability Model

## Overview & Task Summary
Part VII implements property-based testing to validate a fundamental probabilistic invariant that must hold for every valid conditional distribution:

$$\sum_{v \in V} P(v \mid w) = 1.0 \quad \forall w \in \text{Contexts}$$

The automated test script `tests/test_normalisation.py` iterates over every context state in both Bigram and Trigram models and verifies that the sum of output probabilities equals 1.0 within numerical precision tolerance ($\epsilon = 10^{-6}$).

---

## Question 8 Answer

### Question:
*If one of the totals is 0.87, what does this tell you about the implementation?*

### Complete Response:
If a context total equals **0.87** instead of **1.0**, it proves that the implementation contains a critical bug in probability construction or normalization. Specific root causes include:

1. **Incorrect Denominator Calculation**:
   The code divided transition counts by an incorrect total (e.g. dividing by corpus size or vocabulary length $|V|$ instead of the sum of outgoing transition counts $\sum_k C(w, w_k)$).

2. **Dropped or Omitted Transition Events**:
   Certain valid next tokens were excluded from the transition dictionary during count aggregation or CPT population (e.g. ignoring boundary tokens like `<END>`).

3. **Floating-Point Truncation or Unnormalized Smoothing**:
   If Laplace smoothing or unnormalized frequency weights were added without re-normalizing the distribution by dividing by the updated partition function $Z = \sum_v \tilde{P}(v \mid w)$.

4. **Consequences for Text Generation**:
   A distribution summing to 0.87 leaves 13% of probability mass unassigned. If passed to a weighted sampler like `random.choices`, it distorts selection frequencies or raises runtime errors if raw weights do not match expected sum constraints.

---

## Evidence Section

### Verified Output Log from `results/normalisation.txt`:

```text
============================================================
       PROBABILITY NORMALISATION TEST RESULTS
============================================================

--- FIRST-ORDER BIGRAM MODEL NORMALISATION ---
Context '<START> ': sum = 1.000000 [PASSED]
Context 'cat     ': sum = 1.000000 [PASSED]
Context 'dog     ': sum = 1.000000 [PASSED]
Context 'mat     ': sum = 1.000000 [PASSED]
Context 'on      ': sum = 1.000000 [PASSED]
Context 'park    ': sum = 1.000000 [PASSED]
Context 'ran     ': sum = 1.000000 [PASSED]
Context 'rug     ': sum = 1.000000 [PASSED]
Context 'sat     ': sum = 1.000000 [PASSED]
Context 'the     ': sum = 1.000000 [PASSED]
Context 'to      ': sum = 1.000000 [PASSED]

Bigram Normalisation Status: ALL PASSED

--- SECOND-ORDER TRIGRAM MODEL NORMALISATION ---
Context '(<START>, <START>)': sum = 1.000000 [PASSED]
Context '(<START>, the)  ': sum = 1.000000 [PASSED]
Context '(cat, ran)      ': sum = 1.000000 [PASSED]
Context '(cat, sat)      ': sum = 1.000000 [PASSED]
Context '(dog, ran)      ': sum = 1.000000 [PASSED]
Context '(dog, sat)      ': sum = 1.000000 [PASSED]
Context '(on, the)       ': sum = 1.000000 [PASSED]
Context '(ran, to)       ': sum = 1.000000 [PASSED]
Context '(sat, on)       ': sum = 1.000000 [PASSED]
Context '(the, cat)      ': sum = 1.000000 [PASSED]
Context '(the, dog)      ': sum = 1.000000 [PASSED]
Context '(the, mat)      ': sum = 1.000000 [PASSED]
Context '(the, park)     ': sum = 1.000000 [PASSED]
Context '(the, rug)      ': sum = 1.000000 [PASSED]
Context '(to, the)       ': sum = 1.000000 [PASSED]

Trigram Normalisation Status: ALL PASSED
============================================================
```
