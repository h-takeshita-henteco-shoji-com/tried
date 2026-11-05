"""#135 の結果を、まとめて正解の図面と比べる。

モデルごと・課題ごとに check_change.py を当て、表と JSON に残す。
C-4-1 は図面を変えないのが正解なので、図面を保存したかどうかと、元の図面との差を見る。

使い方: uv run --with ezdxf --with shapely python check_all_135.py [結果の日付フォルダ] [形式]
  形式は dxf(既定)か mcp(#134 の LibreCAD 経由)。結果は <フォルダ>/C-<形式>/ から読む
出力: <結果の日付フォルダ>/check-C.json(mcp のときは check-C-mcp.json)と、画面への表
"""
import json
import sys
from pathlib import Path

from check_change import LAYERS, compare
from run_eval import ISSUES, MODELS

DAY = ISSUES["135"]["day"]
BASE = ISSUES["135"]["drawings"]["C"].with_suffix(".dxf")
EXPECTED = DAY / "answer-key/expected"


def main(res, fmt="dxf"):
    rows = {}
    for model in MODELS:
        for qid in ("C-1-1", "C-2-1", "C-3-1", "C-4-1"):
            d = res / f"C-{fmt}" / f"{model}__medium"
            if not (d / f"{qid}.json").exists():
                continue
            out = d / f"{qid}.dxf"
            want = BASE if qid == "C-4-1" else EXPECTED / f"{qid}.dxf"
            r = {"saved": out.exists()}
            if out.exists():
                try:
                    r.update(compare(str(out), str(want)))
                except Exception as e:  # noqa: BLE001  読めない DXF も結果として残す
                    r["error"] = f"{type(e).__name__}: {e}"
            rows[f"{model} {qid}"] = r
    (res / ("check-C.json" if fmt == "dxf" else f"check-C-{fmt}.json")).write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    print("モデル 課題 | 保存 | " + " | ".join(f"{l} 余/不" for l in LAYERS) + " | 寸法の食い違い | 寸法の過不足")
    for k, r in rows.items():
        if not r["saved"] or "error" in r:
            print(f"{k} | {'保存なし' if not r['saved'] else r['error'][:60]}")
            continue
        g = " | ".join(f"{r['geometry'][l]['extra_mm']}/{r['geometry'][l]['missing_mm']}" for l in LAYERS)
        bad = ";".join(f"{d['text']}≠{d['measurement']}" + (f"(画面 {d['shown']})" if d["shown"] else "")
                       for d in r["dims_inconsistent"])
        print(f"{k} | 保存 | {g} | {bad or '-'} | +{r['dims_extra']} -{r['dims_missing']}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DAY / "results/2026-11-02",
         sys.argv[2] if len(sys.argv) > 2 else "dxf")
