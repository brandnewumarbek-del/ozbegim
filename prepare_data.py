from datasets import load_dataset

news = load_dataset("tahrirchi/uz-crawl", split="news[:10%]")

print("Articles:", len(news))
print("Fields:", news.column_names)
print("Source:", news[0]["source"])
print(news[0]["text"][:500])

with open("data/news.txt", "w", encoding="utf-8") as f:
    for article in news:
        f.write(article["text"] + "\n\n")

print("Saved to data/news.txt")