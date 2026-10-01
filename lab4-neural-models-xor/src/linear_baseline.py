import os
import torch
import torch.nn as nn
import torch.optim as optim

def run_linear_baseline():
    # Set seed for reproducibility
    torch.manual_seed(42)

    # 1. Dataset: XOR problem
    # Inputs (4x2), Targets (4x1)
    X = torch.tensor([[0.0, 0.0],
                      [0.0, 1.0],
                      [1.0, 0.0],
                      [1.0, 1.0]], dtype=torch.float32)
    
    Y = torch.tensor([[0.0],
                      [1.0],
                      [1.0],
                      [0.0]], dtype=torch.float32)

    # 2. Linear Baseline Model: Single Affine Layer + Sigmoid Output
    class LinearModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(2, 1)
            self.sigmoid = nn.Sigmoid()

        def forward(self, x):
            # Affine transformation: a = W*x + b
            a = self.linear(x)
            # Sigmoid activation: y_hat = 1 / (1 + exp(-a))
            return self.sigmoid(a)

    model = LinearModel()
    criterion = nn.BCELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    # Record initial state
    with torch.no_grad():
        initial_probs = model(X)
        initial_loss = criterion(initial_probs, Y).item()

    # Full-batch training loop
    num_steps = 5000
    for step in range(num_steps):
        optimizer.zero_grad()
        probs = model(X)
        loss = criterion(probs, Y)
        loss.backward()
        optimizer.step()

    # Final evaluation
    with torch.no_grad():
        final_probs = model(X)
        final_loss = criterion(final_probs, Y).item()
        thresholded_preds = (final_probs >= 0.5).float()
        accuracy = (thresholded_preds == Y).float().mean().item() * 100

    output_lines = [
        "=== Linear Baseline Experiment (Task 1 Prediction Check) ===",
        f"Model Architecture: 2 inputs -> 1 linear output + Sigmoid",
        f"Training Steps: {num_steps}, Learning Rate: 0.1, Optimizer: SGD",
        "-" * 50,
        f"Initial BCE Loss: {initial_loss:.4f}",
        f"Final BCE Loss:   {final_loss:.4f}",
        "-" * 50,
        "Final Predictions on XOR Dataset:",
        f"Input (0,0) -> Prob: {final_probs[0].item():.4f} | Pred: {int(thresholded_preds[0].item())} | Target: 0",
        f"Input (0,1) -> Prob: {final_probs[1].item():.4f} | Pred: {int(thresholded_preds[1].item())} | Target: 1",
        f"Input (1,0) -> Prob: {final_probs[2].item():.4f} | Pred: {int(thresholded_preds[2].item())} | Target: 1",
        f"Input (1,1) -> Prob: {final_probs[3].item():.4f} | Pred: {int(thresholded_preds[3].item())} | Target: 0",
        "-" * 50,
        f"Classification Accuracy: {accuracy:.1f}% (Correct: {int(accuracy/25)}/4)",
        "Conclusion: Single affine layer fails to separate XOR (loss remains high ~0.693, accuracy ~50%)."
    ]

    output_str = "\n".join(output_lines)
    print(output_str)

    os.makedirs("results", exist_ok=True)
    with open("results/linear_baseline_output.txt", "w") as f:
        f.write(output_str + "\n")

if __name__ == "__main__":
    run_linear_baseline()
