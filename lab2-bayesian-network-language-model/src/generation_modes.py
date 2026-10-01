"""
Generation Modes Script: Mode A (Greedy Argmax) vs Mode B (Probabilistic Sampling).

Produces 5 sentences for each mode across both Bigram and Trigram language models.
Alphabetical tie-breaking is enforced for Mode A greedy generation to ensure deterministic outputs.
"""

import random
from bigram_model import BigramLanguageModel, DATASET as BIGRAM_DATASET
from trigram_model import TrigramLanguageModel, DATASET as TRIGRAM_DATASET


def run_generation_modes():
    print("=" * 60)
    print("      GENERATION MODES COMPARISON: GREEDY vs SAMPLING")
    print("=" * 60)

    # 1. Bigram Model
    bigram = BigramLanguageModel()
    bigram.train(BIGRAM_DATASET)

    print("\n--- FIRST-ORDER BIGRAM MODEL ---")
    print("\n[Mode A: Greedy Generation (Deterministic, 5 runs)]")
    for i in range(5):
        # Greedy generation is deterministic, so all 5 runs will produce identical sentences.
        sent = bigram.generate_sentence(mode="greedy")
        print(f"Run {i+1}: <START> {sent} <END>")

    print("\n[Mode B: Probabilistic Sampling Generation (Seeded seed=42, 5 runs)]")
    random.seed(42)
    for i in range(5):
        sent = bigram.generate_sentence(mode="sample")
        print(f"Run {i+1}: <START> {sent} <END>")

    # 2. Trigram Model
    trigram = TrigramLanguageModel()
    trigram.train(TRIGRAM_DATASET)

    print("\n--- SECOND-ORDER TRIGRAM MODEL ---")
    print("\n[Mode A: Greedy Generation (Deterministic, 5 runs)]")
    for i in range(5):
        sent = trigram.generate_sentence(mode="greedy")
        print(f"Run {i+1}: <START> {sent} <END>")

    print("\n[Mode B: Probabilistic Sampling Generation (Seeded seed=42, 5 runs)]")
    random.seed(42)
    for i in range(5):
        sent = trigram.generate_sentence(mode="sample")
        print(f"Run {i+1}: <START> {sent} <END>")


if __name__ == "__main__":
    run_generation_modes()
