import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

def stable_softmax(logits):
    # Numerically stable softmax: subtract max logit before exponentiation
    # softmax(z_i) = exp(z_i - max(z)) / sum_j exp(z_j - max(z))
    max_logits = torch.max(logits, dim=-1, keepdim=True).values
    exps = torch.exp(logits - max_logits)
    return exps / torch.sum(exps, dim=-1, keepdim=True)

def run_xor_three_class():
    torch.manual_seed(42)

    # 1. Dataset: 3-Class Sensor Disagreement Problem
    # Class 0: (0,0) [both inactive]
    # Class 1: (0,1) and (1,0) [disagree]
    # Class 2: (1,1) [both active]
    X = torch.tensor([[0.0, 0.0],
                      [0.0, 1.0],
                      [1.0, 0.0],
                      [1.0, 1.0]], dtype=torch.float32)

    Y_class = torch.tensor([0, 1, 1, 2], dtype=torch.long)
    Y_onehot = F.one_hot(Y_class, num_classes=3).float()

    # 2. Model: 2 inputs -> 2 hidden units (Tanh) -> 3 output logits
    class ThreeClassNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(2, 2)
            self.act = nn.Tanh()
            self.fc2 = nn.Linear(2, 3)  # Final weight shape: (3, 2)

        def forward(self, x):
            return self.fc2(self.act(self.fc1(x)))

    model = ThreeClassNet()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.05)

    # Full-batch training loop
    num_steps = 3000
    for step in range(num_steps):
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, Y_class)
        loss.backward()
        optimizer.step()

    output_lines = [
        "=== Task 5: Three-Class Classification Extension ===",
        "Classes: 0 -> (0,0), 1 -> (0,1)/(1,0), 2 -> (1,1)",
        "Architecture: 2 inputs -> 2 hidden units (Tanh) -> 3 logits",
        f"Final Loss: {loss.item():.6f}",
        "-" * 65
    ]

    # Evaluation and verification
    with torch.no_grad():
        final_logits = model(X)
        probs = stable_softmax(final_logits)
        prob_sums = probs.sum(dim=-1)
        preds = torch.argmax(probs, dim=-1)

    output_lines.append("Predicted Class Probabilities & Softmax Sum Check:")
    for i in range(4):
        x_pair = tuple(X[i].numpy())
        p_vec = probs[i].numpy()
        p_sum = prob_sums[i].item()
        pred_cls = preds[i].item()
        tgt_cls = Y_class[i].item()
        line = f"  Input {x_pair} -> Probs: [{p_vec[0]:.4f}, {p_vec[1]:.4f}, {p_vec[2]:.4f}] | Sum: {p_sum:.6f} | Pred: {pred_cls} | Target: {tgt_cls}"
        output_lines.append(line)

    output_lines.extend([
        "-" * 65,
        "=== Logit Gradient Verification: dL / dz = (p - y) / N ==="
    ])

    # Compute analytical logit gradient using autograd hooks
    model.eval()
    test_logits = model(X).detach().requires_grad_(True)
    test_loss = criterion(test_logits, Y_class)
    test_loss.backward()
    
    autograd_logit_grad = test_logits.grad  # PyTorch mean loss scales by 1/N
    with torch.no_grad():
        test_probs = F.softmax(test_logits, dim=-1)
        # Mathematical derivation formula: (p - y) / N where N=4
        formula_logit_grad = (test_probs - Y_onehot) / 4.0

    max_grad_diff = torch.max(torch.abs(autograd_logit_grad - formula_logit_grad)).item()
    output_lines.extend([
        f"Autograd Logit Grad (Example 0): {autograd_logit_grad[0].numpy()}",
        f"Formula Grad (p - y)/N (Ex 0):   {formula_logit_grad[0].numpy()}",
        f"Max Absolute Difference across all elements: {max_grad_diff:.8e}",
        f"Verification Result: MATCHES EXACTLY? {max_grad_diff < 1e-6}",
        "-" * 65,
        "=== Optional Diagnostic: Logit Constant Shift (+100) Test ==="
    ])

    with torch.no_grad():
        shifted_logits = final_logits + 100.0
        # Standard softmax naive calculation would overflow: exp(z + 100) -> inf
        # Stable softmax subtracts max logit: (z + 100) - max(z + 100) = z - max(z)
        shifted_probs = stable_softmax(shifted_logits)
        shift_diff = torch.max(torch.abs(probs - shifted_probs)).item()

    output_lines.extend([
        f"Original Logits (Ex 0): {final_logits[0].numpy()}",
        f"Shifted Logits  (Ex 0): {shifted_logits[0].numpy()}",
        f"Original Softmax Probs (Ex 0): {probs[0].numpy()}",
        f"Shifted Softmax Probs  (Ex 0): {shifted_probs[0].numpy()}",
        f"Max Absolute Probability Difference: {shift_diff:.8e}",
        "Explanation: Softmax is shift-invariant because exp(z_i + c) / sum exp(z_j + c) = exp(c)exp(z_i) / [exp(c) sum exp(z_j)] = exp(z_i) / sum exp(z_j).",
        "Subtracting max(z) prevents floating-point overflow (e.g., overflow to inf) without altering the exact mathematical probabilities."
    ])

    output_str = "\n".join(output_lines)
    print(output_str)

    os.makedirs("results", exist_ok=True)
    with open("results/xor_three_class_output.txt", "w") as f:
        f.write(output_str + "\n")

if __name__ == "__main__":
    run_xor_three_class()
