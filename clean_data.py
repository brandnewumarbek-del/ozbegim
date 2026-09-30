import re

A = "['‘’ʼ`᾽]"                       # every apostrophe type seen in the data
END_OU = {"obro"}                    # words that really end in oʻ

def end_ou(m):
    word = m.group(1)
    if word.lower() in END_OU:
        return word + "ʻ"
    return m.group(0)

def clean_line(line):
    line = line.replace("\u200b", "").replace("\ufeff", "")         # rule 1: invisible characters
    line = line.replace("\xa0", " ")
    line = re.sub(r"([gG])" + A, r"\1ʻ", line)                      # rule 2a: gʻ
    line = re.sub(r"([oO])" + A + r"(?=\w)", r"\1ʻ", line)          # rule 2b: oʻ
    line = re.sub(r"(\w*[oO])" + A + r"(?!\w)", end_ou, line)       # rule 2d: word-end oʻ
    line = re.sub(r"(?<=[^\W\d_])" + A + r"(?=[^\W\d_])", "ʼ", line) # rule 2c: tutuq ʼ
    line = re.sub(r" {2,}", " ", line)                              # rule 3: extra spaces
    return line.strip()

lines = 0
with open("data/news.txt", encoding="utf-8") as src, \
     open("data/news_clean.txt", "w", encoding="utf-8") as out:
    for line in src:
        out.write(clean_line(line) + "\n")   # empty lines stay: they separate articles
        lines += 1

print("Cleaned lines:", lines)