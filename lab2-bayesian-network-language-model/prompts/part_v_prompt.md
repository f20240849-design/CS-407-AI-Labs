# Part V: LLM Specification Prompt for First-Order Model

## Verbatim Prompt from Lab Sheet (Part V)

```text
Write a simple Python implementation of a first-order autoregressive language model.
The model should:
1. take a list of tokenised sentences as training data;
2. count transitions between consecutive tokens;
3. construct the conditional distribution P(X_t | X_{t-1});
4. display the probabilities for a specified previous token;
5. predict the most probable next token;
6. generate a sentence by repeatedly sampling the next token;
7. stop when the <END> token is generated.
Do not use a machine-learning library or a pretrained language model. Use ordinary Python data structures and random sampling.
```

---

## Improved Version of Part V Prompt

```text
Write a modular, clean Python 3 class named `BigramLanguageModel` that implements a first-order autoregressive Markov language model using standard library data structures only (`collections.defaultdict`, `random`).

Functional & Behavioral Requirements:
1. Data Ingestion & Tokenisation:
   - Accept a list of raw string sentences (e.g., "the cat sat on the mat").
   - Convert text to lowercase, split into word tokens, and prepend `<START>` and append `<END>` tokens.
2. Transition Counting & CPT Estimation:
   - Build transition counts C(w_i, w_j) for all consecutive token pairs.
   - Compute exact Conditional Probability Table (CPT) entries P(X_t = w_j | X_{t-1} = w_i) = C(w_i, w_j) / sum_k C(w_i, w_k).
3. Querying & Distribution Inspection:
   - Provide a method `get_distribution(current_word: str) -> dict` returning the conditional probability distribution for any token.
   - Policy for unseen words or terminal states with no outgoing transitions: return `{"<END>": 1.0}` to ensure safe sequence termination.
4. Deterministic & Probabilistic Prediction:
   - Implement `predict_next_greedy(current_word: str) -> str` returning argmax_w P(w | current_word) with explicit alphabetical tie-breaking.
   - Implement `predict_next_sample(current_word: str) -> str` sampling according to P(X_t | X_{t-1}).
5. Text Generation:
   - Implement `generate_sentence(mode='sample', seed=None) -> str` starting from `<START>` and appending sampled/greedy tokens until `<END>` is emitted.
   - Support a `seed` argument for random reproducibility.

Constraints:
- Do NOT use third-party libraries (PyTorch, TensorFlow, NumPy, NLTK).
- Include comprehensive docstrings and clear variable names matching probabilistic notation.
```

---

## Why the Improved Version is Better

1. **Explicit Edge Case Handling**: Specifies an exact policy for unseen words and terminal states (`{"<END>": 1.0}`), preventing unhandled `KeyError` or zero-division runtime crashes.
2. **Deterministic Tie-Breaking**: Enforces alphabetical tie-breaking for `predict_next_greedy`, guaranteeing reproducible results across different Python environments.
3. **Reproducibility & Modularity**: Encapsulates state within an object-oriented class structure and adds explicit `seed` parameter support for repeatable probabilistic testing.
4. **Disambiguated Input Pipeline**: Defines exact pre-processing rules (lowercasing, padding with `<START>` and `<END>`), eliminating ambiguities in sentence boundaries.
