# Checkpoint Part III: Build a Small Language Dataset

## Overview & Task Summary
Part III prepares the training corpus for model estimation. The dataset consists of 6 simple English sentences. Text pre-processing involves lowercasing, word tokenisation, and boundary padding with special tokens `<START>` and `<END>`.

### Raw Training Corpus:
1. `the cat sat on the mat`
2. `the cat sat on the rug`
3. `the dog sat on the mat`
4. `the dog ran to the park`
5. `the cat ran to the park`
6. `the dog sat on the rug`

---

## Pre-processed Tokenized Corpus

Every sentence is wrapped with `<START>` at the beginning and `<END>` at the end:

1. `<START> the cat sat on the mat <END>`
2. `<START> the cat sat on the rug <END>`
3. `<START> the dog sat on the mat <END>`
4. `<START> the dog ran to the park <END>`
5. `<START> the cat ran to the park <END>`
6. `<START> the dog sat on the rug <END>`

---

## Evidence Section

### Vocabulary Analysis & Statistics:
- **Total Sentence Count**: 6
- **Total Token Count (including boundary tokens)**: $6 \times 8 = 48$ tokens.
- **Unique Vocabulary Size ($|V|$)**: 12 tokens.
  
`Vocabulary List`:
`['<END>', '<START>', 'cat', 'dog', 'mat', 'on', 'park', 'ran', 'rug', 'sat', 'the', 'to']`

### Python Tokenisation Verification Output:
```python
DATASET = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug"
]

# Output Token Lists:
# Sent 1: ['<START>', 'the', 'cat', 'sat', 'on', 'the', 'mat', '<END>']
# Sent 2: ['<START>', 'the', 'cat', 'sat', 'on', 'the', 'rug', '<END>']
# Sent 3: ['<START>', 'the', 'dog', 'sat', 'on', 'the', 'mat', '<END>']
# Sent 4: ['<START>', 'the', 'dog', 'ran', 'to', 'the', 'park', '<END>']
# Sent 5: ['<START>', 'the', 'cat', 'ran', 'to', 'the', 'park', '<END>']
# Sent 6: ['<START>', 'the', 'dog', 'sat', 'on', 'the', 'rug', '<END>']
```
