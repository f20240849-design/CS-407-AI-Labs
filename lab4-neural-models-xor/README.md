# Lab 4: Neural Models – Learning, Depth, Activations, and Output Layers

An undergraduate AI laboratory project exploring neural representations, non-linear hidden layers, activation function dynamics, output layer design, automatic differentiation (autograd), and LLM-assisted code generation for the XOR problem and multi-class extensions.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Software Requirements & Setup](#software-requirements--setup)
- [Execution Guide](#execution-guide)
- [Lab Tasks & Checkpoints](#lab-tasks--checkpoints)
- [Key Findings & Results](#key-findings--results)
- [Submission Checklist](#submission-checklist)

---

## 🎯 Overview

This laboratory investigates why non-linear representations are scientifically necessary for non-linearly separable decision boundaries (such as XOR) and explores engineering choices in neural network design:
1. **Linear Baseline**: Demonstrates why a single affine transformation fails on XOR.
2. **2–2–1 Multi-Layer Perceptron**: Solves binary XOR using logits and `BCEWithLogitsLoss()`.
3. **Symmetry Breaking Failure**: Demonstrates how zero-weight initialization freezes hidden unit learning.
4. **Activation Functions**: Compares Sigmoid, Tanh, and ReLU across loss convergence, classification accuracy, and gradient norms.
5. **Finite-Difference Gradient Checking**: Validates PyTorch autograd gradients against numerical central differences.
6. **Three-Class Multi-Class Extension**: Extends XOR to 3 classes using `CrossEntropyLoss`, verifying softmax probability summation, logit gradient $\mathbf{p} - \mathbf{y}$, and logit shift invariance ($z + 100$).

---

## 📁 Repository Structure

```
lab4-neural-models-xor/
├── README.md
├── requirements.txt
├── SUBMISSION_CHECKLIST.md
├── llm_usage_log.md
├── src/
│   ├── linear_baseline.py        # Task 1: Single affine baseline
│   ├── xor_binary.py             # Task 3 & 4A/B: 2-2-1 PyTorch network
│   ├── symmetry_experiment.py    # Task 4C: Zero initialization symmetry test
│   ├── activation_experiment.py  # Task 4D: Sigmoid vs Tanh vs ReLU comparison
│   ├── gradient_check.py         # Task 4B: Finite-difference gradient check
│   └── xor_three_class.py        # Task 5: 3-class extension & logit gradient check
├── prompts/
│   ├── task3_prompt.md           # LLM prompt for Task 3 code generation
│   └── task5_prompt.md           # LLM prompt for Task 5 code generation
├── checkpoints/
│   ├── checkpoint_task1.md       # Task 1: Problem spec & linear separability
│   ├── checkpoint_task2.md       # Task 2: Model design & validation criteria
│   ├── checkpoint_task3.md       # Task 3: LLM prompt, code, & autograd stages
│   ├── checkpoint_task4.md       # Task 4: Empirical results, symmetry, & activations
│   ├── checkpoint_task5.md       # Task 5: 3-class extension, p - y proof, & shift test
│   └── checkpoint_reflection.md  # 7 Reflection questions answered
└── results/
    ├── linear_baseline_output.txt
    ├── xor_binary_output.txt
    ├── symmetry_experiment_output.txt
    ├── activation_table.md
    ├── gradient_check_output.txt
    └── xor_three_class_output.txt
```

---

## 💻 Software Requirements & Setup

- **Python**: 3.9+
- **PyTorch**: 2.0+ (CPU only required)
- **NumPy**: 1.24+

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/lab4-neural-models-xor.git
cd lab4-neural-models-xor

# Create and activate a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Execution Guide

Run the scripts in order to generate results and empirical logs:

```bash
# 1. Run Linear Baseline (Task 1)
python src/linear_baseline.py

# 2. Run Binary 2-2-1 XOR Model (Task 3 & 4A)
python src/xor_binary.py

# 3. Run Symmetry Experiment (Task 4C)
python src/symmetry_experiment.py

# 4. Run Activation Function Comparison (Task 4D)
python src/activation_experiment.py

# 5. Run Finite-Difference Gradient Check (Task 4B)
python src/gradient_check.py

# 6. Run Three-Class Extension (Task 5)
python src/xor_three_class.py
```

All empirical logs and tables will automatically save into the `results/` folder.

---

## 📝 Checkpoint Mapping

| Checkpoint File | Contents & Focus |
|:---|:---|
| [checkpoint_task1.md](file:///Users/mittals/Desktop/AI%20Labs/lab4-neural-models-xor/checkpoints/checkpoint_task1.md) | Problem specification ($\mathcal{X}, \mathcal{Y}$), 2D geometry, linear separability proof, linear prediction. |
| [checkpoint_task2.md](file:///Users/mittals/Desktop/AI%20Labs/lab4-neural-models-xor/checkpoints/checkpoint_task2.md) | 2–2–1 model architecture, 3 design questions, 4 validation criteria, hidden-unit representation learning. |
| [checkpoint_task3.md](file:///Users/mittals/Desktop/AI%20Labs/lab4-neural-models-xor/checkpoints/checkpoint_task3.md) | LLM engineering prompt, generated code, human pre-execution fixes, autograd stage identification. |
| [checkpoint_task4.md](file:///Users/mittals/Desktop/AI%20Labs/lab4-neural-models-xor/checkpoints/checkpoint_task4.md) | Learning verification, $\frac{\partial L}{\partial W^{(1)}}$ interpretation, symmetry breaking analysis, activation table. |
| [checkpoint_task5.md](file:///Users/mittals/Desktop/AI%20Labs/lab4-neural-models-xor/checkpoints/checkpoint_task5.md) | 3-class extension design, pre-run predictions, empirical results, logit gradient $\mathbf{p}-\mathbf{y}$ proof, stable softmax. |
| [checkpoint_reflection.md](file:///Users/mittals/Desktop/AI%20Labs/lab4-neural-models-xor/checkpoints/checkpoint_reflection.md) | Comprehensive answers to all 7 reflection questions. |

---

## 📜 License & Citation

Developed for undergraduate AI course unit on Neural Models and Deep Learning Representations.
Reference: S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed.
