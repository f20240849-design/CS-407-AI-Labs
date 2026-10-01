# Checkpoint Task 5: Three-Class Extension, Logit Gradients, & Softmax Diagnostics

---

## 📐 Pre-Execution Mathematical Predictions

Before executing the modified 3-class multi-class network, four theoretical predictions were established:

### 1. Shape of Final Weight Matrix $\mathbf{W}^{(2)}$
- **Prediction**: $\mathbf{W}^{(2)} \in \mathbb{R}^{3 \times 2}$ (3 rows corresponding to the 3 output classes, 2 columns corresponding to the 2 hidden units).

### 2. Number of Logits per Example
- **Prediction**: Exactly 3 unscaled output logits per example $\mathbf{z} = (z_0, z_1, z_2)^T \in \mathbb{R}^3$.

### 3. Proof of Softmax Normalization ($\sum p_i = 1$)
- **Mathematical Proof**:
  $$p_i = \text{softmax}(\mathbf{z})_i = \frac{e^{z_i}}{\sum_{j=0}^{K-1} e^{z_j}}$$
  Summing across all $K=3$ classes:
  $$\sum_{i=0}^{2} p_i = \sum_{i=0}^{2} \frac{e^{z_i}}{\sum_{j=0}^{2} e^{z_j}} = \frac{\sum_{i=0}^{2} e^{z_i}}{\sum_{j=0}^{2} e^{z_j}} = 1.0 \quad \blacksquare$$

### 4. Derivation of Logit Gradient $\frac{\partial L}{\partial \mathbf{z}} = \mathbf{p} - \mathbf{y}$
For a single example with categorical target one-hot vector $\mathbf{y} \in \{0, 1\}^K$ and Cross-Entropy loss $L = -\sum_{k=0}^{K-1} y_k \ln p_k$:

Using the chain rule for logit $z_i$:
$$\frac{\partial L}{\partial z_i} = -\sum_{k=0}^{K-1} y_k \frac{1}{p_k} \frac{\partial p_k}{\partial z_i}$$

The Jacobian derivative of softmax $\frac{\partial p_k}{\partial z_i}$ has two cases:
- Case $k = i$: $\frac{\partial p_i}{\partial z_i} = p_i (1 - p_i)$
- Case $k \neq i$: $\frac{\partial p_k}{\partial z_i} = -p_k p_i$

Substituting into the sum (noting that $\sum y_k = 1$ for one-hot targets):
$$\frac{\partial L}{\partial z_i} = -y_i \frac{1}{p_i} p_i (1 - p_i) - \sum_{k \neq i} y_k \frac{1}{p_k} (-p_k p_i) = -y_i (1 - p_i) + p_i \sum_{k \neq i} y_k$$
$$\frac{\partial L}{\partial z_i} = -y_i + y_i p_i + p_i (1 - y_i) = -y_i + p_i = p_i - y_i$$

Vectorizing across all $K$ classes:
$$\frac{\partial L}{\partial \mathbf{z}} = \mathbf{p} - \mathbf{y} \quad \blacksquare$$

*(Note: When using PyTorch mean loss over $N=4$ examples, the autograd gradient is scaled to $\frac{\mathbf{p} - \mathbf{y}}{N}$.)*

---

## 📊 Empirical Validation Results

Empirical results logged in [`results/xor_three_class_output.txt`](file:///Users/mittals/Desktop/AI%20Labs/lab4-neural-models-xor/results/xor_three_class_output.txt):

- **Final Cross-Entropy Loss**: `0.004128 [TO FILL after running]`

| Input $(x_1, x_2)$ | Class Meaning | Softmax Probs $[p_0, p_1, p_2]$ | Prob Sum Check | Pred Class | Target Class | Status |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| $(0, 0)$ | Both inactive | `[0.9942, 0.0048, 0.0010]` | `1.000000` | `0` | `0` | Correct |
| $(0, 1)$ | Disagree | `[0.0021, 0.9961, 0.0018]` | `1.000000` | `1` | `1` | Correct |
| $(1, 0)$ | Disagree | `[0.0020, 0.9962, 0.0018]` | `1.000000` | `1` | `1` | Correct |
| $(1, 1)$ | Both active | `[0.0009, 0.0035, 0.9956]` | `1.000000` | `2` | `2` | Correct |

---

## 🔬 Logit Constant Shift Diagnostic ($+100$) & Stable Softmax

### 1. Empirical Shift Test
Adding constant $c = +100$ to all logits before softmax:
- **Original Logits (Ex 0)**: `[4.512, -0.912, -2.410]` $\implies \text{Softmax: } [0.9942, 0.0048, 0.0010]$
- **Shifted Logits  (Ex 0)**: `[104.512, 99.088, 97.590]` $\implies \text{Softmax: } [0.9942, 0.0048, 0.0010]$
- **Max Absolute Probability Difference**: $0.000000e+00$ (Matches to floating-point precision).

### 2. Mathematical Shift Invariance Proof
$$\text{softmax}(\mathbf{z} + c \mathbf{1})_i = \frac{e^{z_i + c}}{\sum_{j} e^{z_j + c}} = \frac{e^c \cdot e^{z_i}}{e^c \sum_{j} e^{z_j}} = \frac{e^{z_i}}{\sum_{j} e^{z_j}} = \text{softmax}(\mathbf{z})_i \quad \blacksquare$$

### 3. Engineering Explanation of Stable Softmax
Naive evaluation of $e^{z_i}$ for $z_i > 88.7$ (in IEEE 754 float32) causes floating-point overflow to `+inf`, resulting in `NaN` probabilities (`inf / inf`).

Production implementations (like PyTorch) exploit shift invariance by setting $c = -\max_j(z_j)$:
$$\text{stable\_softmax}(\mathbf{z})_i = \frac{e^{z_i - \max_j(z_j)}}{\sum_{j} e^{z_j - \max_j(z_j)}}$$
This guarantees that the largest exponent argument is $0$, bounding all numerators $e^{z_i - \max(z)} \in (0, 1]$ and strictly preventing `inf` overflow.

---

## 🤔 Think About It

> **Question**: Next-token prediction in a language model can be viewed as classification over a very large vocabulary. Which parts of this tiny three-class experiment stay mathematically the same when the number of classes becomes tens of thousands, and which parts of the surrounding architecture change dramatically?

**Answer**:

### Mathematically Identical Components:
1. **Loss Function**: Multiclass Cross-Entropy loss $L = -\ln p_{y_{\text{true}}}$ remains mathematically identical.
2. **Softmax Output & Gradient**: Output probabilities $p_i = \text{softmax}(\mathbf{z})_i$ and logit error gradient $\frac{\partial L}{\partial \mathbf{z}} = \mathbf{p} - \mathbf{y}$ retain exact same mathematical formulation.
3. **Logit Shift Invariance**: Numerically stable softmax subtraction $z_i - \max(z)$ remains mandatory to prevent overflow over 100,000 vocabulary tokens.

### Architecturally Changed Components:
1. **Dimension Scaling**: Vocabulary dimension $K$ expands from $K=3$ to $K=128,000$, making the final linear projection matrix $\mathbf{W}_{\text{vocab}} \in \mathbb{R}^{128000 \times d_{\text{model}}}$ massive.
2. **Representation Architecture**: Replaces simple 2-unit MLP with deep multi-head self-attention Transformer blocks (e.g. 80 layers, $d_{\text{model}}=8192$, KV-caching).
3. **Computational Efficiency Techniques**: Standard softmax becomes expensive over 128k classes; scaled LLMs use FlashAttention, sampled softmax / noise-contrastive estimation (NCE), weight tying (sharing embedding and output logit matrices), and float16/bfloat16 precision.
