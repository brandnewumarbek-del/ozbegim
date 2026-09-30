from collections import Counter

with open("data/news.txt", encoding="utf-8") as f:
    text = f.read(10_000_000)   # read the first 10 million characters

counts = Counter(text)          # count how often each character appears

print("Different characters:", len(counts))
for char, n in counts.most_common(120):
    print(repr(char), n)

import re

broken = re.findall(r"\w+  (km|m|kishi|nafar)\w*", text)
print("Broken number spots:", len(broken))
print("Examples:", broken[:10])
ends = re.findall(r"\b(\w*[oO])['‘’ʼ`᾽](?!\w)", text)
print(Counter(w.lower() for w in ends).most_common(50))