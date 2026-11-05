"""採点の資料を作り、採点の結果を集める(#138。#132 で手で行った手順をスクリプトにした)。

採点はサブエージェントに任せる。採点の偏りを減らすため、モデルの名前と渡し方(DXF/PNG)を伏せる。
- bundle: 問いごとに、決まり・正解・答え(記号つき、順番を混ぜる)を1つの md にまとめ、記号の対応を mapping.json に残す
- collect: サブエージェントが書いた <問い>.grades.json と mapping.json を合わせ、grades-<図面>.json と点数の表を作る

使い方:
  uv run python make_grading.py bundle  --issue 138 --drawing P
  uv run python make_grading.py collect --issue 138 --drawing P
  (#134 の MCP の結果) ... bundle --issue 138 --drawing P --res <#134 の results/2026-11-05-138> --formats mcp
"""
import argparse
import json
import random
import re
from collections import defaultdict
from pathlib import Path

from run_eval import ISSUES, MODELS, load_questions

SCORE = {"正答": 1, "適切な保留": 1, "部分正答": 0.5, "誤答": 0, "誤った断定": 0, "不要な保留": 0}


FORMATS = ("dxf", "png")
RES = None  # --res で、結果の置き場所を変える(#134 の MCP の結果など)


def paths(issue, drawing, day):
    cfg = ISSUES[issue]
    res = RES or cfg["day"] / "results" / day
    return cfg, res, res / f"grading-{drawing}"


def key_sections(text):
    """正解の記録を、決まりと図面のメモの節と、問いごとの節に分ける。"""
    rules = re.split(r"^## [LMHP]-\d ", text.split("## 決まり", 1)[1], maxsplit=1, flags=re.M)[0]
    parts = re.split(r"^(?=### [LMHP]-\d-\d )", text, flags=re.M)
    qs = {}
    for p in parts[1:]:
        qid = p.split()[1]
        qs[qid] = p.split("\n## ", 1)[0].strip()
    return "## 決まり" + rules, qs


def bundle(issue, drawing, day):
    cfg, res, out = paths(issue, drawing, day)
    out.mkdir(parents=True, exist_ok=True)
    rules, qs = key_sections((cfg["day"] / "answer-key" / cfg["keys"][drawing]).read_text())
    mapping = {}
    rng = random.Random(f"{issue}-{drawing}")
    for qid in load_questions(issue, drawing):
        items = []
        for fmt in FORMATS:
            for model in MODELS:
                f = res / f"{drawing}-{fmt}" / f"{model}__medium" / f"{qid}.json"
                if f.exists():
                    items.append((model, fmt, json.loads(f.read_text())["answer"]))
        rng.shuffle(items)
        lines = [f"# 採点の資料 {qid}", "", "## 採点の決まり", "", rules, "", "## この問いの正解", "", qs[qid], "",
                 "## 採点する答え", ""]
        for i, (model, fmt, ans) in enumerate(items, 1):
            code = f"{qid}-{i:02d}"
            mapping[code] = {"model": model, "format": fmt}
            lines += [f"### 答え {code}", "", ans or "(答えなし)", ""]
        (out / f"{qid}.md").write_text("\n".join(lines))
        print(qid, len(items))
    (out / "mapping.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=1))


def collect(issue, drawing, day):
    cfg, res, out = paths(issue, drawing, day)
    mapping = json.loads((out / "mapping.json").read_text())
    rows = []
    for f in sorted(out.glob("*.grades.json")):
        for g in json.loads(f.read_text()):
            m = mapping[g["code"]]
            rows.append({"qid": g["code"].rsplit("-", 1)[0], **m, **g})
    (res / f"grades-{drawing}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    total = defaultdict(float)
    for r in rows:
        total[(r["model"], r["format"])] += SCORE[r["grade"]]
    n = len(load_questions(issue, drawing))
    print(f"| モデル | " + " | ".join(f"{drawing} {f.upper()}" for f in FORMATS) + " |")
    print("|---|" + "---|" * len(FORMATS))
    for model in MODELS:
        print(f"| {model} | " + " | ".join(f"{total[(model, f)]:g}" for f in FORMATS) + " |")
    print(f"{len(rows)} 件、{n} 点満点、迷った判定 {sum(r.get('borderline', False) for r in rows)} 件")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["bundle", "collect"])
    ap.add_argument("--issue", default="138", choices=ISSUES)
    ap.add_argument("--drawing", required=True)
    ap.add_argument("--day", default="2026-11-02")
    ap.add_argument("--res", default=None, help="結果の置き場所。既定は <issue の日のフォルダ>/results/<day>")
    ap.add_argument("--formats", default="dxf,png", help="比べる形式。#134 の MCP の結果は mcp")
    a = ap.parse_args()
    RES = Path(a.res) if a.res else None
    FORMATS = tuple(a.formats.split(","))
    (bundle if a.step == "bundle" else collect)(a.issue, a.drawing, a.day)
