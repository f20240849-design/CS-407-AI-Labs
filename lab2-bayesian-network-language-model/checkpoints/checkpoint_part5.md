# Checkpoint Part V: Ask an LLM to Implement the Model

## Overview & Task Summary
Part V explores prompt engineering for LLM-assisted system construction. The key pedagogical objective is understanding that asking an LLM a vague request (e.g. *"Write a language model in Python"*) leads to unpredictable, unvalidated code. Providing an explicit behavioral specification ensures the generated implementation accurately matches the mathematical model.

---

## Verbatim Lab Prompt (Part V)

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

## Analysis & Behavioral Specification Benefits

1. **Decoupling System Specification from LLM Generation**:
   Specifying requirements upfront forces the developer to define variables, context bounds, edge case policies, and sampling mechanisms before invoking code generation.

2. **Elimination of Library Dependencies**:
   Constraints such as *"Do not use a machine-learning library... Use ordinary Python data structures"* prevent the LLM from inserting heavy frameworks (e.g., PyTorch, Transformers) when a simple frequency-table data structure is intended.

3. **Verifiable System Contract**:
   A step-by-step specification creates unit-testable checkpoints (e.g. checking transition counts, verifying probability normalisation, confirming stopping conditions).

---

## Evidence Section

Refer to the full specification prompt comparison file in [prompts/part_v_prompt.md](file:///Users/mittals/Desktop/AI%20Labs/lab2-bayesian-network-language-model/prompts/part_v_prompt.md).
