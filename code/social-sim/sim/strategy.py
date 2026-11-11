"""協力の型を測る部品。Fischbacher, Gächter & Fehr(2001)の戦略法をAIに解かせる。

ほかの人の平均拠出が 0〜20 のそれぞれの場合に、自分が何点入れるかを答えてもらい、
答え方の形から型に分ける。
- free_rider: どの場合も0
- conditional: ほかの人の平均が増えるほど、自分も増やす(順位相関 0.5 以上)
- hump: 途中まで増やし、その先で減らす
- other: どれにも当たらない
"""
from concurrent.futures import ThreadPoolExecutor
from statistics import mean

from .persona import describe


def schema(endowment):
    props = {"unconditional": {"type": "integer", "minimum": 0, "maximum": endowment}}
    for k in range(endowment + 1):
        props[f"avg{k}"] = {"type": "integer", "minimum": 0, "maximum": endowment}
    props["reason"] = {"type": "string"}
    return {"type": "object", "properties": props, "required": list(props)}


def _ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(xs, ys):
    rx, ry = _ranks(xs), _ranks(ys)
    mx, my = mean(rx), mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def classify(table):
    n = len(table)
    if max(table) == 0:
        return "free_rider"
    peak = max(range(n), key=lambda i: table[i])
    if 2 <= peak <= n - 3 and table[peak] - table[0] >= 3 and table[peak] - table[-1] >= 3:
        return "hump"
    if spearman(list(range(n)), table) >= 0.5:
        return "conditional"
    return "other"


def measure(llm, run, people, spec, prompts, cfg, workers=12, tag="strategy"):
    others = cfg.group_size - 1
    prompt = prompts["strategy"].format(n=cfg.group_size, endowment=cfg.endowment, mpcr=cfg.mpcr,
                                        others=others)
    sch = schema(cfg.endowment)

    def one(p):
        system = prompts["system"].format(persona=describe(p, spec))
        reply = llm.ask(system, prompt, sch)
        run.call(p["id"], system, prompt, reply, tag=tag)
        return reply

    with ThreadPoolExecutor(workers) as ex:
        replies = list(ex.map(one, people))
    rows = []
    for p, r in zip(people, replies):
        table = [r.output[f"avg{k}"] for k in range(cfg.endowment + 1)]
        rows.append({"id": p["id"], "unconditional": r.output["unconditional"], "table": table,
                     "type": classify(table), "slope_to_diag": round(mean(
                         t - k for k, t in enumerate(table)), 2)})
    n = len(rows)
    types = {t: round(sum(x["type"] == t for x in rows) / n, 3)
             for t in ("conditional", "free_rider", "hump", "other")}
    return {"n": n, "types": types,
            "unconditional_mean": round(mean(x["unconditional"] for x in rows), 2),
            "unconditional_values": sorted(x["unconditional"] for x in rows),
            "mean_table": [round(mean(x["table"][k] for x in rows), 2) for k in range(cfg.endowment + 1)],
            "rows": rows, "cost_usd": round(sum(r.cost_usd for r in replies), 4)}


BELIEF_SCHEMA = {
    "type": "object",
    "properties": {
        "expect": {"type": "integer", "minimum": 0, "maximum": 20},
        "contribution": {"type": "integer", "minimum": 0, "maximum": 20},
        "reason": {"type": "string"},
    },
    "required": ["expect", "contribution", "reason"],
}


def beliefs(llm, run, people, spec, prompts, cfg, workers=12, tag="belief"):
    """1回きりのゲームで、ほかの人の平均の予想と、自分の拠出を一緒に聞く。"""
    prompt = prompts["belief"].format(n=cfg.group_size, endowment=cfg.endowment, mpcr=cfg.mpcr,
                                      others=cfg.group_size - 1)

    def one(p):
        system = prompts["system"].format(persona=describe(p, spec))
        reply = llm.ask(system, prompt, BELIEF_SCHEMA)
        run.call(p["id"], system, prompt, reply, tag=tag)
        return reply

    with ThreadPoolExecutor(workers) as ex:
        replies = list(ex.map(one, people))
    exp = [r.output["expect"] for r in replies]
    con = [r.output["contribution"] for r in replies]
    rows = [{"id": p["id"], **{k: p[k] for k in p if k == "belief"}, "expect": e, "contribution": c}
            for p, e, c in zip(people, exp, con)]
    return {"n": len(rows), "expect_mean": round(mean(exp), 2), "expect_values": sorted(exp),
            "contribution_mean": round(mean(con), 2), "contribution_values": sorted(con),
            "corr_spearman": round(spearman(exp, con), 3), "rows": rows,
            "cost_usd": round(sum(r.cost_usd for r in replies), 4)}
