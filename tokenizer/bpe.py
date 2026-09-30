def get_stats(ids):
    counts = {}
    for a, b in zip(ids, ids[1:]):
        counts[(a, b)] = counts.get((a, b), 0) + 1
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

text = "kitoblar daftarlar qalamlar kitob kitoblarimiz daftarlarimiz"
ids = list(text.encode("utf-8"))
print("Start length:", len(ids))

vocab = {i: bytes([i]) for i in range(256)}   # token number -> the bytes it stands for
merges = {}                                     # pair -> new token number

num_merges = 10
for step in range(num_merges):
    stats = get_stats(ids)
    pair = max(stats, key=stats.get)            # the most frequent pair
    new_id = 256 + step
    ids = merge(ids, pair, new_id)
    merges[pair] = new_id
    vocab[new_id] = vocab[pair[0]] + vocab[pair[1]]
    print(f"merge {step + 1}: {new_id} = {vocab[new_id].decode('utf-8', errors='replace')!r}")

print("End length:", len(ids))

def decode(ids):
    data = b"".join(vocab[i] for i in ids)
    return data.decode("utf-8", errors="replace")

def encode(text):
    ids = list(text.encode("utf-8"))
    while len(ids) >= 2:
        stats = get_stats(ids)
        pair = min(stats, key=lambda p: merges.get(p, float("inf")))
        if pair not in merges:
            break
        ids = merge(ids, pair, merges[pair])
    return ids

for w in ["kitoblar", "daftarlarimiz", "oʻzbek 日本"]:
    ids2 = encode(w)
    print(w, "->", ids2, "->", [decode([i]) for i in ids2], "| round trip:", decode(ids2) == w)