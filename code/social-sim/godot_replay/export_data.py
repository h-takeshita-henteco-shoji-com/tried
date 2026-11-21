"""#181 の記録から、Godot の再生動画に使う組を書き出す(data.json)。

使い方: python3 godot_replay/export_data.py [--hook]
各条件で、断った回数が中央値に近い組を1つずつ選ぶ(下の PICKS)。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
# (実行フォルダ, 組の番号, 見出し)。k=0.15 の出す側の決まり + 受ける側の組み合わせ型(μ=1)
PICKS = [
    ("c181damp/20261121-061235-holdout-buyer-t10-students_notrait-hybrid1-damp0.15", 3, "買い手が値段を出す・遅れの損なし"),
    ("c181damp30/20261121-061920-holdout-buyer-t10-delay-students_notrait-hybrid1-damp0.15", 1, "買い手が値段を出す・遅れの損あり"),
    ("c181damp30/20261121-062554-holdout-seller-t10-students_notrait-hybrid1-damp0.15", 14, "売り手が値段を出す・遅れの損なし"),
    ("c181damp30/20261121-063740-holdout-seller-t10-delay-students_notrait-hybrid1-damp0.15", 5, "売り手が値段を出す・遅れの損あり"),
]
HUMAN = {  # Cadigan et al. 2009 表1・表3(10期)。稼ぎは 買い手 / 売り手1人あたり
    ("buyer", False): {"rejections": 10.8, "buyer": 10.55, "seller": 9.72},
    ("buyer", True): {"rejections": 2.9, "buyer": 11.12, "seller": 7.24},
    ("seller", False): {"rejections": 11.0, "buyer": 10.43, "seller": 9.28},
    ("seller", True): {"rejections": 3.3, "buyer": 9.39, "seller": 7.80},
}


def short(text, n=58):
    """理由の最初の1文を、n文字までに縮める。"""
    first = re.split(r"(?<=。)", text or "")[0].strip()
    return first if len(first) <= n else first[: n - 1] + "…"


# 動画の冒頭用: AIだけの交渉(断るかもAIが決める)。2人の売り手が「断れば次は40ドル」と予想しながら35ドルで売った組
HOOK = [("c181/20261120-122204-holdout-buyer-t10-students_notrait-belief", 1, "AIだけの交渉(買い手が値段を出す・遅れの損なし)")]


def main():
    import sys
    hook = "--hook" in sys.argv
    scenes = []
    for folder, gid, title in (HOOK if hook else PICKS):
        d = RUNS / folder
        game = json.loads((d / "manifest.json").read_text())["config"]["game"]
        g = next(json.loads(l) for l in (d / "events.jsonl").read_text().splitlines() if json.loads(l)["group"] == gid)
        rounds = []
        for r in g["rounds"]:
            rounds.append({
                "period": r["period"],
                "offers": r["offers"],
                "accepted": r["accepted"],
                "ai_accepted": r.get("ai_accepted", r["accepted"]),
                "rejections_total": r["rejections_total"],
                "beliefs": {k: v["next_price"] for k, v in (r.get("beliefs") or {}).items()},
                "damp": {k: {"ai": v["ai"], "sent": v["sent"]} for k, v in (r.get("damp") or {}).items()},
                "reasons": {k: short(v) for k, v in r["reasons"].items()},
            })
        p, delay = game["proposer"], game["delay"]
        scenes.append({"title": title, "proposer": p, "delay": delay, "periods": game["periods"],
                       "rounds": rounds, "prices": g["prices"], "payoffs": g["payoffs"],
                       "rejections": g["rejections"], "complete": g["complete"], "human": HUMAN[(p, delay)]})
    out = Path(__file__).resolve().parent / ("data_hook.json" if hook else "data.json")
    out.write_text(json.dumps({"scenes": scenes}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(out, [len(s["rounds"]) for s in scenes])


if __name__ == "__main__":
    main()
