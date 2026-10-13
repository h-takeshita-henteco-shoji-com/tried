"""AIの読者が文章を覚えていないかを確かめる(measures.md の「AIの読者が覚えていないかを確かめる」)。

冒頭だけを渡して続きを200字書かせ、3回くり返す。原文の続き200字と、文字5-gram の一致率を出す。
一致率 = 書かせた続きの5-gram のうち、原文の続きの5-gram にもあるものの割合
使い方: python memory.py <texts_dir> <out.tsv> 文書名...
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from label import claude  # noqa: E402
from reader import MODEL, opening_end  # noqa: E402
from segment import load  # noqa: E402

PROMPT = """次は、ある文章の題と冒頭です。この続きを200字程度で書いてください。前置きや解説は付けず、続きの本文だけを出してください。

題: {title}

{opening}"""


def grams(s, n=5):
    s = re.sub(r"\s", "", s)
    return {s[i:i + n] for i in range(len(s) - n + 1)}


def main(texts, out, docs):
    rows = []
    for d in docs:
        doc = load(f"{texts}/{d}.txt")
        p0 = opening_end(doc)
        opening = "\n".join(s["text"] for s in doc["sents"] if s["par"] <= p0)
        truth = re.sub(r"\s", "", "".join(s["text"] for s in doc["sents"] if s["par"] > p0))[:200]
        g_truth = grams(truth)
        for i in range(1, 4):
            gen = claude(PROMPT.format(title=doc["title"], opening=opening), MODEL)
            g = grams(gen)
            rate = len(g & g_truth) / len(g) if g else 0.0
            rows.append((d, i, rate, gen.replace("\n", " ")))
            print(d, i, f"{rate:.3f}", file=sys.stderr)
    with open(out, "w") as f:
        f.write("doc\ttry\toverlap\tgenerated\n")
        for r in rows:
            f.write(f"{r[0]}\t{r[1]}\t{r[2]:.3f}\t{r[3]}\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
