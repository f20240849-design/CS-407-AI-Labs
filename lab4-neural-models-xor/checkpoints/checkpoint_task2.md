# Checkpoint Task 2: Model Design & Validation Criteria

---

## 🏗️ Model Architecture Specification

The baseline neural model design specified for binary XOR classification is a **2–2–1 Multi-Layer Perceptron (MLP)**:

$$\mathbf{x} \in \mathbb{R}^2 \xrightarrow{\mathbf{W}^{(1)} \in \mathbb{R}^{2 \times 2}, \mathbf{b}^{(1)} \in \mathbb{R}^2} \mathbf{a}^{(1)} \xrightarrow{f^{(1)}} \mathbf{h}^{(1)} \in \mathbb{R}^2 \xrightarrow{\mathbf{W}^{(2)} \in \mathbb{R}^{1 \times 2}, b^{(2)} \in \mathbb{R}} z \xrightarrow{\sigma} \hat{y} \in [0, 1]$$

- **Input Dimension**: 2 ($x_1, x_2$).
- **Hidden Layer**: 2 hidden units with non-linear activation $f^{(1)}$ (Sigmoid or Tanh).
- **Output Layer**: 1 output logit $z$, paired with `BCEWithLogitsLoss()` (internally applying Sigmoid $\sigma(z) = \frac{1}{1 + e^{-z}}$).
- **Optimizer**: Gradient-based optimization (Adam with learning rate $\eta = 0.05$ or SGD with momentum).

---

## ❓ Design Conceptual Questions

### 1. Why is the hidden non-linearity scientifically necessary here?
Without a non-linear activation function $f^{(1)}$, the hidden layer output is purely affine: $\mathbf{h}^{(1)} = \mathbf{W}^{(1)} \mathbf{x} + \mathbf{b}^{(1)}$. 

Substituting $\mathbf{h}^{(1)}$ into the output layer equation yields:
$$z = \mathbf{W}^{(2)} (\mathbf{W}^{(1)} \mathbf{x} + \mathbf{b}^{(1)}) + b^{(2)} = (\mathbf{W}^{(2)} \mathbf{W}^{(1)}) \mathbf{x} + (\mathbf{W}^{(2)} \mathbf{b}^{(1)} + b^{(2)}) = \mathbf{W}_{\text{eff}} \mathbf{x} + b_{\text{eff}}$$

This collapses the 2-layer network into a single linear model, making it mathematically impossible to form a non-linear decision boundary. The non-linear activation $f^{(1)}$ warps the 2D input space $\mathbb{R}^2$ into a 2D hidden feature space $\mathbf{h}^{(1)}$ where the four XOR points become **linearly separable** by the final hyper-plane $\mathbf{W}^{(2)}$.

### 2. Why is sigmoid plus binary cross-entropy a sensible engineering pairing for the output?
1. **Probabilistic Interpretation**: The XOR target is a binary classification task $y \in \{0, 1\}$. The Sigmoid function $\sigma(z) \in (0, 1)$ maps unscaled real-valued logits $z \in \mathbb{R}$ into valid Bernoulli probabilities $P(y=1|\mathbf{x})$.
2. **Gradient Saturation Avoidance**: Combining Sigmoid output with Binary Cross-Entropy (BCE) loss eliminates gradient saturation. For BCE loss $L = -y \ln \hat{y} - (1-y) \ln(1-\hat{y})$ where $\hat{y} = \sigma(z)$, the derivative with respect to the output logit $z$ simplifies cleanly to:
   $$\frac{\partial L}{\partial z} = \hat{y} - y$$
   This error signal $(\hat{y} - y)$ is directly proportional to prediction discrepancy, preventing vanishing gradients when predictions are wrong.
3. **Numerical Stability**: PyTorch's `BCEWithLogitsLoss()` computes $\ln(1 + e^{-z})$ using the `log-sum-exp` trick, preventing numerical underflow/overflow during exponentiation.

### 3. What evidence will count as successful learning?
We define **4 empirical validation criteria**:
1. **Loss Convergence Check**: Final scalar loss drops below $0.05$ (compared to initial uncalibrated loss $\approx 0.693$).
2. **Classification Accuracy Check**: All four thresholded predictions $\mathbb{I}(\hat{y}_i \ge 0.5)$ exactly match true targets $y_i$ ($4/4$ correct, $100\%$ accuracy).
3. **Non-Zero Gradient Check**: Early-step hidden weight gradient tensor norm $\|\nabla_{\mathbf{W}^{(1)}} L\|_2 > 0$, demonstrating active backpropagation flow.
4. **Repeated-Run Stability Check**: Across multiple random seeds, the optimizer consistently finds a valid solution without getting trapped in local minima.

---

## 🤔 Think About It

> **Question**: The hidden units are not given target values. If the network learns XOR, what has determined what each hidden unit should compute? Relate your answer to the role of backpropagation.

**Answer**: The hidden unit representations are determined entirely by **backpropagation via the chain rule**, which propagates output error signals backward through the network parameters:

$$\frac{\partial L}{\partial \mathbf{W}^{(1)}} = \left( \frac{\partial L}{\partial z} \mathbf{W}^{(2)} \odot f'(\mathbf{a}^{(1)}) \right) \mathbf{x}^T$$

Because no intermediate supervision targets exist for $\mathbf{h}^{(1)}$, backpropagation acts as a credit assignment mechanism. It calculates how each individual hidden unit contributed to the final prediction error $\hat{y} - y$. 

The hidden units are driven to split the XOR task into two complementary half-space linear decisions (e.g., $h_1 = \text{step}(x_1 + x_2 - 0.5)$ [OR function] and $h_2 = \text{step}(x_1 + x_2 - 1.5)$ [AND function]). The second layer then computes $h_1 - h_2$ to isolate the XOR region. Backpropagation automatically discovers this internal representation by following the negative gradient of the loss surface.

---

## 📊 Validation Criteria Summary Table

| Criterion | Target Metric / Requirement | Mathematical Condition |
|:---|:---|:---|
| **Loss** | Final BCE Loss | $L_{\text{final}} < 0.05$ |
| **Accuracy** | Correct Labels | $\frac{1}{4}\sum_{i=1}^4 \mathbb{I}(\hat{y}_i = y_i) = 1.0$ |
| **Gradient Flow** | First-Layer Gradient Norm | $\|\nabla_{\mathbf{W}^{(1)}} L\|_2 > 10^{-4}$ |
| **Robustness** | Seed Convergence | Success rate $> 75\%$ over seeds |
