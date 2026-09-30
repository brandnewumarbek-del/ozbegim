text = open("data/news_clean.txt", encoding="utf-8").read(1_000_000)

chars = sorted(set(text))          # every different character, in order
print("Vocabulary size:", len(chars))

stoi = {ch: i for i, ch in enumerate(chars)}   # character → number
itos = {i: ch for i, ch in enumerate(chars)}   # number → character

def encode(s):
    return [stoi[c] for c in s]

def decode(ids):
    return "".join(itos[i] for i in ids)

ids = encode("kitoblarimizdan")
print(ids)
print(decode(ids))
print(encode("日本"))