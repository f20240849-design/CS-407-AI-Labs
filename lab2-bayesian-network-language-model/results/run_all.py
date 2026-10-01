"""
Master Execution Runner: run_all.py

Executes all model training, normalisation tests, text generation experiments, and comparative metrics calculation.
Outputs and updates:
- results/cpts.txt
- results/generated_sentences.txt
- results/normalisation.txt
- results/comparison.md
"""

import random
import sys
from pathlib import Path

# Add src and tests to path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir / "src"))
sys.path.append(str(root_dir / "tests"))

from bigram_model import BigramLanguageModel, DATASET as BIGRAM_DATASET
from trigram_model import TrigramLanguageModel, DATASET as TRIGRAM_DATASET
from test_normalisation import test_normalisation
from compare_models import compare_models


def generate_cpts_file(bigram: BigramLanguageModel, trigram: TrigramLanguageModel, output_path: Path):
    lines = []
    lines.append("============================================================")
    lines.append("   CONDITIONAL PROBABILITY TABLES (CPTs) - EXACT CALCULATIONS")
    lines.append("============================================================\n")

    lines.append("--- FIRST-ORDER BIGRAM MODEL CPT P(X_t | X_{t-1}) ---")
    for word in sorted(bigram.probabilities.keys()):
        lines.append(f"\nContext word: '{word}'")
        total_count = sum(bigram.counts[word].values())
        lines.append(f"  Total observed occurrences as context: {total_count}")
        for next_word, prob in sorted(bigram.probabilities[word].items()):
            count = bigram.counts[word][next_word]
            lines.append(f"  P({next_word:6s} | {word:8s}) = {count}/{total_count} = {prob:.4f}")

    lines.append("\n" + "-" * 60 + "\n")
    lines.append("--- SECOND-ORDER TRIGRAM MODEL CPT P(X_t | X_{t-2}, X_{t-1}) ---")
    for context in sorted(trigram.probabilities.keys()):
        ctx_str = f"('{context[0]}', '{context[1]}')"
        lines.append(f"\nContext tuple: {ctx_str}")
        total_count = sum(trigram.counts[context].values())
        lines.append(f"  Total observed occurrences as context: {total_count}")
        for next_word, prob in sorted(trigram.probabilities[context].items()):
            count = trigram.counts[context][next_word]
            lines.append(f"  P({next_word:6s} | {ctx_str:18s}) = {count}/{total_count} = {prob:.4f}")

    lines.append("\n============================================================")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[INFO] CPTs successfully written to: {output_path}")


def generate_sentences_file(bigram: BigramLanguageModel, trigram: TrigramLanguageModel, output_path: Path):
    lines = []
    lines.append("============================================================")
    lines.append("           GENERATED SENTENCES (20+ SAMPLES)")
    lines.append("============================================================")
    lines.append("NOTE: Deterministic outputs (Greedy Mode A) are exact mathematical")
    lines.append("argmax predictions. Sampled outputs (Mode B) use random.seed(42).")
    lines.append("The exact sampled sentences depend on Python's pseudo-random")
    lines.append("generator, but all transitions maintain non-zero CPT probability.")
    lines.append("============================================================\n")

    lines.append("--- FIRST-ORDER BIGRAM MODEL GENERATION ---")
    lines.append("\n[Mode A: Greedy Argmax Generation (Deterministic)]")
    lines.append(f"Greedy Output: <START> {bigram.generate_sentence(mode='greedy')} <END>")

    lines.append("\n[Mode B: Probabilistic Sampling (20 Sentences, seed=42)]")
    random.seed(42)
    for i in range(20):
        sent = bigram.generate_sentence(mode="sample")
        lines.append(f"Sample {i+1:02d}: <START> {sent} <END>")

    lines.append("\n" + "-" * 60 + "\n")
    lines.append("--- SECOND-ORDER TRIGRAM MODEL GENERATION ---")
    lines.append("\n[Mode A: Greedy Argmax Generation (Deterministic)]")
    lines.append(f"Greedy Output: <START> {trigram.generate_sentence(mode='greedy')} <END>")

    lines.append("\n[Mode B: Probabilistic Sampling (20 Sentences, seed=42)]")
    random.seed(42)
    for i in range(20):
        sent = trigram.generate_sentence(mode="sample")
        lines.append(f"Sample {i+1:02d}: <START> {sent} <END>")

    lines.append("\n============================================================")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[INFO] Generated sentences written to: {output_path}")


def main():
    print("Running master execution runner...")

    results_dir = root_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # Train models
    bigram = BigramLanguageModel()
    bigram.train(BIGRAM_DATASET)

    trigram = TrigramLanguageModel()
    trigram.train(TRIGRAM_DATASET)

    # 1. Save CPTs
    generate_cpts_file(bigram, trigram, results_dir / "cpts.txt")

    # 2. Save Generated Sentences
    generate_sentences_file(bigram, trigram, results_dir / "generated_sentences.txt")

    # 3. Run Normalisation Tests
    test_normalisation()

    # 4. Run Model Comparison
    compare_models()

    print("\n[SUCCESS] All results generated and verified successfully!")


if __name__ == "__main__":
    main()
