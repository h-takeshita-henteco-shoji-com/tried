"""社会実験のシミュレーションを動かす入り口。

使い方:
  python run.py game  --llm dummy:0 --groups 6 --rounds 10 [--punishment] [--matching stranger] [--variant neutral]
  python run.py probe --llm claude:claude-haiku-5-5 --n 12
出力: runs/<日時>-<名前>/ に manifest.json・calls.jsonl・events.jsonl
"""
import argparse
import json
import os
import sys
from dataclasses import asdict
from statistics import mean

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.games.public_goods import Config, Session  # noqa: E402
from sim.llm import backend  # noqa: E402
from sim.persona import describe, diversity, generate, load_spec  # noqa: E402
from sim.probes import first_round, punish_order  # noqa: E402
from sim.record import Run  # noqa: E402
from sim.strategy import beliefs, measure  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPTS = os.path.join(HERE, "prompts", "pgg")
VARIANTS = ["neutral", "paraphrase", "named"]


def load_prompts(variant="neutral", rule="fg2000"):
    files = {"system": "system.md", "punish": "punish.fg2000.md" if rule == "fg2000" else "punish.neutral.md",
             "strategy": "strategy.md", "belief": "belief.md"}
    files.update({v: f"contribute.{v}.md" for v in VARIANTS})
    paths = {k: os.path.join(PROMPTS, f) for k, f in files.items()}
    texts = {k: open(p, encoding="utf-8").read() for k, p in paths.items()}
    texts["contribute"] = texts[variant]
    return texts, paths


def cmd_game(a):
    llm = backend(a.llm)
    cfg = Config(rounds=a.rounds, punishment=a.punishment, matching=a.matching, punish_rule=a.rule,
                 memory_reasons=a.memory, sample_dist=a.dist, belief_state=a.belief, bots=a.bots, bot_punish=a.bot_punish, dist_rho=a.rho)
    spec = load_spec(os.path.join(HERE, "personas", f"{a.personas}.json"))
    people = generate(spec, cfg.group_size * a.groups, a.seed)
    prompts, paths = load_prompts(a.variant, a.rule)
    used = [paths["system"], paths[a.variant]] + ([paths["punish"]] if a.punishment else [])
    config = {"game": asdict(cfg), "groups": a.groups, "seed": a.seed,
              "personas": a.personas, "variant": a.variant}
    name = f"game-{a.matching}-{'p' if a.punishment else 'n'}" + ("-mem" if a.memory else "") + ("-dist" if a.dist else "") + (f"-rho{a.rho:g}" if a.rho else "") + ("-belief" if a.belief else "") + (f"-bots{a.bots}" if a.bots else "") + ("p" if a.bot_punish else "")
    run = Run(a.out, name, config, llm, used)
    run.manifest["people"] = people
    run.manifest["diversity"] = diversity(people, spec)
    mem = [(p, describe(p, spec)) for p in people]
    Session(mem, llm, prompts, cfg, run, seed=a.seed, workers=a.workers).play()
    rows = [json.loads(line) for line in open(os.path.join(run.dir, "events.jsonl"), encoding="utf-8")]
    by_round = {}
    for row in rows:
        by_round.setdefault(row["round"], []).extend(row["contribs"])
    summary = {"mean_by_round": {r: round(mean(v), 2) for r, v in sorted(by_round.items())}}
    run.finish(summary)
    print(run.dir)
    print(json.dumps(summary, ensure_ascii=False))
    print(f"calls={run.calls} cost_usd={run.cost:.4f}")


def cmd_probe(a):
    llm = backend(a.llm)
    cfg = Config()
    prompts, paths = load_prompts()
    out = {}
    run = Run(a.out, "probe", {"game": asdict(cfg), "n": a.n, "seed": a.seed},
              llm, list(paths.values()))
    for pset in ["students", "none"]:
        spec = load_spec(os.path.join(HERE, "personas", f"{pset}.json"))
        people = generate(spec, a.n, a.seed)
        variants = VARIANTS if pset == "students" else ["neutral"]
        for v in variants:
            out[f"{pset}/{v}"] = first_round(llm, run, people, spec, prompts, v, cfg)
            print(pset, v, {k: out[f"{pset}/{v}"][k] for k in
                            ("mean_share", "full_share", "entropy", "textbook_mentions", "cost_usd")})
    spec = load_spec(os.path.join(HERE, "personas", "students.json"))
    out["punish_order"] = punish_order(llm, run, generate(spec, a.n, a.seed), spec, prompts, cfg)
    print("punish_order", json.dumps(out["punish_order"], ensure_ascii=False))
    run.finish(out)
    print(run.dir)
    print(f"calls={run.calls} cost_usd={run.cost:.4f}")


def cmd_strategy(a):
    llm = backend(a.llm)
    cfg = Config()
    prompts, paths = load_prompts()
    run = Run(a.out, "belief" if a.belief else "strategy", {"game": asdict(cfg), "n": a.n, "seed": a.seed, "personas": a.personas},
              llm, [paths["system"], paths["belief" if a.belief else "strategy"]])
    out = {}
    for pset in a.personas.split(","):
        spec = load_spec(os.path.join(HERE, "personas", f"{pset}.json"))
        people = generate(spec, a.n, a.seed)
        if a.belief:
            out[pset] = beliefs(llm, run, people, spec, prompts, cfg, tag=f"belief:{pset}")
            print(pset, {k: out[pset][k] for k in ("expect_mean", "contribution_mean", "corr_spearman")},
                  "cost", out[pset]["cost_usd"], flush=True)
            continue
        out[pset] = measure(llm, run, people, spec, prompts, cfg, tag=f"strategy:{pset}")
        print(pset, out[pset]["types"], "uncond", out[pset]["unconditional_mean"],
              "cost", out[pset]["cost_usd"], flush=True)
        print("  mean_table", out[pset]["mean_table"])
    run.finish(out)
    print(run.dir)
    print(f"calls={run.calls} cost_usd={run.cost:.4f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("game", "probe", "strategy"):
        s = sub.add_parser(name)
        s.add_argument("--llm", default="dummy:0")
        s.add_argument("--seed", type=int, default=1)
        s.add_argument("--out", default=os.path.join(HERE, "runs"))
    g = sub.choices["game"]
    g.add_argument("--groups", type=int, default=1)
    g.add_argument("--rounds", type=int, default=10)
    g.add_argument("--punishment", action="store_true")
    g.add_argument("--variant", default="neutral", choices=VARIANTS)
    g.add_argument("--personas", default="students")
    g.add_argument("--matching", default="partner", choices=["partner", "stranger"])
    g.add_argument("--rule", default="fg2000", choices=["fg2000", "flat"])
    g.add_argument("--workers", type=int, default=12)
    g.add_argument("--memory", action="store_true", help="自分が書いた拠出の理由も、過去の回として渡す")
    g.add_argument("--dist", action="store_true", help="拠出を確率で答えさせ、くじで決める")
    g.add_argument("--belief", action="store_true", help="毎回、見込みと自分へのメモを答えさせ、次の回に引き継ぐ")
    g.add_argument("--rho", type=float, default=0.0, help="--dist のとき、くじの位置を人ごとに固定する度合い(0〜1)")
    g.add_argument("--bots", type=int, default=0, help="毎回20を入れ、減点を付けない参加者の数")
    g.add_argument("--bot-punish", action="store_true", help="固定の参加者も、平均より少ない人に減点を付ける")
    sub.choices["probe"].add_argument("--n", type=int, default=12)
    sub.choices["strategy"].add_argument("--n", type=int, default=48)
    sub.choices["strategy"].add_argument("--personas", default="students,none")
    sub.choices["strategy"].add_argument("--belief", action="store_true",
                                         help="戦略法の代わりに、予想と拠出を一緒に聞く(#172 検証4)")
    a = ap.parse_args()
    {"game": cmd_game, "probe": cmd_probe, "strategy": cmd_strategy}[a.cmd](a)
