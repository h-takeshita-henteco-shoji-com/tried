"""8本の数える指標を出し、#47 の判断を再現したかを判定する。

判定の決まりは、その日のフォルダの assets/criteria.md に従う。

使い方: python count.py <texts_dir> [surprisal.tsv]
"""
import csv
import glob
import os
import re
import statistics as st
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from segment import load  # noqa: E402

PAIRS = "ABCD"
FUN_TRUE = "ABD"  # 原文の方が面白い組
KANJI = re.compile(r"[一-鿿々〆ヶ]")


def text_metrics(doc):
    lens = [s["len"] for s in doc["sents"]]
    body = "".join(s["text"] for s in doc["sents"])
    chars = re.sub(r"\s", "", body)
    m = st.mean(lens)
    sd = st.pstdev(lens)
    return {
        "文の数": len(lens),
        "段落の数": doc["npar"],
        "総文字数": doc["total"],
        "文の長さの平均": m,
        "文の長さの変動係数": sd / m,
        "隣の文との長さの差": st.mean(abs(a - b) for a, b in zip(lens, lens[1:])),
        "漢字の割合": len(KANJI.findall(chars)) / len(chars),
    }


def surprisal_metrics(path):
    by = defaultdict(list)
    with open(path) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            by[(r["model"], r["doc"])].append((int(r["par"]), float(r["surprisal_per_char"])))
    out = defaultdict(dict)
    for (model, doc), rows in by.items():
        vals = [v for _, v in rows]
        first, rest, prev = [], [], None
        for par, v in rows:
            (first if par != prev else rest).append(v)
            prev = par
        out[doc][f"サプライザルの平均[{model}]"] = st.mean(vals)
        out[doc][f"サプライザルの標準偏差[{model}]"] = st.pstdev(vals)
        out[doc][f"サプライザルの段落頭の差[{model}]"] = (
            st.mean(first) - st.mean(rest) if rest else float("nan")
        )
    return out


# 向き: +1 は大きいほど面白い/読みやすい、-1 は小さいほど
FUN = {
    "サプライザルの標準偏差": +1,
    "サプライザルの段落頭の差": +1,
    "文の長さの変動係数": +1,
    "隣の文との長さの差": +1,
}
READ = {
    "文の長さの平均": -1,
    "漢字の割合": -1,
    "サプライザルの平均": -1,
}


def base(name):
    return name.split("[")[0]


def judge(table):
    names = [k for k in next(iter(table.values())) if base(k) in FUN or base(k) in READ]
    result = []
    for n in names:
        b = base(n)
        if b in FUN:
            sign = FUN[b]
            hits = [sign * (table[f"{p}-orig"][n] - table[f"{p}-rewrite"][n]) > 0 for p in FUN_TRUE]
            ranked = sorted(table, key=lambda d: -sign * table[d][n])
            c_low = all(ranked.index(f"C-{v}") >= 4 for v in ("orig", "rewrite"))
            result.append(("面白さ", n, sum(hits), len(hits), hits, c_low, ranked))
        else:
            sign = READ[b]
            hits = []
            for p in PAIRS:
                o, r = table[f"{p}-orig"][n], table[f"{p}-rewrite"][n]
                same = abs(o - r) <= 0.05 * (abs(o) + abs(r)) / 2
                hits.append(same or sign * (r - o) > 0)
            result.append(("読みやすさ", n, sum(hits), len(hits), hits, None, None))
    return result


def model_agreement(path):
    """文書ごとに、モデルどうしの文ごとの値の順位相関(Spearman)を出す。"""
    from itertools import combinations

    from scipy.stats import spearmanr

    by = defaultdict(dict)
    with open(path) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            by[r["doc"]].setdefault(r["model"], []).append(float(r["surprisal_per_char"]))
    print("\n## モデルどうしの順位相関\n")
    print("| 文書 | " + " | ".join(f"{a}-{b}" for a, b in combinations(next(iter(by.values())), 2)) + " |")
    print("|---|---|---|---|")
    for doc, m in by.items():
        rhos = [spearmanr(m[a], m[b]).statistic for a, b in combinations(m, 2)]
        print(f"| {doc} | " + " | ".join(f"{r:.2f}" for r in rhos) + " |")


def main(texts_dir, sur_path=None):
    docs = {os.path.basename(f)[:-4]: load(f) for f in sorted(glob.glob(f"{texts_dir}/*.txt"))}
    table = {d: text_metrics(doc) for d, doc in docs.items()}
    if sur_path:
        for d, m in surprisal_metrics(sur_path).items():
            table[d].update(m)
    cols = list(next(iter(table.values())))
    print("## 8本の値\n")
    print("| 指標 | " + " | ".join(table) + " |")
    print("|---|" + "---|" * len(table))
    for c in cols:
        print(f"| {c} | " + " | ".join(f"{table[d][c]:.3g}" for d in table) + " |")
    print("\n## 判断を再現したか\n")
    print("| 軸 | 指標 | 組の向き | 組ごと | C が下位か |")
    print("|---|---|---|---|---|")
    for axis, n, h, tot, hits, c_low, _ in judge(table):
        pairs = FUN_TRUE if axis == "面白さ" else PAIRS
        each = " ".join(f"{p}{'○' if x else '×'}" for p, x in zip(pairs, hits))
        c = "" if c_low is None else ("○" if c_low else "×")
        mark = "再現" if h == tot else f"{h}/{tot}"
        print(f"| {axis} | {n} | {mark} | {each} | {c} |")
    if sur_path:
        model_agreement(sur_path)


if __name__ == "__main__":
    main(*sys.argv[1:])
