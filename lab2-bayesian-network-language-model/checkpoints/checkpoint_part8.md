# Checkpoint Part VIII: Predicting the Next Word

## Overview & Task Summary
Part VIII evaluates single-step next-token predictions by calculating conditional probability distributions $P(X_{t+1} \mid X_t = w)$ for five preceding context words (`the`, `cat`, `dog`, `sat`, `ran`) and determining their deterministic greedy predictions using $\arg\max_w P(w \mid w_{\text{preceding}})$.

---

## Empirical Prediction Results (First-Order Bigram Model)

1. **Preceding Context: `the`**
   - **Distribution**: `{'cat': 0.2500, 'dog': 0.2500, 'mat': 0.1667, 'park': 0.1667, 'rug': 0.1667}`
   - **$\arg\max P(w \mid \text{the})$**: `'cat'` *(Alphabetical tie-breaking between 'cat' (0.25) and 'dog' (0.25))*.

2. **Preceding Context: `cat`**
   - **Distribution**: `{'sat': 0.6667, 'ran': 0.3333}`
   - **$\arg\max P(w \mid \text{cat})$**: `'sat'` *(0.6667)*.

3. **Preceding Context: `dog`**
   - **Distribution**: `{'sat': 0.6667, 'ran': 0.3333}`
   - **$\arg\max P(w \mid \text{dog})$**: `'sat'` *(0.6667)*.

4. **Preceding Context: `sat`**
   - **Distribution**: `{'on': 1.0000}`
   - **$\arg\max P(w \mid \text{sat})$**: `'on'` *(1.0000)*.

5. **Preceding Context: `ran`**
   - **Distribution**: `{'to': 1.0000}`
   - **$\arg\max P(w \mid \text{ran})$**: `'to'` *(1.0000)*.

---

## Question 9 Answer

### Question:
*Are the most probable predictions always the same as the words that you would personally expect? What does this tell you about the difference between a probability model and human linguistic expectations?*

### Complete Response:
**No**, the most probable model predictions are not always aligned with human linguistic expectations.

### Differences Between a Probability Model and Human Linguistic Expectations:

1. **Statistical Empirical Frequencies vs Deep Semantic World Knowledge**:
   - A probability model strictly reflects raw transition frequencies empirical to its training dataset. It has no intrinsic understanding of syntax, physical reality, or semantic plausibility.
   - For example, if given context `the`, the model predicts `cat` simply because `cat` appeared 3 times out of 12 in the training corpus. It cannot evaluate whether a `dog`, `bird`, or `car` makes more logical sense in a broader context.

2. **Lack of Long-Range Context and Pragmatics**:
   - Human linguistic expectations rely on deep discourse memory, pragmatics, situational context, and real-world common sense.
   - A first-order model forgets everything prior to the immediately preceding word ($X_{t-1}$). Consequently, after predicting `the`, it considers `mat`, `rug`, and `park` equally valid choices regardless of whether the subject was a `cat` or `dog`, or whether the action was `sat on` or `ran to`.

3. **Sensitivity to Dataset Bias and Sparsity**:
   - Human language expectations accommodate billions of valid grammatical construct variations.
   - A statistical n-gram model assigns probability **0.0** to any word missing from its local training transitions, even if the phrasing is completely natural in standard English (e.g. `the cat slept` receives $P=0$ because `slept` is absent from training data).

---

## Evidence Section

### Summary Table of Distributions & Argmax Predictions:

| Preceding Word ($X_t$) | Candidate Words & Probabilities | $\arg\max_w P(w \mid X_t)$ | Human Expectation Alignment Notes |
| :--- | :--- | :--- | :--- |
| `the` | `cat`: 0.25, `dog`: 0.25, `mat`: 0.17, `park`: 0.17, `rug`: 0.17 | `cat` | Tied between `cat` & `dog`; tie broken alphabetically. |
| `cat` | `sat`: 0.67, `ran`: 0.33 | `sat` | `sat` preferred 2:1 over `ran` in corpus. |
| `dog` | `sat`: 0.67, `ran`: 0.33 | `sat` | `sat` preferred 2:1 over `ran` in corpus. |
| `sat` | `on`: 1.00 | `on` | Deterministic transition in corpus ($P=1.0$). |
| `ran` | `to` : 1.00 | `to` | Deterministic transition in corpus ($P=1.0$). |
