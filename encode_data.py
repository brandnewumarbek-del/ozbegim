import sys
import time
from array import array

sys.path.insert(0, "tokenizer")
from bpe import load, build_vocab, encode, decode, PATTERN

merges = load("tokenizer/uz_bpe.txt")
vocab = build_vocab(merges)

cache = {}                       # word -> its numbers (remember answers)
tokens = array("H")              # "H" = small whole numbers, 2 bytes each (0..65535)

start = time.time()
with open("data/news_clean.txt", encoding="utf-8") as f:
    for line_number, line in enumerate(f):
        for chunk in PATTERN.findall(line):
            if chunk not in cache:
                cache[chunk] = encode(chunk, merges)
            tokens.extend(cache[chunk])
        if line_number % 100_000 == 0:
            print(f"line {line_number:,}  tokens {len(tokens):,}  ({time.time() - start:.0f}s)")

split = int(len(tokens) * 0.9)   # 90% for learning, 10% for the exam
with open("data/train.bin", "wb") as f:
    tokens[:split].tofile(f)
with open("data/val.bin", "wb") as f:
    tokens[split:].tofile(f)

print("Total tokens:", f"{len(tokens):,}")
print("Unique words remembered:", f"{len(cache):,}")
print("Train:", f"{split:,}", " Val:", f"{len(tokens) - split:,}")
print("Check:", decode(tokens[:30].tolist(), vocab))