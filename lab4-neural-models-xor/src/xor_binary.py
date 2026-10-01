import os
import torch
import torch.nn as nn
import torch.optim as optim

def run_xor_binary():
    # Set seed for exact reproducibility
    torch.manual_seed(42)

    # XOR Training Data: 4 examples, 2 features each
    X = torch.tensor([[0.0, 0.0],
                      [0.0, 1.0],
                      [1.0, 0.0],
                      [1.0, 1.0]], dtype=torch.float32)

    Y = torch.tensor([[0.0],
                      [1.0],
                      [1.0],
                      [0.0]], dtype=torch.float32)

    # 2–2–1 Multi-Layer Perceptron Architecture
    class XORNet(nn.Module):
        def __init__(self, hidden_dim=2, activation=nn.Sigmoid):
            super().__init__()
            # Layer 1: 2 inputs -> 2 hidden units
            self.fc1 = nn.Linear(2, hidden_dim)
            # Hidden activation
            self.act = activation()
            # Layer 2: 2 hidden units -> 1 output logit
            self.fc2 = nn.Linear(hidden_dim, 1)

        def forward(self, x):
            # [STAGE 1: FORWARD PASS]
            # Hidden layer pre-activation: a(1) = W(1) * x + b(1)
            h_pre = self.fc1(x)
            # Hidden layer post-activation: h(1) = f(a(1))
            h_post = self.act(h_pre)
            # Output layer pre-activation (logit): z = W(2) * h(1) + b(2)
            logits = self.fc2(h_post)
            return logits

    model = XORNet(hidden_dim=2, activation=nn.Sigmoid)
    
    # Numerically stable Binary Cross-Entropy with Logits loss
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.05)

    # Record initial state
    with torch.no_grad():
        initial_logits = model(X)
        # [STAGE 2: SCALAR LOSS FORMATION]
        initial_loss = criterion(initial_logits, Y).item()
        initial_probs = torch.sigmoid(initial_logits)

    # Full-batch training loop
    num_steps = 3000
    for step in range(num_steps):
        # Reset parameter gradients
        optimizer.zero_grad()
        
        # [STAGE 1: FORWARD PASS]
        logits = model(X)
        
        # [STAGE 2: SCALAR LOSS FORMATION]
        loss = criterion(logits, Y)
        
        # [STAGE 3: REVERSE-MODE AUTOMATIC DIFFERENTIATION (AD)]
        loss.backward()
        
        # [STAGE 4: OPTIMISER STEP]
        optimizer.step()

    # Inspect gradients after the final backward pass
    # Exposing the first-layer weight gradient tensor dL/dW(1)
    fc1_weight_grad = model.fc1.weight.grad.clone()

    # Final evaluation
    with torch.no_grad():
        final_logits = model(X)
        final_loss = criterion(final_logits, Y).item()
        final_probs = torch.sigmoid(final_logits)
        thresholded_preds = (final_probs >= 0.5).float()
        correct_count = (thresholded_preds == Y).sum().item()

    output_lines = [
        "=== Binary XOR 2-2-1 Neural Network Experiment (Task 3 & 4) ===",
        f"Architecture: 2 inputs -> 2 hidden units (Sigmoid) -> 1 logit output",
        f"Loss Function: BCEWithLogitsLoss | Optimizer: Adam (lr=0.05, steps={num_steps})",
        "-" * 65,
        f"Initial Loss: {initial_loss:.6f}",
        f"Final Loss:   {final_loss:.6f}",
        "-" * 65,
        "Final Predictions & Probabilities:",
        f"  (0,0) -> Logit: {final_logits[0].item():8.4f} | Prob: {final_probs[0].item():.6f} | Pred: {int(thresholded_preds[0].item())} | Target: 0",
        f"  (0,1) -> Logit: {final_logits[1].item():8.4f} | Prob: {final_probs[1].item():.6f} | Pred: {int(thresholded_preds[1].item())} | Target: 1",
        f"  (1,0) -> Logit: {final_logits[2].item():8.4f} | Prob: {final_probs[2].item():.6f} | Pred: {int(thresholded_preds[2].item())} | Target: 1",
        f"  (1,1) -> Logit: {final_logits[3].item():8.4f} | Prob: {final_probs[3].item():.6f} | Pred: {int(thresholded_preds[3].item())} | Target: 0",
        "-" * 65,
        f"Accuracy: {correct_count}/4 examples correctly classified.",
        "-" * 65,
        "First-Layer Weight Gradient Tensor (dL / dW(1)) after final backward():",
        f"{fc1_weight_grad}",
        "-" * 65,
        "Autograd Backprop Stages Verified:",
        "  1. Forward Pass: h(1) = sigmoid(W(1)x + b(1)), z = W(2)h(1) + b(2)",
        "  2. Scalar Loss: L = BCEWithLogits(z, y)",
        "  3. Reverse AD: loss.backward() calculates parameter.grad",
        "  4. Optimizer Step: optimizer.step() updates parameters using gradients"
    ]

    output_str = "\n".join(output_lines)
    print(output_str)

    os.makedirs("results", exist_ok=True)
    with open("results/xor_binary_output.txt", "w") as f:
        f.write(output_str + "\n")

if __name__ == "__main__":
    run_xor_binary()
