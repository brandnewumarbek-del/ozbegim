import re
import time
from collections import Counter

# split text into chunks: words (with their leading space), numbers, punctuation, whitespace
PATTERN = re.compile(r" ?[^\W\d_]+| ?\d+| ?[^\s\w]+|\s+")


def get_stats(words):
    counts = Counter()
    for word, freq in words.items():
        for pair in zip(word, word[1:]):
            counts[pair] += freq
    return counts


def merge(ids, pair, new_id):
    result = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and (ids[i], ids[i + 1]) == pair:
            result.append(new_id)
            i += 2
        else:
            result.append(ids[i])
            i += 1
    return result


def train(text, vocab_size):
    chunks = Counter(PATTERN.findall(text))                          # each unique chunk + how often
    words = {tuple(c.encode("utf-8")): n for c, n in chunks.items()}
    print("Unique chunks:", len(words))

    merges = {}
    stats = get_stats(words)                                         # count pairs once
    start = time.time()
    for new_id in range(256, vocab_size):
        pair = max(stats, key=lambda p: (stats[p], p))
        if stats[pair] <= 0:
            break

        changed = []                                                 # only words with the pair change
        for word, freq in words.items():
            if pair[0] in word and pair[1] in word:
                new_word = tuple(merge(word, pair, new_id))
                if new_word != word:
                    changed.append((word, new_word, freq))

        for word, new_word, freq in changed:                         # update counts for those words only
            del words[word]
            words[new_word] = freq
            for p in zip(word, word[1:]):
                stats[p] -= freq
            for p in zip(new_word, new_word[1:]):
                stats[p] += freq

        merges[pair] = new_id
        if new_id % 500 == 0:
            print(f"{new_id} tokens  ({time.time() - start:.0f}s)")
    return merges


def build_vocab(merges):
    vocab = {i: bytes([i]) for i in range(256)}
    for (a, b), new_id in merges.items():                            # dicts keep insertion order
        vocab[new_id] = vocab[a] + vocab[b]
    return vocab


def save(merges, path):
    with open(path, "w") as f:
        for a, b in merges:
            f.write(f"{a} {b}\n")


def load(path):
    merges = {}
    with open(path) as f:
        for new_id, line in enumerate(f, start=256):
            a, b = line.split()
            merges[(int(a), int(b))] = new_id
    return merges


def encode(text, merges):
    ids = []
    for chunk in PATTERN.findall(text):
        chunk_ids = list(chunk.encode("utf-8"))
        while len(chunk_ids) >= 2:
            pairs = set(zip(chunk_ids, chunk_ids[1:]))
            pair = min(pairs, key=lambda p: merges.get(p, float("inf")))
            if pair not in merges:
                break
            chunk_ids = merge(chunk_ids, pair, merges[pair])
        ids.extend(chunk_ids)
    return ids


def decode(ids, vocab):
    return b"".join(vocab[i] for i in ids).decode("utf-8", errors="replace")


if __name__ == "__main__":
    text = open("data/news_clean.txt", encoding="utf-8").read(20_000_000)
    merges = train(text, vocab_size=8000)
    save(merges, "tokenizer/uz_bpe.txt")
    print("Saved", len(merges), "merges")