import os
import torch
import torch.nn as nn
import torch.optim as optim

def run_symmetry_experiment():
    torch.manual_seed(42)

    X = torch.tensor([[0.0, 0.0],
                      [0.0, 1.0],
                      [1.0, 0.0],
                      [1.0, 1.0]], dtype=torch.float32)

    Y = torch.tensor([[0.0],
                      [1.0],
                      [1.0],
                      [0.0]], dtype=torch.float32)

    class SymmetryXORNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(2, 2)
            self.act = nn.Sigmoid()
            self.fc2 = nn.Linear(2, 1)
            
            # ALL-ZERO INITIALISATION
            nn.init.zeros_(self.fc1.weight)
            nn.init.zeros_(self.fc1.bias)
            nn.init.zeros_(self.fc2.weight)
            nn.init.zeros_(self.fc2.bias)

        def forward(self, x):
            return self.fc2(self.act(self.fc1(x)))

    model = SymmetryXORNet()
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    steps_to_log = [0, 1, 5, 10, 50, 100, 500, 1000, 2000]
    logs = []

    output_lines = [
        "=== Symmetry Breaking Failure Experiment (Task 4 Part C) ===",
        "Initialisation: All weights and biases set to exactly ZERO.",
        "Tracking Hidden Layer Weight Matrix (W(1)) rows across training steps:",
        "-" * 65
    ]

    for step in range(2001):
        if step in steps_to_log:
            w1 = model.fc1.weight.data.clone()
            row0 = w1[0].numpy()
            row1 = w1[1].numpy()
            are_identical = torch.allclose(w1[0], w1[1])
            with torch.no_grad():
                logits = model(X)
                loss_val = criterion(logits, Y).item()
            
            line = f"Step {step:4d} | Loss: {loss_val:.6f} | Row 0: [{row0[0]:.6f}, {row0[1]:.6f}] | Row 1: [{row1[0]:.6f}, {row1[1]:.6f}] | Identical? {are_identical}"
            output_lines.append(line)

        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, Y)
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        final_probs = torch.sigmoid(model(X))
        thresholded = (final_probs >= 0.5).float()

    output_lines.extend([
        "-" * 65,
        "Final Predictions under Zero Initialization:",
        f"  (0,0) -> Prob: {final_probs[0].item():.4f} | Pred: {int(thresholded[0].item())}",
        f"  (0,1) -> Prob: {final_probs[1].item():.4f} | Pred: {int(thresholded[1].item())}",
        f"  (1,0) -> Prob: {final_probs[2].item():.4f} | Pred: {int(thresholded[2].item())}",
        f"  (1,1) -> Prob: {final_probs[3].item():.4f} | Pred: {int(thresholded[3].item())}",
        "-" * 65,
        "Symmetry Analysis Conclusion:",
        "Because both hidden units start with identical zero weights and biases,",
        "they compute the exact same activation for every input. Consequently, backpropagation",
        "delivers identical gradients to both hidden units at every step. They update symmetrically",
        "and behave as a single scalar unit, rendering hidden depth useless for feature learning."
    ])

    output_str = "\n".join(output_lines)
    print(output_str)

    os.makedirs("results", exist_ok=True)
    with open("results/symmetry_experiment_output.txt", "w") as f:
        f.write(output_str + "\n")

if __name__ == "__main__":
    run_symmetry_experiment()
