"""
Probability Normalisation Verification Test Suite.

Verifies the essential probabilistic invariant:
    sum_{v} P(v | context) == 1.0
for every valid context in both First-Order (Bigram) and Second-Order (Trigram) models.

Outputs results to stdout and saves to 'results/normalisation.txt'.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from bigram_model import BigramLanguageModel, DATASET as BIGRAM_DATASET
from trigram_model import TrigramLanguageModel, DATASET as TRIGRAM_DATASET


def test_normalisation():
    output_lines = []
    output_lines.append("============================================================")
    output_lines.append("       PROBABILITY NORMALISATION TEST RESULTS")
    output_lines.append("============================================================\n")

    # 1. Bigram Model Normalisation
    bigram = BigramLanguageModel()
    bigram.train(BIGRAM_DATASET)

    output_lines.append("--- FIRST-ORDER BIGRAM MODEL NORMALISATION ---")
    bigram_all_passed = True
    for word, dist in sorted(bigram.probabilities.items()):
        total = sum(dist.values())
        status = "PASSED" if abs(total - 1.0) < 1e-6 else "FAILED"
        if status == "FAILED":
            bigram_all_passed = False
        output_lines.append(f"Context '{word:8s}': sum = {total:.6f} [{status}]")
        for next_word, prob in sorted(dist.items()):
            output_lines.append(f"  P({next_word:6s} | {word:8s}) = {prob:.4f}")

    output_lines.append(f"\nBigram Normalisation Status: {'ALL PASSED' if bigram_all_passed else 'FAILED'}\n")

    # 2. Trigram Model Normalisation
    trigram = TrigramLanguageModel()
    trigram.train(TRIGRAM_DATASET)

    output_lines.append("--- SECOND-ORDER TRIGRAM MODEL NORMALISATION ---")
    trigram_all_passed = True
    for context, dist in sorted(trigram.probabilities.items()):
        total = sum(dist.values())
        status = "PASSED" if abs(total - 1.0) < 1e-6 else "FAILED"
        if status == "FAILED":
            trigram_all_passed = False
        ctx_str = f"({context[0]}, {context[1]})"
        output_lines.append(f"Context '{ctx_str:16s}': sum = {total:.6f} [{status}]")
        for next_word, prob in sorted(dist.items()):
            output_lines.append(f"  P({next_word:6s} | {ctx_str:16s}) = {prob:.4f}")

    output_lines.append(f"\nTrigram Normalisation Status: {'ALL PASSED' if trigram_all_passed else 'FAILED'}\n")
    output_lines.append("============================================================")

    result_text = "\n".join(output_lines)
    print(result_text)

    # Save to results/normalisation.txt
    results_dir = Path(__file__).resolve().parent.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    norm_file = results_dir / "normalisation.txt"
    norm_file.write_text(result_text, encoding="utf-8")
    print(f"\n[INFO] Normalisation results saved to: {norm_file}")


if __name__ == "__main__":
    test_normalisation()
