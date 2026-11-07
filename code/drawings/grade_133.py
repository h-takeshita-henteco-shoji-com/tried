"""#133 の積算(T-5-1)の答えから、材料ごとの合計と合計金額を拾い出し、正解と比べる。

答えの書き方はモデルごとに違うので、行の中の語と数で拾う。拾えなかった値は「?」にし、人が答えを読んで埋める。
答えの文と、AI が作ったファイル(<問い>-files/ の .md と .txt)の両方を読む。

使い方: uv run --with ezdxf --with shapely python code/drawings/grade_133.py <results/日付/T-dxf>
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import estimate_133 as E  # noqa: E402

KEYS = {  # 項目 → 行に含まれる語
    "フローリング": ["フローリング"], "磁器質タイル": ["タイル"], "クッションフロア": ["クッションフロア"],
    "ビニルクロス(壁)": ["クロス（壁）", "クロス(壁)", "壁クロス", "壁 ビニルクロス", "ビニルクロス 壁"],
    "ビニルクロス(天井)": ["クロス（天井）", "クロス(天井)", "天井クロス", "天井 ビニルクロス", "ビニルクロス 天井"],
    "木製巾木": ["木製巾木"], "ソフト巾木": ["ソフト巾木"],
}
NUM = re.compile(r"(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)")


def texts(d, qid):
    rec = json.loads((d / f"{qid}.json").read_text())
    out = [rec["answer"]]
    files = d / f"{qid}-files"
    if files.exists():
        out += [f.read_text(errors="replace") for f in files.rglob("*") if f.suffix in (".md", ".txt", ".csv")]
    return rec, "\n".join(out)


def pick(text, words, want):
    """語を含む行の数のうち、正解にいちばん近いもの(拾い違いを見るため、近さも返す)。"""
    cands = []
    for line in text.splitlines():
        if any(w in line for w in words):
            for m in NUM.findall(line):
                v = float(m.replace(",", ""))
                if 0 < v < 1000:
                    cands.append(v)
    if not cands:
        return None
    return min(cands, key=lambda v: abs(v - want))


def total(text):
    vals = []
    for line in text.splitlines():
        if "合計" in line or "総額" in line:
            vals += [int(m.replace(",", "")) for m in re.findall(r"\d{1,3}(?:,\d{3}){2,}", line)]
    return max(vals) if vals else None


def main(root):
    truth = E.compute()
    root = Path(root)
    rows = []
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        if not (d / "T-5-1.json").exists():
            continue
        rec, text = texts(d, "T-5-1")
        row = {"model": d.name, "seconds": rec["seconds"], "exit": rec["exit"], "total": total(text)}
        for k, words in KEYS.items():
            row[k] = pick(text, words, truth["totals"][k])
        row["折れ戸を建具に入れた"] = bool(re.search(r"折れ戸[^\n]{0,30}(55,000|65,000)", text))
        rows.append(row)
    print("正解:", {k: truth["totals"][k] for k in KEYS}, "合計", f"{truth['total']:,}")
    for r in rows:
        print(json.dumps(r, ensure_ascii=False))
    return rows


if __name__ == "__main__":
    main(sys.argv[1])
