# Checkpoint Part X: Deterministic vs Probabilistic Generation

## Overview & Task Summary
Part X compares two distinct text generation strategies:
- **Mode A: Greedy Generation**: Always selects the most probable next token $\arg\max_w P(w \mid w_{\text{prev}})$. Ties are broken alphabetically.
- **Mode B: Probabilistic Sampling**: Samples next tokens according to the conditional probability distribution $P(w \mid w_{\text{prev}})$.

---

## Empirical Sentence Output Comparison

### Mode A: Greedy Argmax Generation (5 Runs):
- **Run 1**: `<START> the cat sat on the mat <END>`
- **Run 2**: `<START> the cat sat on the mat <END>`
- **Run 3**: `<START> the cat sat on the mat <END>`
- **Run 4**: `<START> the cat sat on the mat <END>`
- **Run 5**: `<START> the cat sat on the mat <END>`

*Greedy Mode Summary*: **1 unique sentence** across all 5 runs (0% variation).

### Mode B: Probabilistic Sampling Generation (5 Runs, Seed = 42):
- **Run 1**: `<START> the cat sat on the mat <END>`
- **Run 2**: `<START> the dog sat on the rug <END>`
- **Run 3**: `<START> the cat ran to the park <END>`
- **Run 4**: `<START> the cat sat on the rug <END>`
- **Run 5**: `<START> the dog ran to the park <END>`

*Sampling Mode Summary*: **5 unique sentences** across 5 runs (100% variation).

---

## Question 10 Answer

### Question:
*Compare the two sets of generated sentences. Which mode produces more variation? Why?*

### Complete Response:
**Mode B (Probabilistic Sampling)** produces significantly more variation.

### Rationale & Theoretical Explanation:

1. **Deterministic Argmax Collapse in Mode A**:
   - Mode A computes $\arg\max_w P(w \mid w_{\text{prev}})$ at every step. Because the probability table $P(w \mid w_{\text{prev}})$ and tie-breaking rules are static and fixed, the greedy algorithm takes the exact same transition choice every time it visits a given state.
   - Starting from `<START>`, it selects `the` ($P=1.0$), then `cat` (highest probability 0.25, broken alphabetically against `dog`), then `sat` (0.67), then `on` (1.0), then `the` (1.0), then `mat` (0.17, alphabetical tie-break against `park`/`rug`), and finally `<END>` (1.0). 
   - This causes greedy generation to collapse into a single deterministic path with zero diversity across runs.

2. **Stochastic Sampling of Full Probability Mass in Mode B**:
   - Mode B draws samples proportionally across all non-zero transitions in $P(w \mid w_{\text{prev}})$. 
   - At context `the`, `cat` (25%), `dog` (25%), `mat` (16.7%), `park` (16.7%), and `rug` (16.7%) all have non-zero chances of selection. 
   - This stochastic behavior explores multiple valid pathways through the state space graph, producing diverse sentence structures.

---

## Evidence Section

### Comparative Summary Table:

| Generation Mode | Selection Function | Diversity Ratio (Unique/5 Runs) | Output Behavior |
| :--- | :--- | :--- | :--- |
| **Mode A (Greedy)** | $\arg\max_w P(w \mid w_{\text{prev}})$ | **1/5 (20%)** | 100% Deterministic, zero variance across runs |
| **Mode B (Sampling)** | $w \sim P(w \mid w_{\text{prev}})$ | **5/5 (100%)** | Stochastic, explores full probability distribution |
