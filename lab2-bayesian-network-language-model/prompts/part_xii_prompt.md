# Part XII: LLM Specification Prompt for Second-Order Model

## Verbatim Prompt from Lab Sheet (Part XII)

```text
Modify the existing first-order autoregressive model into a second-order model.
The model should estimate
P(X_t | X_{t-2}, X_{t-1}).
Represent the model using counts of observed triples and use these counts to construct conditional probability distributions.
Do not replace the model with a neural network or a pretrained language model.
```

---

## Improved Version of Part XII Prompt

```text
Refactor the existing Python `BigramLanguageModel` into a robust `TrigramLanguageModel` class representing a second-order Markov autoregressive model estimation P(X_t | X_{t-2}, X_{t-1}).

Requirements:
1. Context Convention & Tokenisation:
   - Prepend double start tokens (`<START>`, `<START>`) and append single end token `<END>` to each input sentence.
   - Initial state context key must be the 2-tuple (`<START>`, `<START>`).
2. Triple Counting & CPT Construction:
   - Store observed triple counts C(w_{t-2}, w_{t-1}, w_t) using a nested dictionary structure keyed by context 2-tuples `(w_{t-2}, w_{t-1})`.
   - Calculate conditional distributions P(w_t | w_{t-2}, w_{t-1}) = C(w_{t-2}, w_{t-1}, w_t) / sum_k C(w_{t-2}, w_{t-1}, w_k).
3. Unseen Context Policy:
   - If queried with an unobserved context tuple `(w_a, w_b)`, return `{"<END>": 1.0}` to gracefully terminate generation without crashing.
4. Generation Modes:
   - Support both Mode A (Greedy Argmax with alphabetical tie-breaking) and Mode B (Probabilistic Sampling using `random.choices`).
   - State updating during generation: transition context from `(w_{t-2}, w_{t-1})` to `(w_{t-1}, w_t)`.
5. Constraints:
   - Use standard library Python structures only.
   - Maintain complete type annotations and clear documentation.
```

---

## Why the Improved Version is Better

1. **Explicit Multi-Token Context State Specification**: Clarifies the exact data structure for context representation (2-tuples `(w_{t-2}, w_{t-1})`) and state transition mechanics during text generation.
2. **Double Start Token Standardization**: Specifies `('<START>', '<START>')` context initialization, preventing indexing off-by-one errors on sentence beginnings.
3. **Robust Fallback Policy**: Defines fallback behavior for zero-frequency trigram context tuples, ensuring the sampling generator never encounters deadlocks.
4. **Architectural Parity**: Preserves exact feature symmetry (greedy tie-breaking, seeded sampling) with the first-order implementation for seamless comparative testing.
