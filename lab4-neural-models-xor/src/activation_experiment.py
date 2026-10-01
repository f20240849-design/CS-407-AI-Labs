import os
import torch
import torch.nn as nn
import torch.optim as optim

def evaluate_activation(activation_cls, activation_name, seed=42, num_steps=3000, lr=0.05, early_step=5):
    torch.manual_seed(seed)

    X = torch.tensor([[0.0, 0.0],
                      [0.0, 1.0],
                      [1.0, 0.0],
                      [1.0, 1.0]], dtype=torch.float32)

    Y = torch.tensor([[0.0],
                      [1.0],
                      [1.0],
                      [0.0]], dtype=torch.float32)

    class ModularXORNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(2, 2)
            self.act = activation_cls()
            self.fc2 = nn.Linear(2, 1)

        def forward(self, x):
            return self.fc2(self.act(self.fc1(x)))

    model = ModularXORNet()
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    early_grad_norm = None

    for step in range(num_steps):
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, Y)
        loss.backward()

        if step == early_step:
            w1_grad = model.fc1.weight.grad
            early_grad_norm = torch.norm(w1_grad, p=2).item()

        optimizer.step()

    with torch.no_grad():
        final_logits = model(X)
        final_loss = criterion(final_logits, Y).item()
        final_probs = torch.sigmoid(final_logits)
        preds = (final_probs >= 0.5).float()
        is_4_of_4 = (preds == Y).all().item()

    return {
        "activation": activation_name,
        "seed": seed,
        "final_loss": final_loss,
        "is_4_of_4": is_4_of_4,
        "early_grad_norm": early_grad_norm
    }

def run_activation_experiment():
    activations = [
        (nn.Sigmoid, "Sigmoid"),
        (nn.Tanh, "Tanh"),
        (nn.ReLU, "ReLU")
    ]
    
    seeds = [42, 100, 777, 2026]
    
    print("=== Activation Function Comparison Experiment (Task 4 Part D) ===")
    
    # Primary evaluation on seed 42
    primary_results = []
    for act_cls, name in activations:
        res = evaluate_activation(act_cls, name, seed=42)
        primary_results.append(res)
    
    # Multi-seed stability summary
    all_runs = []
    for act_cls, name in activations:
        for seed in seeds:
            res = evaluate_activation(act_cls, name, seed=seed)
            all_runs.append(res)

    # Format Markdown Table for results/activation_table.md
    markdown_lines = [
        "# Activation Experiment Results (Seed 42)",
        "",
        "| Hidden Activation | Final Loss | 4/4 Correct? | Early $\|\\nabla_{W^{(1)}} L\|_2$ (Step 5) |",
        "|:---:|:---:|:---:|:---:|"
    ]

    for r in primary_results:
        correct_str = "Yes (4/4)" if r["is_4_of_4"] else "No"
        markdown_lines.append(f"| **{r['activation']}** | {r['final_loss']:.6f} | {correct_str} | {r['early_grad_norm']:.6f} |")

    markdown_lines.extend([
        "",
        "## Multi-Seed Robustness Summary (Seeds: 42, 100, 777, 2026)",
        "",
        "| Hidden Activation | Convergence Rate (4/4 Correct) | Average Final Loss | Notes |",
        "|:---:|:---:|:---:|:---|"
    ])

    for act_cls, name in activations:
        runs = [r for r in all_runs if r["activation"] == name]
        successes = sum(1 for r in runs if r["is_4_of_4"])
        avg_loss = sum(r["final_loss"] for r in runs) / len(runs)
        rate_str = f"{successes}/{len(runs)} ({successes/len(runs)*100:.0f}%)"
        
        note = ""
        if name == "Sigmoid":
            note = "Slower convergence due to derivative saturation at high/low pre-activations."
        elif name == "Tanh":
            note = "Fastest convergence; zero-centered activation speeds up optimization."
        elif name == "ReLU":
            note = "Fast when active, but can suffer from dead units if initialized negatively."

        markdown_lines.append(f"| **{name}** | {rate_str} | {avg_loss:.6f} | {note} |")

    markdown_content = "\n".join(markdown_lines)
    print(markdown_content)

    os.makedirs("results", exist_ok=True)
    with open("results/activation_table.md", "w") as f:
        f.write(markdown_content + "\n")

if __name__ == "__main__":
    run_activation_experiment()
