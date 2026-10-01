# Checkpoint Part XII: Use the LLM Again

## Overview & Task Summary
Part XII uses LLM specification prompts to extend the first-order implementation into a second-order model ($P(X_t \mid X_{t-2}, X_{t-1})$) without introducing machine learning framework dependencies.

---

## Verbatim Lab Prompt (Part XII)

```text
Modify the existing first-order autoregressive model into a second-order model.
The model should estimate
P(X_t | X_{t-2}, X_{t-1}).
Represent the model using counts of observed triples and use these counts to construct conditional probability distributions.
Do not replace the model with a neural network or a pretrained language model.
```

---

## Implementation & Code Inspection Verification

The resulting implementation in `src/trigram_model.py` updates the probabilistic core as follows:

1. **Context Representation**: Context states are represented as 2-tuples `(w_{t-2}, w_{t-1})`.
2. **Initial State Convention**: The initial context is explicitly set to `('<START>', '<START>')`.
3. **Triple Counting**: Counts $C(w_{t-2}, w_{t-1}, w_t)$ are stored in `self.counts[context][target]`.
4. **CPT Calculation**: Computed via `self.probabilities[context][target] = count / total`.
5. **Fallback Policy for Unseen Tuples**: Returns `{ "<END>": 1.0 }` if an unobserved 2-token tuple is encountered.

---

## Evidence Section

Refer to the full prompt engineering analysis in [prompts/part_xii_prompt.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/prompts/part_xii_prompt.md) and Python source in [src/trigram_model.py](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/src/trigram_model.py).
