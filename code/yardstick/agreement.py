"""文の役割を見分けた2つの結果の一致率を出す(measures.md の「3. 文の役割を見分ける」手順4〜6)。

- 文の役割ごとに、文単位の「当てはまる/当てはまらない」で Krippendorff の α(nominal)
- 前後1文のずれを一致とみなす版も出す
- 関連は、種類、始点、終点の組が一致した割合(2方向の平均)。前後1文の幅の版も出す
使い方: python agreement.py <texts_dir> <結果1のフォルダ> <結果2のフォルダ>
"""
import csv
import glob
import os
import re
import sys

import krippendorff
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from segment import load  # noqa: E402

ROLES = ["起", "承", "転", "結", "問い", "答え", "明かし", "寄り道", "題の主張", "問いへの最後の答え", "書き手の結び"]
COLS = {"読んでいる時点": 1, "読み終えた後": 2}


def roles_of(cell):
    out = set()
    for r in re.split(r"[,、，]", cell or ""):
        r = re.sub(r"\[.*?\]|\(.*?\)|（.*?）", "", r).strip()
        if r in ROLES:
            out.add(r)
    return out


def read_roles(path, n):
    marks = {c: [set() for _ in range(n)] for c in COLS}
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if not row or not re.match(r"s\d{3}$", row[0]):
                continue
            i = int(row[0][1:]) - 1
            if i >= n:
                continue
            for c, j in COLS.items():
                marks[c][i] = roles_of(row[j] if len(row) > j else "")
    if all(not m for c in COLS for m in marks[c]):
        return None
    return marks


def sid(x):
    m = re.match(r"(t00|s\d{3})", x.strip())
    if not m:
        return None
    return 0 if m.group(1) == "t00" else int(m.group(1)[1:])


def read_relations(path):
    edges = []
    if not os.path.exists(path):
        return edges
    with open(path, encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 3 or row[0] == "関連":
                continue
            a, b = sid(row[1]), sid(row[2])
            if a is not None and b is not None:
                edges.append((row[0].strip(), a, b))
    return edges


def alpha(x, y):
    data = np.array([x, y], dtype=float)
    if len(set(data.flatten())) < 2:
        return float("nan")
    return krippendorff.alpha(reliability_data=data, level_of_measurement="nominal")


def tolerant(x, y):
    """x の当てはまる文の前後1文に y の当てはまる文があれば、y をその位置に寄せる。"""
    y = list(y)
    for i, v in enumerate(x):
        if v and not y[i]:
            for j in (i - 1, i + 1):
                if 0 <= j < len(y) and y[j] and not x[j]:
                    y[j], y[i] = 0, 1
                    break
    return y


def edge_match(e1, e2, tol):
    def hit(e, pool):
        return any(e[0] == f[0] and abs(e[1] - f[1]) <= tol and abs(e[2] - f[2]) <= tol for f in pool)
    if not e1 and not e2:
        return float("nan")
    r1 = sum(hit(e, e2) for e in e1) / len(e1) if e1 else 0
    r2 = sum(hit(e, e1) for e in e2) / len(e2) if e2 else 0
    return (r1 + r2) / 2


def main(texts, d1, d2):
    docs = [os.path.basename(p)[:-4] for p in sorted(glob.glob(f"{texts}/*.txt"))]
    pooled = {(c, r): ([], []) for c in COLS for r in ROLES}
    print("## 文書ごとの関連の一致率\n")
    print("| 文書 | 関連の数(1/2) | 一致率 | 前後1文 |")
    print("|---|---|---|---|")
    for d in docs:
        n = len(load(f"{texts}/{d}.txt")["sents"])
        m1, m2 = read_roles(f"{d1}/{d}.roles.tsv", n), read_roles(f"{d2}/{d}.roles.tsv", n)
        if m1 is None or m2 is None:
            continue
        for c in COLS:
            for r in ROLES:
                pooled[(c, r)][0].extend(int(r in s) for s in m1[c])
                pooled[(c, r)][1].extend(int(r in s) for s in m2[c])
        e1, e2 = read_relations(f"{d1}/{d}.relations.tsv"), read_relations(f"{d2}/{d}.relations.tsv")
        print(f"| {d} | {len(e1)}/{len(e2)} | {edge_match(e1, e2, 0):.2f} | {edge_match(e1, e2, 1):.2f} |")
    print("\n## 文の役割ごとの α(8本をまとめて、文単位)\n")
    print("| 文の役割 | 時点 | 当てはまる文の数(1/2) | α | α(前後1文) | 0.667以上 |")
    print("|---|---|---|---|---|---|")
    for c in COLS:
        for r in ROLES:
            x, y = pooled[(c, r)]
            if not x:
                continue
            a, at = alpha(x, y), alpha(x, tolerant(x, y))
            ok = "○" if at >= 0.667 else "×" if at == at else "-"
            print(f"| {r} | {c} | {sum(x)}/{sum(y)} | {a:.2f} | {at:.2f} | {ok} |")


if __name__ == "__main__":
    main(*sys.argv[1:4])
