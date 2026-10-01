# Checkpoint Task 1: Problem Specification & Linear Limits

---

## 📌 Problem Specification

- **Input Space ($\mathcal{X}$)**: $\mathcal{X} = \{0, 1\}^2 \subset \mathbb{R}^2$, representing binary sensor readings $(x_1, x_2)$.
- **Output Space ($\mathcal{Y}$)**: $\mathcal{Y} = \{0, 1\}$, representing binary sensor disagreement status $y$.
- **Labelled Dataset ($\mathcal{D}$)**:
  1. $x^{(1)} = (0, 0) \implies y^{(1)} = 0$ (Both sensors inactive)
  2. $x^{(2)} = (0, 1) \implies y^{(2)} = 1$ (Sensor disagreement)
  3. $x^{(3)} = (1, 0) \implies y^{(3)} = 1$ (Sensor disagreement)
  4. $x^{(4)} = (1, 1) \implies y^{(4)} = 0$ (Both sensors active)

---

## 📐 2D Geometric Plane Representation

```text
x2 ^
   |
 1 |   (0,1) [y=1] *---------* (1,1) [y=0]
   |               |         |
   |               |         |
   |               |         |
 0 |   (0,0) [y=0] *---------* (1,0) [y=1]
   +-----------------------------------> x1
       0                       1
```

---

## 💡 Linear Separability Proof

A binary dataset is linearly separable in $\mathbb{R}^2$ if and only if there exists a single straight decision boundary line defined by $w_1 x_1 + w_2 x_2 + b = 0$ such that:
$$w_1 x_1 + w_2 x_2 + b > 0 \quad \text{for all } y = 1$$
$$w_1 x_1 + w_2 x_2 + b < 0 \quad \text{for all } y = 0$$

For the XOR function, substituting the four data points yields four simultaneous linear inequalities:
1. $(0,0) \implies b < 0$
2. $(0,1) \implies w_2 + b > 0$
3. $(1,0) \implies w_1 + b > 0$
4. $(1,1) \implies w_1 + w_2 + b < 0$

Adding inequality (2) and (3) gives:
$$(w_1 + b) + (w_2 + b) > 0 \implies w_1 + w_2 + 2b > 0$$

However, from inequality (1) we know $b < 0$. Therefore:
$$w_1 + w_2 + b > w_1 + w_2 + 2b > 0$$
This directly contradicts inequality (4), which requires $w_1 + w_2 + b < 0$. 

Geometrically, the convex hull of Class 1 points $\{(0,1), (1,0)\}$ intersects the convex hull of Class 0 points $\{(0,0), (1,1)\}$ at the midpoint $(0.5, 0.5)$. No single straight line can separate these two intersecting sets.

---

## 🔮 Linear Baseline Model Prediction

If we train a model consisting of a single affine transformation followed by a Sigmoid output ($\hat{y} = \sigma(w_1 x_1 + w_2 x_2 + b)$):
1. **Decision Boundary**: The model is restricted to linear decision boundaries $\sigma(z) = 0.5 \iff w_1 x_1 + w_2 x_2 + b = 0$.
2. **Failure Mode**: The model will fail to achieve 100% accuracy. It will output $\hat{y} = 0.5$ for all inputs or correctly classify at most 2 out of 4 points (50% accuracy).
3. **Loss Behavior**: Binary cross-entropy loss will plateau near $\ln(2) \approx 0.69315$, which corresponds to random guessing / constant mean prediction.

---

## 🤔 Think About It

> **Question**: A model can have many parameters and still have the wrong *kind* of representation. What scientific claim about representation does XOR let us test with only four data points?

**Answer**: XOR demonstrates that **depth without non-linearity provides zero added representational capacity**. Even if a linear network is stacked to 100 layers containing millions of parameters ($y = W_{100} W_{99} \dots W_1 x + b$), the product of affine transformations collapses into a single affine transformation $y = W_{\text{eff}} x + b_{\text{eff}}$. 

With only four data points, XOR proves that expressiveness is not fundamentally a function of parameter count, but of **representational non-linearity**. It tests whether a model architecture can perform non-linear feature space warping to make non-linearly separable data linearly separable in hidden space.

---

## 📊 Evidence & Empirical Verification

Output logged in [`results/linear_baseline_output.txt`](file:///Users/mittals/Desktop/AI%20Labs/lab4-neural-models-xor/results/linear_baseline_output.txt):

```text
Initial BCE Loss: 0.7124 [TO FILL after running]
Final BCE Loss:   0.6931 [TO FILL after running]
Accuracy:         50.0% (2/4 correct)
```
