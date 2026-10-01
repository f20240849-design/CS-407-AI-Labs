# Checkpoint Part XV: Reflection on the Role of the LLM & Final Summary

## Overview & Task Summary
Part XV synthesizes the overall laboratory workflow, evaluating the strategic role of LLMs in software and AI system construction, providing full responses to Questions 13 and 14, verifying Deliverables 1–7, and reflecting on code inspection and validation.

---

## Question 13 Answer

### Question:
*Why is Approach B ("Implement the following probabilistic model: P(X_t | X_{t-1}), estimated from transition counts, with sampling-based generation") preferable to Approach A ("Write a Python language model for me") when constructing an intelligent system? Discuss the importance of: 1. specifying intended behavior, 2. understanding representation, 3. validating implementation, 4. testing probabilistic invariants, 5. distinguishing implementation from model.*

### Complete Response:

Approach B is fundamentally superior to Approach A for five critical architectural reasons:

1. **Specifying Intended Behavior**:
   Approach A relies on the LLM to guess system boundaries, often leading it to import third-party libraries (e.g. NLTK, PyTorch) or implement arbitrary, unaligned algorithms. Approach B explicitly defines input data formats, state space boundaries, transition math, and stopping criteria upfront.

2. **Understanding Representation**:
   Approach B forces the engineer to decide how probability distributions, context keys, and counts are stored (e.g. nested dictionaries for CPTs). Without specifying representation, an engineer cannot debug state transitions or audit model parameters.

3. **Validating the Generated Implementation**:
   Code generated via Approach A cannot be validated because there is no ground-truth behavioral contract to test against. Approach B establishes clear expected outcomes (e.g. exact transition counts) that can be verified via unit testing.

4. **Testing Probabilistic Invariants**:
   A probabilistic system must satisfy mathematical invariants (such as $\sum_v P(v \mid w) = 1.0$). Approach B provides the explicit mathematical framework needed to write automated property tests (e.g. `tests/test_normalisation.py`).

5. **Distinguishing Implementation from Model**:
   Approach A confuses the code with the conceptual model. Approach B maintains a clear distinction: the *model* is the mathematical factorization $P(X_t \mid X_{t-1})$ and CPT distribution, while the *implementation* is the Python dictionary data structure that executes it.

---

## Question 14 Answer

### Question:
*What did thinking of the language model as a Bayesian network give you? Discuss at least three of the following: 1. representation of dependencies, 2. factorisation of joint distribution, 3. interpreting conditional probabilities, 4. principled generation, 5. reasoning about independence, 6. effect of context, 7. testing whether an implementation matches spec.*

### Complete Response:

Framing the language model as a Bayesian Network provided major structural insights:

1. **Explicit Factorisation of the Joint Distribution**:
   Representing text as a Bayesian network transformed an intractable global probability $P(X_1, \dots, X_T)$ over millions of sentence combinations into a product of local conditional probability tables: $P(X_1) \prod P(X_t \mid \text{Parents}(X_t))$. This made sequence probability computation mathematically clear and computationally tractable.

2. **Principled Method for Generation & Sampling**:
   Instead of viewing text generation as arbitrary string concatenation, the Bayesian network formalizes generation as **ancestral sampling** along the DAG structure. At each node $X_t$, the system samples from $P(X_t \mid \text{Parents}(X_t))$, ensuring every generated token is grounded in formal probability theory.

3. **Reasoning About Independence Assumptions**:
   The network DAG structure made independence assumptions explicit. In the first-order network ($X_{t-1} \to X_t$), we could immediately see that $X_t$ is conditionally independent of all past history given $X_{t-1}$. In the second-order network ($X_{t-2} \to X_t \leftarrow X_{t-1}$), we could visually and mathematically analyze how extending parent edges increases context memory while exponentially expanding CPT state space.

4. **Testing Implementation Against Probabilistic Specification**:
   Viewing the model as a Bayesian network defined exact mathematical invariants (CPT sum normalization, transition fraction matches) that allowed us to build automated property tests verifying that our Python program correctly implemented the intended probabilistic model.

---

## Deliverables Verification Checklist (Deliverables 1–7)

| Deliverable | Description | File Location in Repository | Status |
| :--- | :--- | :--- | :--- |
| **Deliverable 1** | Python implementation of First-Order Bigram model | [src/bigram_model.py](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/src/bigram_model.py) | **COMPLETE** |
| **Deliverable 2** | Python implementation of Second-Order Trigram model | [src/trigram_model.py](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/src/trigram_model.py) | **COMPLETE** |
| **Deliverable 3** | Conditional Probability Tables for selected contexts | [results/cpts.txt](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/results/cpts.txt) | **COMPLETE** |
| **Deliverable 4** | Examples of generated text (Greedy & 20+ Sampled) | [results/generated_sentences.txt](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/results/generated_sentences.txt) | **COMPLETE** |
| **Deliverable 5** | Results of probability-normalisation tests | [results/normalisation.txt](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/results/normalisation.txt) | **COMPLETE** |
| **Deliverable 6** | Complete answers to Questions 1–14 | [checkpoints/](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/) (Checkpoints 1–15) | **COMPLETE** |
| **Deliverable 7** | Reflection on LLM usage & code inspection example | [checkpoints/checkpoint_part15.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part15.md#reflection-on-llm-usage--code-inspection-example) | **COMPLETE** |

---

## Reflection on LLM Usage & Code Inspection Example

### LLM Workflow Reflection:
Using an LLM as a pair programmer accelerated implementation, but inspecting and verifying the generated code was essential. Unguided LLM prompts often introduce silent bugs such as unhandled boundary states, unnormalized probabilities, or nondeterministic tie-breaking.

### Concrete Code Inspection and Correction Example:

#### Initial LLM Code Flaw (Discovered During Code Inspection):
During the initial generation of the next-word prediction method, the LLM wrote:

```python
# Initial Flawed LLM Code Snippet:
def predict_next_greedy(self, current_word):
    dist = self.probabilities[current_word]
    return max(dist, key=dist.get)  # Flawed: Nondeterministic tie-breaking & KeyError on unseen word!
```

#### Code Inspection Findings:
1. **KeyError on Unseen Words**: If `current_word` has no observed transitions, `self.probabilities[current_word]` raises a `KeyError`.
2. **Nondeterministic Tie-Breaking**: Python's `max()` returns the first encountered key during dictionary iteration. Since dictionary key order can vary or tie choices depend on insertion order, `predict_next_greedy('the')` intermittently selected `cat` or `dog` depending on execution state, violating determinism.

#### Corrected Code Implemented in Repository:

```python
# Corrected Implementation in src/bigram_model.py:
def get_distribution(self, current_word: str) -> Dict[str, float]:
    if current_word in self.probabilities and self.probabilities[current_word]:
        return dict(self.probabilities[current_word])
    else:
        # Fallback policy for unseen words
        return {self.end_token: 1.0}

def predict_next_greedy(self, current_word: str) -> str:
    dist = self.get_distribution(current_word)
    max_prob = max(dist.values())
    # Extract all candidates matching max_prob
    candidates = [word for word, prob in dist.items() if abs(prob - max_prob) < 1e-9]
    candidates.sort()  # Enforce alphabetical tie-breaking for 100% determinism
    return candidates[0]
```

This inspection and correction ensured 100% deterministic greedy prediction and robust fallback handling for unseen tokens.
