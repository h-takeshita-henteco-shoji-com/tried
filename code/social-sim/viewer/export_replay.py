"""1回のゲームの記録(runs/<日時>-game-*)を、Godot の再生画面が読む replay.json にまとめる。

使い方: python viewer/export_replay.py runs/<日時>-game-p [viewer/data/replay.json]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from sim.persona import describe, load_spec  # noqa: E402

MAX_CHARS = 150   # 吹き出しに出す理由の長さ。長い分は「…」で切る


def short(text):
    text = " ".join(text.split())
    return text if len(text) <= MAX_CHARS else text[:MAX_CHARS - 1] + "…"


def relabel(text, order):
    """罰の理由の中の A・B・C(人ごとに混ぜたラベル)を、参加者の名前に置き換える。"""
    if not order:
        return text
    names = {chr(ord("A") + i): f"参加者{k + 1}" for i, k in enumerate(order)}
    text = re.sub(r"(?<![A-Za-z])([A-C])(?:さん)?(?![A-Za-z])", lambda m: names.get(m.group(1), m.group(0)), text)
    return text


def main(run_dir, out):
    m = json.load(open(os.path.join(run_dir, "manifest.json"), encoding="utf-8"))
    events = [json.loads(line) for line in open(os.path.join(run_dir, "events.jsonl"), encoding="utf-8")]
    calls = [json.loads(line) for line in open(os.path.join(run_dir, "calls.jsonl"), encoding="utf-8")]
    spec = load_spec(os.path.join(os.path.dirname(HERE), "personas", f"{m['config']['personas']}.json"))
    game = m["config"]["game"]
    size = game["group_size"]
    people = m["people"][:size]           # 試作では第0組だけを再生する
    ids = [p["id"] for p in people]
    punish = {(c["who"], c["tag"]): c["output"] for c in calls if c["tag"] and c["tag"].endswith(":punish")}
    rounds = []
    for e in events:
        if e["group"] != 0:
            continue
        rounds.append({
            "round": e["round"],
            "contribs": e["contribs"],
            "base": e["base"],
            "points": e["points"],
            "final": e["final"],
            "contribute_reasons": [short(r) for r in e["reasons"]],
            "punish_reasons": [short(relabel(punish.get((pid, f"g0r{e['round']}:punish"), {}).get("reason", ""),
                                             (e.get("punish_orders") or [None] * size)[i]))
                               for i, pid in enumerate(ids)],
        })
    replay = {
        "title": "公共財ゲーム(罰あり)" if game["punishment"] else "公共財ゲーム",
        "llm": m["llm"],
        "llm_version": m["llm_version"],
        "run": os.path.basename(run_dir.rstrip("/")),
        "game": game,
        "members": [{"name": f"参加者{i + 1}", "persona": describe(p, spec)} for i, p in enumerate(people)],
        "rounds": rounds,
    }
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(replay, f, ensure_ascii=False, indent=1)
    print(out, len(rounds), "rounds")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "data", "replay.json"))
