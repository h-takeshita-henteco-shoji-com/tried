"""再生画面(main3d.gd)の場面の並びを再現して、録画の中の各場面の始まりの秒を出す。
動画の切り出し(へんロボの解説動画)に使う。main3d.gd の _build_steps を変えたら、ここも合わせる。

使い方: python viewer/step_times.py viewer/data/replay.json [場面の名前 ...]
"""
import json
import sys

STEP_LEN = {"title": 5.0, "intro": 1.6, "contrib": 2.6, "contrib_talk": 7.0, "distribute": 2.6, "punish": 2.4,
            "punish_talk": 7.0, "result": 2.4, "end": 6.0, "chat_intro": 2.2, "chat": 4.0, "talk": 2.6,
            "talk_talk": 6.0, "talk_punish": 3.4, "plan": 8.0, "punish_plan": 8.0}
THINK = ["plan", "punish_plan", "contrib_talk", "punish_talk", "talk_talk"]


def think_text(rd, step, i):
    if step == "plan":
        pl = rd["plans"][i]
        return "入れると思う量: %s\n%s" % ("、".join(f"{k} {int(v)}" for k, v in pl["expect"].items()), pl["plan"])
    if step == "punish_plan":
        return rd["punish_plans"][i]
    key = {"contrib_talk": "contribute_reasons", "punish_talk": "punish_reasons", "talk_talk": "talk_reasons"}[step]
    return rd[key][i]


def steps(data):
    out, s = [], 0.0
    names = ["intro", "contrib", "contrib_talk", "distribute"] + (["punish", "punish_talk"] if data["game"]["punishment"] else []) + ["result"]
    out.append(("title", -1, -1, s, STEP_LEN["title"])); s += STEP_LEN["title"]
    for r, rd in enumerate(data["rounds"]):
        pre = []
        chat = rd.get("chat") or []
        if chat:
            pre.append(("chat_intro", -1, None))
            for k, c in enumerate(chat):
                pre.append(("chat", c["who"], min(max(2.2 + len(c["text"]) * 0.055, 3.2), 7.5)))
        if rd.get("talk") is not None:
            pre += [("talk", -1, None), ("talk_talk", -1, None)] + ([("talk_punish", -1, None)] if rd.get("talk_points") is not None else [])
        if rd.get("plans") is not None:
            pre.append(("plan", -1, None))
        for n in names:
            items = [(n, -1, None)]
            if n == "intro":
                items += pre
            if n == "punish" and rd.get("punish_plans") is not None:
                items = [("punish_plan", -1, None), (n, -1, None)]
            if rd.get("plans") is not None and n in ("contrib_talk", "punish_talk"):
                continue
            for name, who, ln in items:
                if name in THINK:
                    for w in range(4):
                        tl = min(max(2.5 + len(think_text(rd, name, w)) * 0.035, 4.0), 7.5)
                        out.append((name, r, w, s, tl)); s += tl
                    continue
                ln = ln if ln is not None else STEP_LEN[name]
                out.append((name, r, who, s, ln)); s += ln
    out.append(("end", -1, -1, s, STEP_LEN["end"]))
    return out


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    want = set(sys.argv[2:])
    for name, r, who, start, ln in steps(data):
        if not want or name in want:
            print(f"{start:8.2f} {ln:5.2f}  第{r + 1}回 {name} {'ABCD'[who] if who >= 0 else ''}")
    print("合計", round(steps(data)[-1][3] + STEP_LEN["end"], 2), "秒")
