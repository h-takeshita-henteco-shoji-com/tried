"""1回のゲームの記録(runs/<日時>-game-*)を、Godot の再生画面が読む replay.json にまとめる。

使い方: python viewer/export_replay.py runs/<日時>-game-p [viewer/data/replay.json] [--group N]
- --group: 再生する組(毎回同じ相手の条件だけ。既定は0)
- プログラムで動く参加者(--bots)は、名前はそのままに、人物像の欄で「プログラム」と示す
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


BOT_PERSONA = "プログラムで動く参加者。毎回20を入れる。"
BOT_PUNISH = "プログラムで動く参加者。毎回20を入れ、平均より少ない人に減点を付ける。"


def main(run_dir, out, group=0):
    m = json.load(open(os.path.join(run_dir, "manifest.json"), encoding="utf-8"))
    events = [json.loads(line) for line in open(os.path.join(run_dir, "events.jsonl"), encoding="utf-8")]
    calls = [json.loads(line) for line in open(os.path.join(run_dir, "calls.jsonl"), encoding="utf-8")]
    spec = load_spec(os.path.join(os.path.dirname(HERE), "personas", f"{m['config']['personas']}.json"))
    game = m["config"]["game"]
    size = game["group_size"]
    if group and game["matching"] != "partner":
        raise SystemExit("組を選べるのは、毎回同じ相手の条件だけ")
    first = next(e for e in events if e["group"] == group)
    by_id = {p["id"]: p for p in m["people"]}
    ids = first["members"]
    people = [by_id[pid] for pid in ids]
    bots = {f"p{k * size:03d}" for k in range(game.get("bots", 0))}
    bot_text = BOT_PUNISH if game.get("bot_punish") else BOT_PERSONA
    punish = {(c["who"], c["tag"]): c["output"] for c in calls if c["tag"] and c["tag"].endswith(":punish")}
    rounds = []
    for e in events:
        if e["group"] != group:
            continue
        rounds.append({
            "round": e["round"],
            "contribs": e["contribs"],
            "base": e["base"],
            "points": e["points"],
            "final": e["final"],
            "contribute_reasons": ["(プログラム)毎回20を入れる。" if pid in bots else short(r)
                                   for pid, r in zip(ids, e["reasons"])],
            "punish_reasons": ["(プログラム)平均より少ない人に、差に応じて減点を付ける。" if pid in bots and game.get("bot_punish")
                               else short(relabel(punish.get((pid, f"g{group}r{e['round']}:punish"), {}).get("reason", ""),
                                             (e.get("punish_orders") or [None] * size)[i]))
                               for i, pid in enumerate(ids)],
        })
    replay = {
        "title": "公共財ゲーム(罰あり)" if game["punishment"] else "公共財ゲーム",
        "llm": m["llm"],
        "llm_version": m["llm_version"],
        "run": os.path.basename(run_dir.rstrip("/")),
        "game": game,
        "group": group,
        "subtitle": (f"AIが演じる{size - len(bots & set(ids))}人と、プログラムの参加者{len(bots & set(ids))}人が、"
                     f"{len(rounds)}回くり返す") if bots & set(ids) else f"AIが演じる{size}人の参加者が、{len(rounds)}回くり返す",
        "members": [{"name": f"参加者{i + 1}", "persona": bot_text if p["id"] in bots else describe(p, spec)}
                    for i, p in enumerate(people)],
        "rounds": rounds,
    }
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(replay, f, ensure_ascii=False, indent=1)
    print(out, len(rounds), "rounds")


if __name__ == "__main__":
    args = sys.argv[1:]
    g = 0
    if "--group" in args:
        k = args.index("--group")
        g = int(args[k + 1])
        del args[k:k + 2]
    main(args[0], args[1] if len(args) > 1 else os.path.join(HERE, "data", "replay.json"), g)
