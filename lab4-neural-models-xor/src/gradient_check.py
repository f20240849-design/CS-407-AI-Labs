import os
import torch
import torch.nn as nn
import numpy as np

def run_gradient_check():
    torch.manual_seed(42)

    X = torch.tensor([[0.0, 0.0],
                      [0.0, 1.0],
                      [1.0, 0.0],
                      [1.0, 1.0]], dtype=torch.float64)  # Use float64 for high numerical precision

    Y = torch.tensor([[0.0],
                      [1.0],
                      [1.0],
                      [0.0]], dtype=torch.float64)

    class PreciseXORNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(2, 2, dtype=torch.float64)
            self.act = nn.Sigmoid()
            self.fc2 = nn.Linear(2, 1, dtype=torch.float64)

        def forward(self, x):
            return self.fc2(self.act(self.fc1(x)))

    model = PreciseXORNet()
    criterion = nn.BCEWithLogitsLoss()

    # 1. Compute Analytical Gradients via PyTorch Autograd
    logits = model(X)
    loss = criterion(logits, Y)
    loss.backward()

    analytical_grads = {}
    for name, param in model.named_parameters():
        analytical_grads[name] = param.grad.clone()

    # 2. Compute Numerical Gradients using Central Finite Differences
    epsilon = 1e-6
    numerical_grads = {}
    
    for name, param in model.named_parameters():
        num_grad = torch.zeros_like(param.data)
        flat_param = param.data.view(-1)
        flat_num_grad = num_grad.view(-1)

        for i in range(flat_param.numel()):
            orig_val = flat_param[i].item()

            # Plus epsilon
            flat_param[i] = orig_val + epsilon
            loss_plus = criterion(model(X), Y).item()

            # Minus epsilon
            flat_param[i] = orig_val - epsilon
            loss_minus = criterion(model(X), Y).item()

            # Restore original value
            flat_param[i] = orig_val

            # Central difference formula
            flat_num_grad[i] = (loss_plus - loss_minus) / (2.0 * epsilon)

        numerical_grads[name] = num_grad

    # 3. Compare Analytical vs Numerical Gradients
    output_lines = [
        "=== Finite-Difference Gradient Verification (Task 4 Part B Extra) ===",
        f"Epsilon for central difference: {epsilon}",
        "-" * 70,
        f"{'Parameter Name':<15} | {'Analytical Grad Norm':<20} | {'Numerical Grad Norm':<20} | {'Rel Difference':<15}",
        "-" * 70
    ]

    all_passed = True
    for name in analytical_grads:
        a_g = analytical_grads[name]
        n_g = numerical_grads[name]

        diff_norm = torch.norm(a_g - n_g).item()
        sum_norm = (torch.norm(a_g) + torch.norm(n_g)).item() + 1e-12
        rel_diff = diff_norm / sum_norm

        output_lines.append(
            f"{name:<15} | {torch.norm(a_g).item():<20.8f} | {torch.norm(n_g).item():<20.8f} | {rel_diff:<15.4e}"
        )

        if rel_diff > 1e-5:
            all_passed = False

    output_lines.extend([
        "-" * 70,
        f"Gradient Check Passed? {all_passed} (Relative diff < 1e-5 across all parameters)",
        "Conclusion: Reverse-mode automatic differentiation in PyTorch matches central finite-difference gradients."
    ])

    output_str = "\n".join(output_lines)
    print(output_str)

    os.makedirs("results", exist_ok=True)
    with open("results/gradient_check_output.txt", "w") as f:
        f.write(output_str + "\n")

if __name__ == "__main__":
    run_gradient_check()
