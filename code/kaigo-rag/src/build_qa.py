"""介護サービス関係Q&A集(Excel)を、1問1件のチャンクにする。

入力: data/raw/qa_all.xlsx(厚労省「介護サービス関係Q&A集」令和8年9月掲載版)
出力: data/qa_all.jsonl
"""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CONT = "（上の行の続き）"


def clean(v) -> str:
    if pd.isna(v):
        return ""
    return str(v).replace(CONT, "").strip()


def wareki_year(src: str):
    """出典の先頭「24.3.16」「6.4.18」などから、発出の年を西暦の目安にする。"""
    src = re.sub(r"^\s*元", "1", src)
    m = re.match(r"\s*(\d+)\s*[\.．]", src)
    if not m:
        return None
    y = int(m.group(1))
    # 平成12〜31年 と 令和1〜8年 を見分ける(令和は 1〜8、平成は 12 以上)
    return 2018 + y if y <= 8 else 1988 + y


def main():
    d = pd.read_excel(ROOT / "data/raw/qa_all.xlsx", header=None, skiprows=4)
    d.columns = ["_", "課", "連番", "種別old", "種別new", "基準種別", "項目", "質問", "回答", "出典", "問番号", "_2"]
    d["種別"] = d["種別old"].fillna(d["種別new"])

    rows = []
    for _, r in d.iterrows():
        q, a = clean(r["質問"]), clean(r["回答"])
        is_cont = str(r["質問"]).startswith(CONT) or str(r["回答"]).startswith(CONT)
        if is_cont and rows:
            rows[-1]["question"] += ("\n" + q) if q else ""
            rows[-1]["answer"] += ("\n" + a) if a else ""
            continue
        if not q and not a:
            continue
        src = clean(r["出典"]).replace("\n", " ")
        rows.append(
            {
                "qa_id": f"QA{len(rows) + 1:04d}",
                "service": re.sub(r"\s+", " ", clean(r["種別"])),
                "category": clean(r["基準種別"]),
                "item": clean(r["項目"]),
                "question": q,
                "answer": a,
                "source": src,
                "year": wareki_year(src),
            }
        )
    with open(ROOT / "data/qa_all.jsonl", "w") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    print(len(rows), "QA")
    print(pd.Series([x["year"] for x in rows]).describe())


if __name__ == "__main__":
    main()
