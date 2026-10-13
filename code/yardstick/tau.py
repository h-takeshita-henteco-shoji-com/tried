"""τ(問いが同じかを決める cos の下限)を、私の ○/× と一致が最大になる値に決める。

予測は cos ≥ τ なら「同じ問い」とする。候補は、隣り合う cos の中点と両端。
一致が最大の候補が複数あれば、すべて出す。
使い方: python tau.py <tau-pairs.tsv>
"""
import csv
import sys

YES = set("○◯〇")


def main(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            mark = (r["同じ問いか(○/×)"] or "").strip()
            if mark:
                rows.append((float(r["cos"]), mark[0] in YES))
    rows.sort()
    cs = [c for c, _ in rows]
    cands = [cs[0] - 0.001] + [(a + b) / 2 for a, b in zip(cs, cs[1:])] + [cs[-1] + 0.001]
    score = {t: sum((c >= t) == y for c, y in rows) for t in cands}
    best = max(score.values())
    pos = [c for c, y in rows if y]
    neg = [c for c, y in rows if not y]
    auc = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg))
    print(f"組の数: {len(rows)}(同じ {len(pos)}、違う {len(neg)})")
    print(f"一致が最大の τ: {', '.join(f'{t:.3f}' for t in cands if score[t] == best)}(一致 {best}/{len(rows)})")
    print(f"仮の τ = 0.85 での一致: {sum((c >= 0.85) == y for c, y in rows)}/{len(rows)}")
    print(f"全部を「違う」とした場合の一致: {len(neg)}/{len(rows)}")
    print(f"AUC(同じ問いの cos が、違う問いの cos より大きい確率): {auc:.2f}")


if __name__ == "__main__":
    main(sys.argv[1])
