# AI Laboratory: Bayesian Networks and Autoregressive Language Models

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License-MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository contains the complete, final submission for the AI Laboratory exercise **"Bayesian Networks and Autoregressive Language Models"**. It explores how probability theory, the chain rule of probability, and Bayesian networks form the foundation of modern autoregressive language models.

---

## 📖 Overview

Modern Large Language Models (LLMs) generate text autoregressively by estimating conditional probability distributions over vocabulary tokens given preceding context:

$$P(X_1, X_2, \dots, X_T) = \prod_{t=1}^{T} P(X_t \mid X_1, X_2, \dots, X_{t-1})$$

In this laboratory, we build first-order ($P(X_t \mid X_{t-1})$) and second-order ($P(X_t \mid X_{t-2}, X_{t-1})$) Markov language models from scratch using pure Python data structures. We construct exact Conditional Probability Tables (CPTs) from training data, evaluate greedy vs. sampling generation modes, write automated probability normalisation tests, compare parameter space trade-offs, and examine the relationship between small Bayesian networks and modern neural LLMs.

---

## 🎯 Learning Objectives

1. Explain the relationship between the chain rule of probability and autoregressive modelling.
2. Represent a simple autoregressive language model as a Bayesian network.
3. Construct conditional probability tables from text corpus data.
4. Use a probabilistic model to predict the next word.
5. Generate text by repeatedly sampling from conditional distributions.
6. Use an LLM to assist with the implementation of a probabilistic model using explicit specifications.
7. Test whether an LLM-generated implementation satisfies probabilistic invariants ($\sum_v P(v \mid w) = 1.0$).
8. Explain why the probabilistic structure of an autoregressive model remains central when using neural networks.

---

## 📂 Repository Structure

```text
lab2-bayesian-network-language-model/
├── README.md                          # Main project overview and run guide
├── src/                               # Python source code implementations
│   ├── __init__.py                    # Package initializer
│   ├── bigram_model.py                # First-Order Markov Model P(X_t | X_{t-1})
│   ├── trigram_model.py               # Second-Order Markov Model P(X_t | X_{t-2}, X_{t-1})
│   ├── generation_modes.py            # Mode A (Greedy Argmax) vs Mode B (Sampling)
│   └── compare_models.py              # Quantitative & qualitative model comparison
├── tests/                             # Automated test suite
│   └── test_normalisation.py          # Property test: sum_v P(v | context) == 1.0
├── results/                           # Generated results and execution runners
│   ├── run_all.py                     # Master execution runner script
│   ├── cpts.txt                       # Exact Conditional Probability Tables (CPTs)
│   ├── generated_sentences.txt        # 20+ generated sentences across models/modes
│   ├── normalisation.txt              # Probability normalisation test output
│   └── comparison.md                  # Detailed analytical report comparing models
├── prompts/                           # LLM Specification Prompt Files
│   ├── part_v_prompt.md               # First-Order Specification Prompt (verbatim & improved)
│   └── part_xii_prompt.md              # Second-Order Specification Prompt (verbatim & improved)
└── checkpoints/                       # Mandatory Submission Checkpoints (Parts I–XV)
    ├── checkpoint_part1.md            # Part I: Chain Rule & Question 1
    ├── checkpoint_part2.md            # Part II: Bayesian Network DAG & Question 2
    ├── checkpoint_part3.md            # Part III: Dataset Pre-processing & Tokenisation
    ├── checkpoint_part4.md            # Part IV: Hand-Calculated CPTs & Question 3
    ├── checkpoint_part5.md            # Part V: LLM Specification Prompt Engineering
    ├── checkpoint_part6.md            # Part VI: Code Inspection & Questions 4–7
    ├── checkpoint_part7.md            # Part VII: Normalisation Testing & Question 8
    ├── checkpoint_part8.md            # Part VIII: Next-Word Prediction & Question 9
    ├── checkpoint_part9.md            # Part IX: Text Generation & 20+ Samples
    ├── checkpoint_part10.md           # Part X: Greedy vs Sampling & Question 10
    ├── checkpoint_part11.md           # Part XI: Second-Order BN & Question 11
    ├── checkpoint_part12.md           # Part XII: LLM Second-Order Prompt
    ├── checkpoint_part13.md           # Part XIII: Model Comparison & Question 12
    ├── checkpoint_part14.md           # Part XIV: Connection to Modern LLMs
    └── checkpoint_part15.md           # Part XV: Reflection, Questions 13–14 & Deliverables
```

---

## 🗂️ Table of Contents & File Index

### 🐍 Python Source Code
- [src/bigram_model.py](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/src/bigram_model.py): Implements `BigramLanguageModel` with counts $C(w_i, w_j)$, CPT calculation, greedy argmax with alphabetical tie-breaking, seeded sampling, and unseen word fallback policy.
- [src/trigram_model.py](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/src/trigram_model.py): Implements `TrigramLanguageModel` with triple counts $C(w_{t-2}, w_{t-1}, w_t)$, initial context `('<START>', '<START>')`, sampling generation, and unseen context handling.
- [src/generation_modes.py](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/src/generation_modes.py): Demonstrates Mode A (Greedy Argmax) vs Mode B (Probabilistic Sampling).
- [src/compare_models.py](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/src/compare_models.py): Calculates non-zero parameters, zero-probability contexts, diversity ratios, and qualitative coherence.

### 🧪 Tests & Results
- [tests/test_normalisation.py](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/tests/test_normalisation.py): Verifies $\sum_v P(v \mid w) = 1.0$ for all context keys.
- [results/run_all.py](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/results/run_all.py): Master runner executing all experiments and outputting results.
- [results/cpts.txt](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/results/cpts.txt): Full exact CPT probability distributions.
- [results/generated_sentences.txt](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/results/generated_sentences.txt): 20+ generated text samples.
- [results/normalisation.txt](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/results/normalisation.txt): Probability normalisation test log.
- [results/comparison.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/results/comparison.md): Comprehensive Markdown comparison report.

### 📝 LLM Prompt Engineering
- [prompts/part_v_prompt.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/prompts/part_v_prompt.md): Verbatim and improved prompt for first-order model.
- [prompts/part_xii_prompt.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/prompts/part_xii_prompt.md): Verbatim and improved prompt for second-order model.

### 📋 Submission Checkpoints (Questions 1–14 & Deliverables 1–7)
- [checkpoints/checkpoint_part1.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part1.md): **Question 1** (Chain-rule factorisation).
- [checkpoints/checkpoint_part2.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part2.md): **Question 2** (First-order Markov independence assumption).
- [checkpoints/checkpoint_part3.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part3.md): Part III Dataset preparation & tokenisation.
- [checkpoints/checkpoint_part4.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part4.md): **Question 3** (Hand-calculated CPTs & zero-probability transitions).
- [checkpoints/checkpoint_part5.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part5.md): Part V Specification prompt engineering.
- [checkpoints/checkpoint_part6.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part6.md): **Questions 4, 5, 6, 7** (Code inspection).
- [checkpoints/checkpoint_part7.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part7.md): **Question 8** (Normalisation testing & non-1.0 sum diagnosis).
- [checkpoints/checkpoint_part8.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part8.md): **Question 9** (Next-word prediction & human expectations).
- [checkpoints/checkpoint_part9.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part9.md): Part IX Text generation (20 sampled sentences).
- [checkpoints/checkpoint_part10.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part10.md): **Question 10** (Mode A Greedy vs Mode B Sampling).
- [checkpoints/checkpoint_part11.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part11.md): **Question 11** (Second-order Bayesian network analysis).
- [checkpoints/checkpoint_part12.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part12.md): Part XII Second-order LLM specification.
- [checkpoints/checkpoint_part13.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part13.md): **Question 12** (Context trade-offs & curse of dimensionality).
- [checkpoints/checkpoint_part14.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part14.md): Part XIV Connection to modern neural LLMs & table.
- [checkpoints/checkpoint_part15.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/checkpoints/checkpoint_part15.md): **Questions 13 & 14**, Deliverables 1–7 checklist, and LLM code inspection reflection.

---

## ⚡ Execution Instructions (Python 3 Only)

No external libraries are required. All scripts run using Python 3 standard library modules (`collections`, `random`, `math`, `pathlib`, `sys`).

### 1. Run Master Execution Script (Generates All Outputs)
```bash
python3 results/run_all.py
```

### 2. Run Probability Normalisation Test Suite
```bash
python3 tests/test_normalisation.py
```

### 3. Run Individual Model Demonstrations
```bash
# First-Order Bigram Model
python3 src/bigram_model.py

# Second-Order Trigram Model
python3 src/trigram_model.py

# Generation Modes Comparison (Greedy vs Sampling)
python3 src/generation_modes.py

# Comparative Model Analysis
python3 src/compare_models.py
```

---

## 📊 Summary of Main Results

- **Probability Normalisation**: 100% of context distributions across both Bigram (11 contexts) and Trigram (15 contexts) models sum to exactly `1.000000` (Passed).
- **First-Order Bigram Parameters**: 14 non-zero conditional probabilities; 1 zero-probability context (8.3% sparsity).
- **Second-Order Trigram Parameters**: 19 non-zero conditional probabilities; 129 zero-probability contexts (89.6% sparsity due to exponential context space growth $12^2 = 144$).
- **Generation Diversity**: Mode A (Greedy) produces 1 unique sentence (0% variation due to deterministic argmax collapse). Mode B (Sampling) produces 100% unique valid sentences across sampled runs.
