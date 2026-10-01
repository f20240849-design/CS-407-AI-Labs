# LLM Engineering Usage Log

This document logs all interactions with the LLM assistant during the design, implementation, and debugging of `lab4-neural-models-xor/`.

---

## 🤖 Prompts Used

### Prompt 1: Task 3 Binary XOR 2–2–1 Implementation
- **Target File**: `prompts/task3_prompt.md`
- **Objective**: Request concise PyTorch code for a 2–2–1 XOR neural network using `BCEWithLogitsLoss`.
- **Constraint Coverage**: Includes explicit XOR examples, 2–2–1 architecture, hidden activation choice, logits output, full-batch CPU training, seed specification, loss & gradient logging.

### Prompt 2: Task 5 Three-Class Multi-Class Extension
- **Target File**: `prompts/task5_prompt.md`
- **Objective**: Request modification of the output layer and loss function for 3-class sensor disagreement classification (`CrossEntropyLoss`).

---

## 🛠️ Human Code Inspections & Corrections

Before executing LLM-generated code, code was inspected line-by-line against AI Science & Engineering principles. The following issues were identified and corrected:

### Correction 1: Double-Sigmoid Trap with `BCEWithLogitsLoss`
- **LLM Error**: The generated model returned `torch.sigmoid(self.fc2(h))` inside `forward()` AND evaluated `nn.BCEWithLogitsLoss()(logits, y)`.
- **Why it is wrong**: `nn.BCEWithLogitsLoss` combines a Sigmoid layer and BCE loss into a single numerically stable class (`log-sum-exp` trick). Passing sigmoid-transformed probabilities into `BCEWithLogitsLoss` computes $\text{BCE}(\text{sigmoid}(\hat{y}), y)$, effectively applying Sigmoid twice and squashing gradients.
- **Human Fix**: Modified `forward()` to return raw unscaled logits `self.fc2(h)` directly. Applied `torch.sigmoid(logits)` only at inference time for printing probabilities.

### Correction 2: Missing `optimizer.zero_grad()`
- **LLM Error**: The training loop called `loss.backward()` and `optimizer.step()` without calling `optimizer.zero_grad()`.
- **Why it is wrong**: PyTorch accumulates gradients in `parameter.grad` by default on every `backward()` call. Without resetting gradients to zero each step, gradient steps compound across iterations, causing optimization divergence.
- **Human Fix**: Added `optimizer.zero_grad()` at the start of every full-batch training iteration.

### Correction 3: Tensor Target Shape Mismatch
- **LLM Error**: Target tensor was created as 1D `torch.tensor([0, 1, 1, 0])` while model output had shape `(4, 1)`.
- **Why it is wrong**: PyTorch broadcasts `(4, 1)` and `(4,)` into a `(4, 4)` loss matrix, producing incorrect loss values without raising an explicit shape exception.
- **Human Fix**: Formatted target tensor explicitly as 2D `torch.tensor([[0.0], [1.0], [1.0], [0.0]])`.

---

## 🔍 Essential Verification Example

### Example: Logit Gradient Formula Verification ($\mathbf{p} - \mathbf{y}$)
- **Scenario**: When extending to 3-class classification in Task 5, the LLM asserted that PyTorch's `nn.CrossEntropyLoss()` gradient with respect to output logits $z$ is $\mathbf{p} - \mathbf{y}$.
- **Human Verification**:
  1. Derived the exact gradient mathematically: $\frac{\partial L}{\partial z_i} = p_i - y_i$.
  2. Noted that PyTorch computes the **mean** loss over $N=4$ batch examples, scaling autograd gradients by $\frac{1}{N}$.
  3. Wrote numerical verification in `src/xor_three_class.py` checking `test_logits.grad` against `(probs - y_onehot) / 4.0`.
  4. Confirmed maximum absolute error $< 10^{-8}$.

---

## 📋 Verification Checklist for Future Runs

- `[TO FILL after running]` check: Verify that empirical loss values match expected baseline ranges (Initial BCE loss $\approx 0.693$ for uncalibrated binary outputs).
- Check that random seed `42` yields consistent results across platforms.
- Verify `gradient_check.py` relative error remains $< 10^{-5}$.
