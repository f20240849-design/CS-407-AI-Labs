"""
Second-Order Markov / Trigram Language Model implementation using standard Python data structures.

This module models P(X_t | X_{t-2}, X_{t-1}) estimated from trigram transition counts.
It supports:
- Initial context convention: ('<START>', '<START>')
- Triple counting C(w_{t-2}, w_{t-1}, w_t)
- Conditional probability table (CPT) construction P(X_t | X_{t-2}, X_{t-1})
- Querying distributions for 2-token context tuples
- Deterministic greedy prediction (argmax with alphabetical tie-breaking)
- Probabilistic text generation until <END>
- Documented fallback policy for unseen context tuples
"""

import random
from collections import defaultdict
from typing import Dict, List, Tuple


DATASET = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug",
]


class TrigramLanguageModel:
    """
    Second-Order Autoregressive Language Model (Trigram Model).
    
    Probability factorization:
        P(X_1, X_2, ..., X_T) = P(X_1 | <START>, <START>) 
                                * P(X_2 | <START>, X_1) 
                                * P(X_3 | X_1, X_2) ...
    """

    def __init__(self, start_token: str = "<START>", end_token: str = "<END>"):
        self.start_token = start_token
        self.end_token = end_token
        self.vocabulary = set()
        self.counts = defaultdict(lambda: defaultdict(int))
        self.probabilities = defaultdict(dict)
        self.is_trained = False

    def tokenize(self, sentence: str) -> List[str]:
        """Convert a sentence string into lowercase tokens with double start tokens and end token."""
        words = sentence.strip().lower().split()
        return [self.start_token, self.start_token] + words + [self.end_token]

    def train(self, sentences: List[str]):
        """
        Build triple counts C(w_{t-2}, w_{t-1}, w_t) and compute CPT probabilities:
            P(w_t | w_{t-2}, w_{t-1}) = C(w_{t-2}, w_{t-1}, w_t) / sum_k C(w_{t-2}, w_{t-1}, w_k)
        """
        self.counts.clear()
        self.probabilities.clear()
        self.vocabulary = {self.start_token, self.end_token}

        for sentence in sentences:
            tokens = self.tokenize(sentence)
            for token in tokens:
                self.vocabulary.add(token)

            for i in range(len(tokens) - 2):
                context = (tokens[i], tokens[i + 1])
                target = tokens[i + 2]
                self.counts[context][target] += 1

        # Calculate CPT P(X_t | X_{t-2}, X_{t-1})
        for context, target_dict in self.counts.items():
            total = sum(target_dict.values())
            for target, count in target_dict.items():
                self.probabilities[context][target] = count / total

        self.is_trained = True

    def get_distribution(self, context: Tuple[str, str]) -> Dict[str, float]:
        """
        Return P(X_t | (X_{t-2}, X_{t-1}) = context).
        Policy for unseen context tuples:
            Emit <END> with probability 1.0 to gracefully terminate text generation.
        """
        if context in self.probabilities and self.probabilities[context]:
            return dict(self.probabilities[context])
        else:
            # Documented Unseen Context Policy:
            # Emit <END> with 1.0 probability when encountering unseen context state.
            return {self.end_token: 1.0}

    def predict_next_greedy(self, context: Tuple[str, str]) -> str:
        """
        Predict argmax_{w} P(w | context).
        Ties are broken alphabetically for deterministic behavior.
        """
        dist = self.get_distribution(context)
        max_prob = max(dist.values())
        candidates = [word for word, prob in dist.items() if abs(prob - max_prob) < 1e-9]
        candidates.sort()  # Alphabetical tie-breaking
        return candidates[0]

    def predict_next_sample(self, context: Tuple[str, str]) -> str:
        """Sample next word according to P(X_t | context)."""
        dist = self.get_distribution(context)
        words = list(dist.keys())
        probs = list(dist.values())
        return random.choices(words, weights=probs, k=1)[0]

    def generate_sentence(self, mode: str = "sample", seed: int = None) -> str:
        """
        Generate a full sentence starting from context ('<START>', '<START>') until <END>.
        mode: 'greedy' or 'sample'
        """
        if seed is not None:
            random.seed(seed)

        tokens = []
        context = (self.start_token, self.start_token)
        max_length = 50  # Safety limit

        for _ in range(max_length):
            if mode == "greedy":
                next_word = self.predict_next_greedy(context)
            else:
                next_word = self.predict_next_sample(context)

            if next_word == self.end_token:
                break

            tokens.append(next_word)
            context = (context[1], next_word)

        return " ".join(tokens)


if __name__ == "__main__":
    model = TrigramLanguageModel()
    model.train(DATASET)

    print("--- SECOND-ORDER TRIGRAM LANGUAGE MODEL ---")
    print(f"Vocabulary ({len(model.vocabulary)} tokens): {sorted(list(model.vocabulary))}\n")

    print("--- TRANSITION PROBABILITIES P(X_t | X_{t-2}, X_{t-1}) ---")
    for ctx in sorted(model.probabilities.keys()):
        dist_str = ", ".join([f"{k}: {v:.4f}" for k, v in sorted(model.probabilities[ctx].items())])
        print(f"P(w | {ctx}) = {{ {dist_str} }}")

    print("\n--- SAMPLE GENERATION (Seed = 42) ---")
    random.seed(42)
    for i in range(5):
        sent = model.generate_sentence(mode="sample")
        print(f"Sampled Sentence {i+1}: <START> {sent} <END>")

    print("\n--- GREEDY GENERATION ---")
    print(f"Greedy Sentence: <START> {model.generate_sentence(mode='greedy')} <END>")
