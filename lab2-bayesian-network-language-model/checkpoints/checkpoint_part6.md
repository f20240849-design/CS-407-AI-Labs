# Checkpoint Part VI: Inspect the LLM-Generated Code

## Overview & Task Summary
Part VI performs a formal code inspection of the LLM-generated Python implementation (`src/bigram_model.py`) to verify that the internal mechanics correspond precisely to the theoretical Bayesian network specification.

---

## Question Answers

### Question 4:
*Where in the program are the transition counts stored?*

#### Answer:
In `src/bigram_model.py`, transition counts $C(w_i, w_j)$ are stored in the instance attribute `self.counts`, initialized as a nested `collections.defaultdict`:

```python
self.counts = defaultdict(lambda: defaultdict(int))
```

During training inside `train()`, transition counts are updated in lines 46–50:

```python
for i in range(len(tokens) - 1):
    w_curr = tokens[i]
    w_next = tokens[i + 1]
    self.counts[w_curr][w_next] += 1
```

---

### Question 5:
*Where is $P(X_t \mid X_{t-1})$ computed?*

#### Answer:
The conditional probability distribution $P(X_t = w_j \mid X_{t-1} = w_i)$ is computed inside `train()` in lines 53–56 of `src/bigram_model.py`:

```python
for w_curr, next_dict in self.counts.items():
    total = sum(next_dict.values())
    for w_next, count in next_dict.items():
        self.probabilities[w_curr][w_next] = count / total
```

The computed distributions are stored in `self.probabilities`, where `self.probabilities[w_curr][w_next]` maps directly to $P(w_{\text{next}} \mid w_{\text{curr}})$.

---

### Question 6:
*How does the program choose the next word? Is it: 1. always choosing the most probable word, or 2. sampling from the probability distribution? Explain the difference.*

#### Answer:
The program implements **both** methods to demonstrate the fundamental distinction:

1. **`predict_next_greedy(current_word)` (Greedy Argmax Selection)**:
   - Always selects the word $w$ that maximizes the conditional probability: $\arg\max_{w} P(w \mid w_{\text{current}})$.
   - **Behavior**: Completely deterministic. Given the same starting context, it always generates the exact same sequence.
   - **Limitation**: Can cause repetitive loops and lacks creative diversity.

2. **`predict_next_sample(current_word)` (Probabilistic Sampling)**:
   - Uses `random.choices(words, weights=probs, k=1)[0]` to sample a candidate word proportionally to its probability $P(w \mid w_{\text{current}})$.
   - **Behavior**: Stochastic. Words with higher probabilities are selected more frequently, but lower-probability words have a non-zero chance of selection.
   - **Advantage**: Generates diverse sentences reflecting the full probability distribution.

---

### Question 7:
*What happens if the program encounters a word for which no transition has been observed?*

#### Answer:
If an unobserved word is queried, `self.probabilities[current_word]` will be empty.
To handle this without crashing, `get_distribution(current_word)` implements an explicit, documented fallback policy in lines 62–67 of `src/bigram_model.py`:

```python
def get_distribution(self, current_word: str) -> Dict[str, float]:
    if current_word in self.probabilities and self.probabilities[current_word]:
        return dict(self.probabilities[current_word])
    else:
        # Documented Unseen Word Policy:
        # Emit <END> with probability 1.0 to ensure deterministic sequence termination.
        return {self.end_token: 1.0}
```

If an unseen word is encountered during text generation, the model returns `{ "<END>": 1.0 }`, gracefully terminating the sentence generation loop without raising a `KeyError` or entering an infinite loop.

---

## Evidence Section

### Verified Code Line Mapping ([bigram_model.py](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/src/bigram_model.py)):
- **Count Storage**: `self.counts` (`defaultdict(lambda: defaultdict(int))`), L32, L49.
- **Probability Computation**: `count / total`, L56.
- **Selection Methods**: `predict_next_greedy` (L70), `predict_next_sample` (L80).
- **Unseen Word Policy**: `get_distribution` fallback returning `{self.end_token: 1.0}`, L67.
