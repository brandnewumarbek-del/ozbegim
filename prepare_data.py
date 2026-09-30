from datasets import load_dataset

wiki = load_dataset("wikimedia/wikipedia", "20231101.uz", split="train")

print ("Articles:", len(wiki))
print("First title:", wiki[0]["title"])
print(wiki[0]["text"][:500])

with open("data/uzwiki.txt", "w", encoding="utf-8") as f:
    for article in wiki:
        f.write(article["text"] + "\n\n")

print("Saved to data/uzwiki.txt")