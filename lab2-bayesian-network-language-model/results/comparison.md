# Model Comparison: First-Order (Bigram) vs Second-Order (Trigram)

This document provides a quantitative and qualitative comparison between the First-Order Markov model ($P(X_t | X_{t-1})$) and the Second-Order Markov model ($P(X_t | X_{t-2}, X_{t-1})$) trained on the 6-sentence dataset.

## 1. Quantitative Summary Table

| Metric | First-Order (Bigram) | Second-Order (Trigram) | Analysis / Explanation |
| :--- | :--- | :--- | :--- |
| **Vocabulary Size ($|V|$)** | 12 tokens | 12 tokens | Includes `<START>` and `<END>` tokens. |
| **Context Length** | 1 token ($X_{t-1}$) | 2 tokens ($X_{t-2}, X_{t-1}$) | Trigram considers double history context. |
| **Total Context Space** | 12 ($|V|^1$) | 144 ($|V|^2$) | Exponential expansion of context tuple space. |
| **Observed Contexts** | 11 | 15 | Contexts actually present in training data. |
| **Zero-Probability Contexts** | **1** (8.3%) | **129** (89.6%) | Unobserved context tuples in training set. |
| **Distinct Parameters (Non-zero CPT)** | **17** | **19** | Total non-zero conditional probabilities stored. |
| **Generation Diversity (Unique/20)** | **10/20** (50%) | **6/20** (30%) | Number of distinct sentences out of 20 samples. |

---

## 2. Qualitative Coherence & Sample Outputs

### First-Order Bigram Model Samples (Selected 5 of 20):
1. `<START> the cat sat on the rug <END>` (Valid)
2. `<START> the dog ran to the park <END>` (Valid)
3. `<START> the cat ran to the mat <END>` (Hybrid/Nonsensical combination across dataset sentences)
4. `<START> the dog sat on the park <END>` (Syntactically invalid combination enabled by first-order history loss)
5. `<START> the cat sat on the mat <END>` (Valid)

*Observations on Bigram Coherence*:
The Bigram model suffers from memory loss. Once it generates `the`, it predicts `mat`, `rug`, or `park` based only on `the` without remembering whether the verb was `sat on` or `ran to`. This allows grammatically questionable combinations like `ran to the mat` or `sat on the park`.

### Second-Order Trigram Model Samples (Selected 5 of 20):
1. `<START> the cat sat on the mat <END>` (Exact match from training corpus)
2. `<START> the cat sat on the rug <END>` (Exact match from training corpus)
3. `<START> the dog sat on the mat <END>` (Exact match from training corpus)
4. `<START> the dog ran to the park <END>` (Exact match from training corpus)
5. `<START> the cat ran to the park <END>` (Exact match from training corpus)

*Observations on Trigram Coherence*:
The Trigram model achieves 100% syntactic and semantic coherence because its 2-token context window (`on the` -> `mat`/`rug`, `to the` -> `park`) prevents impossible preposition-noun pairings. However, due to limited data, it mostly memorizes and reproduces exact corpus sentences.

---

## 3. Detailed Trade-off Analysis

### Why Increasing Context Improves Coherence
Extending context from $X_{t-1}$ to $(X_{t-2}, X_{t-1})$ conditions predictions on richer structural history. In English, prepositions like `to` vs `on` require distinct destination targets (`to the park` vs `on the mat/rug`). The trigram context (`ran`, `to`) uniquely isolates `park`, eliminating ungrammatical output like `ran to the mat`.

### The Curse of Dimensionality & Data Sparsity
As context length $k$ increases, context space grows exponentially as $|V|^k$.
- Bigram context space: $12^1 = 12$ states (1 zero-probability state, 8.3% sparsity).
- Trigram context space: $12^2 = 144$ states (129 zero-probability states, 89.6% sparsity).
- 4-gram context space: $12^4 = 20,736$ states.

For small datasets, most higher-order context tuples are never observed in training data ($P = 0$), causing severe data sparsity and rendering the model unable to generate novel valid sentences without smoothing or neural representation.
