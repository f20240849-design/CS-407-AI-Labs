# Task 5 Prompt Document

This file contains the exact, unedited prompt provided to the LLM engineering assistant to extend the binary XOR code to a 3-class multi-class classification problem.

---

## 💬 Exact Prompt Text

```text
Modify only the output layer and loss function portion of our previous PyTorch XOR code to implement a 3-class sensor disagreement classification model. Do not alter the hidden layer representation size.

Task Specification:
- Class 0: Both sensors inactive -> (0,0)
- Class 1: Sensors disagree       -> (0,1) and (1,0)
- Class 2: Both sensors active   -> (1,1)

Architecture & Loss Requirements:
- Keep 2 input features and 2 hidden units (use Tanh or Sigmoid activation).
- Replace the single output logit with 3 output logits (final layer weight shape 3x2).
- Use PyTorch CrossEntropyLoss for multiclass classification.
- Train full-batch for 3,000 steps using Adam (lr=0.05) with random seed 42.

Reporting & Verification Requirements:
- Print the final loss and predicted class probabilities for all four inputs.
- For input (0,0), print the 3-element softmax probability vector and verify numerically that its sum equals 1.0.
- Verify numerically that the autograd gradient of the loss with respect to the output logits equals (p - y) / N.
- Include a diagnostic test that adds constant +100 to all logits before computing softmax, and explain why stable implementations subtract the maximum logit before exponentiating.
```

---

## 📌 Engineering Constraints Summary

1. 3 discrete classes: 0, 1, 2.
2. 2 hidden units -> 3 output logits.
3. `CrossEntropyLoss` pairing.
4. Softmax probability vector summation check ($\sum p_i = 1$).
5. Analytical logit gradient verification ($\mathbf{p} - \mathbf{y}$).
6. Logit shift diagnostic ($z + 100$) and numerically stable softmax explanation.
