"""AIが1回目にちょうど半分(10)を入れる理由を、条件を1つずつ変えて確かめる(#172 追加検証F)。

使い方: python why10.py --llm claude:claude-haiku-5-5 [--n 24] [--only base,e30]
同じ24人(students の人物像、seed 1)に、履歴のない1回目の拠出だけを聞く。
罰なし・同じ相手の条件。変えるのは、手元の量・戻りの率・付け足す1文・答え方だけ。
"""
import argparse
import json
import os
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from statistics import mean, pstdev

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.games.public_goods import Config, CONTRIBUTE_SCHEMA, rules_extra  # noqa: E402
from sim.llm import backend  # noqa: E402
from sim.persona import describe, generate, load_spec  # noqa: E402
from sim.record import Run  # noqa: E402

INFO = "参考までに、以前この実験に参加した人たちは、1回目に平均{v}ポイントを入れました。\n"
PRIVATE = ("誰が何ポイント入れたかは、ほかの参加者にも実験者にも分かりません。"
           "記録されるのはグループの合計だけです。\n")
CALC_SCHEMA = {
    "type": "object",
    "properties": {
        "calc": {"type": "string"},
        "contribution": {"type": "integer", "minimum": 0, "maximum": 30},
        "reason": {"type": "string"},
    },
    "required": ["calc", "contribution", "reason"],
}
CALC_NOTE = ("\n答える前に、自分の稼ぎをいちばん多くするには何ポイント入れればよいかを計算し、"
             "calc に書いてください。そのうえで、実際に入れる量を決めてください。")

# 名前: (手元, 戻りの率, 付け足す1文, 計算させるか)
CONDS = {
    "base": (20, 0.4, "", False),
    "e30": (30, 0.4, "", False),
    "e10": (10, 0.4, "", False),
    "m0.3": (20, 0.3, "", False),
    "m0.7": (20, 0.7, "", False),
    "m0.9": (20, 0.9, "", False),
    "info4": (20, 0.4, INFO.format(v=4), False),
    "info16": (20, 0.4, INFO.format(v=16), False),
    "private": (20, 0.4, PRIVATE, False),
    "calc": (20, 0.4, "", True),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--llm", default="dummy:0")
    ap.add_argument("--n", type=int, default=24)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--personas", default="students")
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default=os.path.join(HERE, "runs"))
    a = ap.parse_args()
    llm = backend(a.llm)
    paths = {k: os.path.join(HERE, "prompts", "pgg", f) for k, f in
             (("system", "system.md"), ("contribute", "contribute.neutral.md"))}
    prompts = {k: open(p, encoding="utf-8").read() for k, p in paths.items()}
    spec = load_spec(os.path.join(HERE, "personas", f"{a.personas}.json"))
    people = generate(spec, a.n, a.seed)
    names = a.only.split(",") if a.only else list(CONDS)
    run = Run(a.out, "why10", {"conds": {k: CONDS[k] for k in names}, "n": a.n, "seed": a.seed,
                               "personas": a.personas, "game": asdict(Config())},
              llm, list(paths.values()))
    out = {}
    for name in names:
        e, mpcr, extra, calc = CONDS[name]
        cfg = Config(endowment=e, mpcr=mpcr)

        def one(p):
            system = prompts["system"].format(persona=describe(p, spec))
            prompt = prompts["contribute"].format(
                n=cfg.group_size, endowment=e, mpcr=mpcr, rounds=cfg.rounds, round=1,
                history="(まだありません)", rules_extra=rules_extra(cfg) + extra)
            schema = CONTRIBUTE_SCHEMA
            if calc:
                prompt += CALC_NOTE
                schema = CALC_SCHEMA
            reply = llm.ask(system, prompt, schema)
            run.call(p["id"], system, prompt, reply, tag=f"why10:{name}")
            return reply.output

        with ThreadPoolExecutor(12) as ex:
            outs = list(ex.map(one, people))
        xs = [min(max(o["contribution"], 0), e) for o in outs]
        out[name] = {"endowment": e, "mpcr": mpcr, "mean": round(mean(xs), 2),
                     "share": round(mean(xs) / e, 3), "sd": round(pstdev(xs), 2),
                     "half_share": round(sum(x * 2 == e for x in xs) / len(xs), 3),
                     "zero": sum(x == 0 for x in xs), "full": sum(x == e for x in xs),
                     "counts": dict(sorted(Counter(xs).items()))}
        print(name, json.dumps(out[name], ensure_ascii=False), flush=True)
    run.finish(out)
    print(run.dir)
    print(f"calls={run.calls} cost_usd={run.cost:.4f}")


if __name__ == "__main__":
    main()
