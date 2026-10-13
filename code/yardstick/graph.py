"""文どうしの関連(relations.tsv)から、構成の指標を出す(measures.md の「構成の側: グラフとして数える」の3)。

- 答えの先出し率 = 「答える」と「先に明かす」の関連のうち、答えや明かしが問いや転より前に来る割合。
  「先に明かす」は、題や見出しから先に言っているので、すべて先出しに数える
- 理由の先置き率 = 「理由を渡す」の関連のうち、結が転より前にある割合
- 題からの先に明かす = 題 t00 から出る「先に明かす」の関連の数
範囲で書かれた文番号は、始まりの文を使う。
使い方: python graph.py <relations のフォルダ>...
"""
import glob
import os
import re
import sys


def sid(x):
    m = re.match(r"(t00|s\d{3})", x.strip())
    if not m:
        return None
    return 0 if m.group(1) == "t00" else int(m.group(1)[1:])


def edges(path):
    out = []
    for line in open(path, encoding="utf-8"):
        row = line.rstrip("\n").split("\t")
        if len(row) < 3 or row[0] == "関連":
            continue
        a, b = sid(row[1]), sid(row[2])
        if a is not None and b is not None:
            out.append((row[0].strip(), a, b))
    return out


def metrics(es):
    ans = [e for e in es if e[0] == "答える"]
    rev = [e for e in es if e[0] == "先に明かす"]
    why = [e for e in es if e[0] == "理由を渡す"]
    first = sum(a < b for _, a, b in ans) + len(rev)
    n = len(ans) + len(rev)
    return {
        "答えの先出し率": first / n if n else float("nan"),
        "(先出し/対象)": f"{first}/{n}",
        "理由の先置き率": sum(a < b for _, a, b in why) / len(why) if why else float("nan"),
        "題からの先に明かす": sum(1 for _, a, _ in rev if a == 0),
    }


if __name__ == "__main__":
    for d in sys.argv[1:]:
        print(f"## {os.path.basename(d)}\n")
        print("| 文書 | 答えの先出し率 | (先出し/対象) | 理由の先置き率 | 題からの先に明かす |")
        print("|---|---|---|---|---|")
        for p in sorted(glob.glob(f"{d}/*.relations.tsv")):
            m = metrics(edges(p))
            v = [f"{x:.2f}" if isinstance(x, float) else str(x) for x in m.values()]
            print(f"| {os.path.basename(p).split('.')[0]} | " + " | ".join(v) + " |")
        print()
