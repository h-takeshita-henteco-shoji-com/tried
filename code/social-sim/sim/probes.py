"""くせの測定の部品。同じ判断を、条件を少しずつ変えて聞き、答えのずれを数える。

- 協力しすぎ: 1回目の拠出の平均、全額を入れた割合
- 言い回しへの敏感さ: neutral と paraphrase(中身は同じ、言い方だけ違う)の差
- 教科書の再演: neutral と named(実験の名前を明かす)の差。理由の中に実験名が出るか
- 人物像の効き目: 人物像あり(students)となし(none)の、答えのばらつきの差
- 選択肢の順番: 罰の段で、同じ相手を並べる順だけを変えたときの差
- 費用: 1回あたりの利用料
"""
import re
from concurrent.futures import ThreadPoolExecutor
from statistics import mean

from .games.public_goods import CONTRIBUTE_SCHEMA, punish_schema
from .persona import describe, entropy

TEXTBOOK = re.compile(r"公共財|フリーライ|ただ乗り|囚人のジレンマ|Fehr|ゲーム理論|ナッシュ|社会的ジレンマ")


def first_round(llm, run, people, spec, prompts, variant, cfg, workers=8):
    """全員に、履歴のない1回目の拠出だけを聞く。"""
    def one(p):
        system = prompts["system"].format(persona=describe(p, spec))
        prompt = prompts[variant].format(n=cfg.group_size, endowment=cfg.endowment, mpcr=cfg.mpcr,
                                         rounds=cfg.rounds, round=1, history="(まだありません)")
        reply = llm.ask(system, prompt, CONTRIBUTE_SCHEMA)
        run.call(p["id"], system, prompt, reply, tag=f"first:{variant}")
        return reply

    with ThreadPoolExecutor(workers) as ex:
        replies = list(ex.map(one, people))
    xs = [r.output["contribution"] for r in replies]
    e = cfg.endowment
    return {
        "variant": variant,
        "n": len(xs),
        "mean_share": round(mean(xs) / e, 3),
        "full_share": round(sum(x == e for x in xs) / len(xs), 3),
        "zero_share": round(sum(x == 0 for x in xs) / len(xs), 3),
        "entropy": entropy(xs),
        "textbook_mentions": round(sum(bool(TEXTBOOK.search(r.output["reason"]))
                                       for r in replies) / len(xs), 3),
        "values": xs,
        "cost_usd": round(sum(r.cost_usd for r in replies), 4),
        "sec_mean": round(mean(r.seconds for r in replies), 1),
    }


def punish_order(llm, run, people, spec, prompts, cfg, mine=15, others=(20, 10, 0), workers=8):
    """同じ3人(拠出 20・10・0)を、並べる順だけ変えて見せる。低い人にどれだけ罰が向くかを比べる。"""
    orders = {"low_first": sorted(others), "low_last": sorted(others, reverse=True)}
    labels = ["A", "B", "C"]
    base = cfg.endowment - mine + (mine + sum(others)) * cfg.mpcr
    result = {}
    for name, order in orders.items():
        table = "\n".join(f"- {lab}: グループの口座に {c} ポイント入れた" for lab, c in zip(labels, order))
        prompt = prompts["punish"].format(round=1, mine=mine, table=table, max=cfg.punish_max,
                                          cost=cfg.punish_cost, impact=cfg.punish_impact,
                                          payoff=base)

        def one(p, prompt=prompt):
            system = prompts["system"].format(persona=describe(p, spec))
            reply = llm.ask(system, prompt, punish_schema(labels, cfg.punish_max))
            run.call(p["id"], system, prompt, reply, tag=f"punish_order:{name}")
            return reply

        with ThreadPoolExecutor(workers) as ex:
            replies = list(ex.map(one, people))
        by_contrib = {c: round(mean(r.output[lab] for r in replies), 2)
                      for lab, c in zip(labels, order)}
        result[name] = {
            "points_by_contribution": by_contrib,
            "points_on_label_A": round(mean(r.output["A"] for r in replies), 2),
            "cost_usd": round(sum(r.cost_usd for r in replies), 4),
        }
    return result
