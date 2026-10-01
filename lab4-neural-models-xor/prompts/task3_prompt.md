# Task 3 Prompt Document

This file contains the exact, unedited prompt provided to the LLM engineering assistant to generate the initial PyTorch binary XOR implementation.

---

## 💬 Exact Prompt Text

```text
Generate minimal, readable PyTorch code for the following XOR classification task. Do not change the architecture or task specified below.

Dataset (explicitly specified):
- Input x1=0, x2=0 -> Target y=0
- Input x1=0, x2=1 -> Target y=1
- Input x1=1, x2=0 -> Target y=1
- Input x1=1, x2=1 -> Target y=0

Architecture & Training Requirements:
- 2–2–1 Neural Network (2 input features, 2 hidden units, 1 output).
- Hidden activation: Sigmoid.
- Output: Return raw unscaled logits (do not apply sigmoid inside forward pass).
- Loss function: Use PyTorch BCEWithLogitsLoss for numerical stability.
- Initialisation: Random weight initialisation with seed 42 set for reproducibility.
- Training: Full-batch gradient descent (or Adam) for 3,000 lightweight CPU steps.

Reporting Requirements:
- Print the initial loss before training and the final loss after training.
- Print all four predicted probabilities (after applying torch.sigmoid to logits).
- Print thresholded binary prediction labels (0 or 1 using threshold 0.5).
- Expose and print at least one parameter-gradient tensor (specifically the first-layer weight gradient parameter.grad) after backward().
- Explain each test/check in one concise sentence.
```

---

## 📌 Engineering Constraints Summary

1. Explicit 4 XOR training pairs.
2. 2–2–1 topology.
3. Sigmoid hidden activation.
4. Logits output + `BCEWithLogitsLoss`.
5. Seed set to `42`.
6. Full-batch CPU training.
7. Print initial/final loss, probabilities, thresholded labels, and `fc1.weight.grad`.
