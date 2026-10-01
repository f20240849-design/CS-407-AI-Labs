"""
First-Order Markov / Bigram Language Model implementation using standard Python data structures.

This module models P(X_t | X_{t-1}) estimated from bigram transition counts.
It supports:
- Counting transitions C(w_i, w_j)
- Building conditional probability tables (CPTs) P(X_t | X_{t-1})
- Querying next-word distributions for a given token
- Greedy prediction (argmax) with deterministic alphabetical tie-breaking
- Probabilistic text generation by random sampling until <END>
- Documented fallback policy for unseen tokens/contexts
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


class BigramLanguageModel:
    """
    First-Order Autoregressive Language Model (Bigram Model).
    
    Probability factorization:
        P(X_1, X_2, ..., X_T) = P(X_1 | <START>) * P(X_2 | X_1) * ... * P(<END> | X_T)
    """

    def __init__(self, start_token: str = "<START>", end_token: str = "<END>"):
        self.start_token = start_token
        self.end_token = end_token
        self.vocabulary = set()
        self.counts = defaultdict(lambda: defaultdict(int))
        self.probabilities = defaultdict(dict)
        self.is_trained = False

    def tokenize(self, sentence: str) -> List[str]:
        """Convert a sentence string into lowercase tokens with start and end tokens."""
        words = sentence.strip().lower().split()
        return [self.start_token] + words + [self.end_token]

    def train(self, sentences: List[str]):
        """
        Build transition counts C(w_i, w_j) and compute conditional probabilities:
            P(w_j | w_i) = C(w_i, w_j) / sum_k C(w_i, w_k)
        """
        self.counts.clear()
        self.probabilities.clear()
        self.vocabulary = {self.start_token, self.end_token}

        for sentence in sentences:
            tokens = self.tokenize(sentence)
            for token in tokens:
                self.vocabulary.add(token)
            
            for i in range(len(tokens) - 1):
                w_curr = tokens[i]
                w_next = tokens[i + 1]
                self.counts[w_curr][w_next] += 1

        # Calculate CPT P(X_t | X_{t-1})
        for w_curr, next_dict in self.counts.items():
            total = sum(next_dict.values())
            for w_next, count in next_dict.items():
                self.probabilities[w_curr][w_next] = count / total

        self.is_trained = True

    def get_distribution(self, current_word: str) -> Dict[str, float]:
        """
        Return P(X_t | X_{t-1} = current_word).
        Policy for unseen words or terminal tokens with no outgoing transitions:
            Return {self.end_token: 1.0} to gracefully terminate text generation.
        """
        if current_word in self.probabilities and self.probabilities[current_word]:
            return dict(self.probabilities[current_word])
        else:
            # Documented Unseen Word Policy:
            # Emit <END> with probability 1.0 to ensure deterministic and safe sequence termination.
            return {self.end_token: 1.0}

    def predict_next_greedy(self, current_word: str) -> str:
        """
        Predict argmax_{w} P(w | current_word).
        Ties are broken alphabetically for deterministic behavior.
        """
        dist = self.get_distribution(current_word)
        max_prob = max(dist.values())
        candidates = [word for word, prob in dist.items() if abs(prob - max_prob) < 1e-9]
        candidates.sort()  # Alphabetical tie-breaking
        return candidates[0]

    def predict_next_sample(self, current_word: str) -> str:
        """Sample next word according to P(X_t | X_{t-1} = current_word)."""
        dist = self.get_distribution(current_word)
        words = list(dist.keys())
        probs = list(dist.values())
        return random.choices(words, weights=probs, k=1)[0]

    def generate_sentence(self, mode: str = "sample", seed: int = None) -> str:
        """
        Generate a full sentence starting from <START> until <END>.
        mode: 'greedy' or 'sample'
        """
        if seed is not None:
            random.seed(seed)

        tokens = []
        current = self.start_token
        max_length = 50  # Prevent infinite loops

        for _ in range(max_length):
            if mode == "greedy":
                next_word = self.predict_next_greedy(current)
            else:
                next_word = self.predict_next_sample(current)

            if next_word == self.end_token:
                break

            tokens.append(next_word)
            current = next_word

        return " ".join(tokens)


if __name__ == "__main__":
    model = BigramLanguageModel()
    model.train(DATASET)

    print("--- FIRST-ORDER BIGRAM LANGUAGE MODEL ---")
    print(f"Vocabulary ({len(model.vocabulary)} tokens): {sorted(list(model.vocabulary))}\n")

    print("--- TRANSITION PROBABILITIES P(X_t | X_{t-1}) ---")
    for word in sorted(model.probabilities.keys()):
        dist_str = ", ".join([f"{k}: {v:.4f}" for k, v in sorted(model.probabilities[word].items())])
        print(f"P(w | '{word}') = {{ {dist_str} }}")

    print("\n--- SAMPLE GENERATION (Seed = 42) ---")
    random.seed(42)
    for i in range(5):
        sent = model.generate_sentence(mode="sample")
        print(f"Sampled Sentence {i+1}: <START> {sent} <END>")

    print("\n--- GREEDY GENERATION ---")
    print(f"Greedy Sentence: <START> {model.generate_sentence(mode='greedy')} <END>")
