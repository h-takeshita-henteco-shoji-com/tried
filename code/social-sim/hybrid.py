"""LLMと規則型の組み合わせ(#172)。LLMには人物像から各人の性質だけを答えさせ、拠出は式で計算する。

使い方: python hybrid.py --llm claude:claude-haiku-5-5 [--persona-seeds 1-5] [--reps 4]
1. 人物像(students)ごとに1回だけ、LLMに3つを聞く
   - 実験の前の見込み(ほかの人が平均で何ポイント入れると思うか)
   - 前の回のほかの人の平均が 0・5・10・15・20 だったときに、次の回に入れる量
   - 前の回に減点を3点・6点受けたとき(ほかの人の平均は10)に、次の回に入れる量
     --punish-ctx below では、自分が4しか入れなかった場面で聞く(実際のゲームで罰を受けるのは、こちらの場面)
2. 答えを rule_model.py の式に入れる。見込みの更新・罰の付け方・ゆらぎは規則型と同じ
   - 罰への反応 = 減点を受けたときの量と、同じ場面で受けなかったときの量の差を、1点あたりに直した平均
3. 人物像の組(persona seed)ごとに、ゆらぎの乱数を変えて reps 回ずつ、4条件を回す
比べる相手は rule_model.py(型を決まった割合で乱数で割り振る)。式は同じなので、差は性質の出どころだけ。
"""
import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rule_model import parse_seeds, play  # noqa: E402
from sim.games.public_goods import Config  # noqa: E402
from sim.llm import backend  # noqa: E402
from sim.persona import describe, generate, load_spec  # noqa: E402
from sim.record import Run  # noqa: E402

XS = [0, 5, 10, 15, 20]
PROMPT = """これから、{n}人のグループで次の実験を{rounds}回くり返します。グループの顔ぶれは変わりません。

毎回、あなたは{e}ポイントを受け取ります。
そのうち何ポイントを「グループの口座」に入れるかを、0から{e}の整数で決めます。
入れなかった分は、そのままあなたの手元に残ります。
グループの口座に集まった合計は、1ポイントにつき{mpcr}ポイントずつ、全員にそれぞれ配られます。
入れたかどうかに関係なく、全員が同じだけ受け取ります。
毎回の結果のあとで、ほかの人がそれぞれ何ポイント入れたかが分かります。
ポイントは、実験の後でお金に換えて支払われます。

実験の進め方を決めるため、前もって次の3つを答えてください。

1. 実験が始まる前の予想: ほかの人は、1回目に平均で何ポイント入れると思いますか(expect)
2. 前の回に、ほかの{others}人が入れたポイントの平均が次の値だったとき、あなたは次の回に何ポイント入れますか
   - 平均0のとき(next0)、平均5のとき(next5)、平均10のとき(next10)、平均15のとき(next15)、平均20のとき(next20)
3. この実験に、ほかの人に「減点」を付ける段があったとします。減点1点につき、付けられた人のその回の稼ぎが10%減ります。
   {punish_ctx}あなたは次の回に何ポイント入れますか
   - 減点を受けなかったとき(punished0)、3点受けたとき(punished3)、6点受けたとき(punished6)
"""
PUNISH_CTX = {
    "even": "前の回に、ほかの人の平均は10ポイントで、あなたは合わせて次の点数の減点を受けました。",
    "below": "前の回に、あなたは4ポイント、ほかの人は平均10ポイントを入れました。そのあと、あなたは合わせて次の点数の減点を受けました。",
}


def schema(e):
    keys = ["expect"] + [f"next{x}" for x in XS] + ["punished0", "punished3", "punished6"]
    props = {k: {"type": "integer", "minimum": 0, "maximum": e} for k in keys}
    props["reason"] = {"type": "string"}
    return {"type": "object", "properties": props, "required": list(props)}


def to_params(p, o):
    table = [o[f"next{x}"] for x in XS]
    base10 = o["punished0"]   # 同じ場面で減点がなかったときの量を基準にする
    deter = ((o["punished3"] - base10) / 3 + (o["punished6"] - base10) / 6) / 2
    return {"id": p["id"], "belief0": o["expect"], "xs": XS, "table": table,
            "deter": round(deter, 3), "raw": {k: v for k, v in o.items() if k != "reason"}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--llm", default="dummy:0")
    ap.add_argument("--persona-seeds", default="1-5")
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument("--personas", default="students")
    ap.add_argument("--punish-ctx", default="even", choices=list(PUNISH_CTX),
                    help="減点を受けた場面: even=平均どおり入れたのに受けた / below=平均より少なく入れて受けた")
    ap.add_argument("--out", default=os.path.join(HERE, "runs", "hybrid"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    llm = backend(a.llm)
    cfg = Config()
    spec = load_spec(os.path.join(HERE, "personas", f"{a.personas}.json"))
    system_t = open(os.path.join(HERE, "prompts", "pgg", "system.md"), encoding="utf-8").read()
    prompt = PROMPT.format(n=cfg.group_size, rounds=cfg.rounds, e=cfg.endowment, mpcr=cfg.mpcr,
                           others=cfg.group_size - 1, punish_ctx=PUNISH_CTX[a.punish_ctx])
    label = "hybrid" if a.punish_ctx == "even" else f"hybrid-{a.punish_ctx}"
    seeds = parse_seeds(a.persona_seeds)
    ask_run = Run(a.out, f"{label}-ask", {"persona_seeds": seeds, "personas": a.personas,
                                        "prompt": prompt}, llm,
                  [os.path.join(HERE, "prompts", "pgg", "system.md")])
    all_params = {}
    for ps in seeds:
        people = generate(spec, 24, ps)

        def one(p):
            system = system_t.format(persona=describe(p, spec))
            reply = llm.ask(system, prompt, schema(cfg.endowment))
            ask_run.call(p["id"], system, prompt, reply, tag=f"hybrid:s{ps}")
            return to_params(p, reply.output)

        with ThreadPoolExecutor(8) as ex:
            all_params[ps] = list(ex.map(one, people))
        print(f"persona seed {ps}: asked, cost={ask_run.cost:.4f}", flush=True)
    ask_run.finish({"params": all_params})
    for ps in seeds:
        for rep in range(a.reps):
            seed = ps * 100 + rep
            for matching in ("partner", "stranger"):
                for punishment in (False, True):
                    play(Config(matching=matching, punishment=punishment), seed, a.out,
                         llm_params=all_params[ps], label=label)
    print(ask_run.dir)
    print(f"calls={ask_run.calls} cost_usd={ask_run.cost:.4f}")


if __name__ == "__main__":
    main()
