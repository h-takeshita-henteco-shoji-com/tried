"""福岡市中央卸売市場の年報(青果物編)から、野菜の品目別・月別の数量と価格を取り出す(#184)。

使い方: .venv/bin/python fukuoka_parse.py
入力: data/raw_fukuoka/*.pdf(https://www.city.fukuoka.lg.jp/nosui/seika/life/documents/ の年報、2016〜2025年)
出力: data/fukuoka_veg_monthly.csv(年月・品目ごとの数量kg、金額円、価格円/kg)
- 表は「野菜品目別月別取扱高表」(1ページに4か月、3ページで12か月)
- 2020・2022・2023年の PDF は文字の対応表が崩れている。数字と記号は一定のずれ(0x3EAC)で戻せる。
  品目名は戻せないので、前後の年の同じページ・同じ行の品目名を当てる(行の数がそろうことを確かめる)
"""
import re
import unicodedata
import subprocess
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
RAW = HERE / "data/raw_fukuoka"
YEAR = {"0insatuyou": 2016, "all_seika_nenpo_29": 2017, "all_seika_nenpo_30": 2018}
YEAR.update({f"all_seika_nenpo_0{i}": 2018 + i for i in range(1, 8)})
TRIPLE = re.compile(r"([\d,]+\.\d+)\s+([\d,]+)\s+([\d,]+)")


def decode(s):
    return "".join(chr(ord(c) - 0x3EAC) if 0x3EAC + 0x20 <= ord(c) <= 0x3EAC + 0x7E else c for c in s)


def pages(pdf):
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    return [decode(p) for p in txt.split("\f")]


def veg_pages(pgs):
    """野菜の月別表のページと、各ページの月の並び。読めない年は、4か月の行が多い連続3ページを1〜4・5〜8・9〜12月とする。"""
    out = [(p, [int(unicodedata.normalize("NFKC", m)) for m in re.findall(r"([０-９0-9]+)月", hdr(p))])
           for p in pgs if "野菜品目別月別取扱高表" in p]
    if out:
        return out
    good = [i for i, p in enumerate(pgs) if sum(len(TRIPLE.findall(l)) == 4 for l in p.splitlines()) >= 15]
    i = next(i for i in good if i + 1 in good and i + 2 in good)
    return [(pgs[i + k], [4 * k + 1, 4 * k + 2, 4 * k + 3, 4 * k + 4]) for k in range(3)]


def hdr(page):
    return next((l for l in page.splitlines() if re.search(r"[０-９0-9]+月", l) and "月別" not in l), "")


def rows(page):
    out = []
    for l in page.splitlines():
        ts = list(TRIPLE.finditer(l))
        if not ts:
            continue
        head = l[: ts[0].start()]
        if len(head) > 1 and head[0] in "根菜類葉茎果豆土物" and head[1] == " ":
            head = head[1:]  # 左端の分類の文字(根・菜・類 など)を除く
        out.append((re.sub(r"\s", "", head), [((t.start() + t.end()) / 2, t.group(1), t.group(2)) for t in ts]))
    return out


def place(rs, months):
    """数字の組を、列の位置で月に割り当てる。列の中心は、組がいちばん多い行の中心の中央値。"""
    k = max(len(c) for _, c in rs)
    full = [c for _, c in rs if len(c) == k]
    centers = [sorted(c[j][0] for c in full)[len(full) // 2] for j in range(k)]
    out = []
    for name, cells in rs:
        for x, kg, yen in cells:
            j = min(range(k), key=lambda q: abs(centers[q] - x))
            if j < len(months):
                out.append((name, months[j], float(kg.replace(",", "")), float(yen.replace(",", ""))))
    return out


def month_kg(rs, ms):
    """行ごとに {月: kg}。"""
    return [(n, {m: kg for n2, m, kg, _ in place([(n, c)], ms)}) for n, c in rs] if False else None


def align(rs, ms, ref):
    """品目名の読めない行を、参照年の行と、量の近さで1対1に対応させる(並び順は保つ)。"""
    import math
    g = [{m: kg for _, m, kg, _ in place(rs, ms) if _ == n} for n, _ in []]  # 使わない
    gp = place_rows(rs, ms)
    rp = []
    for rrs, rms in ref:
        rp += place_rows(rrs, rms)
    # 参照年の品目名ごとに、月→kg(全ページを合わせる)
    refd = {}
    for n, d in rp:
        refd.setdefault(n, {}).update(d)
    order = list(dict.fromkeys(n for n, _ in rp))
    def cost(d, n):
        common = [m for m in d if m in refd[n]]
        if not common:
            return 3.0
        return sum(abs(math.log(d[m] + 1) - math.log(refd[n][m] + 1)) for m in common) / len(common)
    G, R = len(gp), len(order)
    INF = 1e9
    dp = [[INF] * (R + 1) for _ in range(G + 1)]
    bt = [[None] * (R + 1) for _ in range(G + 1)]
    for j in range(R + 1):
        dp[0][j] = 0
    for i in range(1, G + 1):
        for j in range(1, R + 1):
            a = dp[i - 1][j - 1] + cost(gp[i - 1][1], order[j - 1])
            b = dp[i][j - 1]  # 参照年の品目を飛ばす
            dp[i][j], bt[i][j] = (a, "m") if a <= b else (b, "s")
    i, j, names = G, R, [None] * G
    while i > 0:
        if bt[i][j] == "m":
            names[i - 1] = order[j - 1]
            i, j = i - 1, j - 1
        else:
            j -= 1
    return [(names[k], c) for k, (_, c) in enumerate(rs)]


def place_rows(rs, ms):
    out = {}
    order = []
    for idx, (n, c) in enumerate(rs):
        key = (idx, n)
        order.append(key)
        out[key] = {}
    for idx, (n, cells) in enumerate(rs):
        for name, m, kg, yen in place([(n, cells)] + [x for x in rs if len(x[1]) == max(len(y[1]) for y in rs)][:30], ms)[:len(cells)]:
            out[(idx, n)][m] = kg
    return [(n, out[(i, n)]) for i, n in order]


def main():
    parsed = {}
    for pdf in sorted(RAW.glob("*.pdf")):
        parsed[YEAR[pdf.stem]] = [(rows(p), ms) for p, ms in veg_pages(pages(pdf))]
    recs = []
    for y in sorted(parsed):
        for k, (rs, ms) in enumerate(parsed[y]):
            if sum(bool(re.search(r"[ぁ-んァ-ン]", n)) for n, _ in rs) < 10:  # 品目名が読めない年
                ref = next(parsed[r] for r in (2021, 2024, 2019, 2018) if r in parsed
                           and sum(bool(re.search(r"[ぁ-んァ-ン]", n)) for n, _ in parsed[r][0][0]) >= 10)
                rs = align(rs, ms, ref)
            for name, m, kg, yen in place(rs, ms):
                recs.append({"年": y, "月": m, "品目": name, "kg": kg, "円": yen})
    df = pd.DataFrame(recs).drop_duplicates(["年", "月", "品目"])
    df["価格"] = df["円"] / df["kg"]
    df.to_csv(HERE / "data/fukuoka_veg_monthly.csv", index=False)
    cnt = df.groupby("品目").size()
    print(df.shape, "120か月そろう品目:", (cnt == 120).sum())
    print(cnt[cnt >= 110].sort_values().to_string())


if __name__ == "__main__":
    main()
