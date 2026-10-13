"""AIが見分けた文の役割、関連、特徴を、文書ごとに数える(1次データの集計)。

- 役割は「読み終えた後の役割」で数える。転は [全体] と [内側] を分ける
- 役割が変わった文 = 読んでいる時点と読み終えた後で、役割の集合が違う文
使い方: python role_counts.py <texts_dir> <labeling_run_dir>...
"""
import csv
import glob
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from agreement import ROLES, roles_of  # noqa: E402
from segment import load  # noqa: E402

RELS = ["予想を作る", "理由を渡す", "答える", "伏せる", "先に明かす", "外れる"]
FEATS = ["型", "崩し", "具体", "声", "たとえ"]


def count(texts, run):
    rows = {}
    for p in sorted(glob.glob(f"{texts}/*.txt")):
        d = os.path.basename(p)[:-4]
        doc = load(p)
        c = Counter()
        changed = 0
        for line in open(f"{run}/{d}.roles.tsv", encoding="utf-8"):
            r = line.rstrip("\n").split("\t")
            if not re.match(r"s\d{3}$", r[0]):
                continue
            now = r[1] if len(r) > 1 else ""
            after = r[2] if len(r) > 2 else ""
            for role in roles_of(after):
                c[role] += 1
            a = after.replace(" ", "")
            c["転[全体]"] += "転[全体]" in a
            c["転[内側]"] += "転[内側]" in a
            changed += roles_of(now) != roles_of(after)
        for r in csv.reader(open(f"{run}/{d}.relations.tsv", encoding="utf-8"), delimiter="\t"):
            if r and r[0].strip() in RELS:
                c["関連:" + r[0].strip()] += 1
        for r in csv.reader(open(f"{run}/{d}.features.tsv", encoding="utf-8"), delimiter="\t"):
            if len(r) > 2 and r[2].strip() in FEATS:
                c["特徴:" + r[2].strip()] += 1
        c["文の数"] = len(doc["sents"])
        c["役割が変わった文"] = changed
        rows[d] = c
    return rows


def main(texts, *runs):
    keys = (["文の数"] + ROLES[:2] + ["転[全体]", "転[内側]"] + ROLES[3:] + ["役割が変わった文"]
            + ["関連:" + r for r in RELS] + ["特徴:" + f for f in FEATS])
    tables = [count(texts, r) for r in runs]
    docs = list(tables[0])
    print("値は「1回目/2回目」。役割は読み終えた後の役割で数えた\n")
    print("| 項目 | " + " | ".join(docs) + " |")
    print("|---|" + "---|" * len(docs))
    for k in keys:
        print(f"| {k} | " + " | ".join("/".join(str(t[d][k]) for t in tables) for d in docs) + " |")


if __name__ == "__main__":
    main(*sys.argv[1:])
