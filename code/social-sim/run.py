"""社会実験のシミュレーションを動かす入り口。

使い方:
  python run.py game  --llm dummy:0 --groups 1 --rounds 3 [--punishment] [--variant neutral]
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
from sim.games.public_goods import Config, Group  # noqa: E402
from sim.llm import backend  # noqa: E402
from sim.persona import describe, diversity, generate, load_spec  # noqa: E402
from sim.probes import first_round, punish_order  # noqa: E402
from sim.record import Run  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPTS = os.path.join(HERE, "prompts", "pgg")
VARIANTS = ["neutral", "paraphrase", "named"]


def load_prompts(variant="neutral"):
    files = {"system": "system.md", "punish": "punish.neutral.md"}
    files.update({v: f"contribute.{v}.md" for v in VARIANTS})
    paths = {k: os.path.join(PROMPTS, f) for k, f in files.items()}
    texts = {k: open(p, encoding="utf-8").read() for k, p in paths.items()}
    texts["contribute"] = texts[variant]
    return texts, paths


def cmd_game(a):
    llm = backend(a.llm)
    cfg = Config(rounds=a.rounds, punishment=a.punishment)
    spec = load_spec(os.path.join(HERE, "personas", f"{a.personas}.json"))
    people = generate(spec, cfg.group_size * a.groups, a.seed)
    prompts, paths = load_prompts(a.variant)
    used = [paths["system"], paths[a.variant]] + ([paths["punish"]] if a.punishment else [])
    config = {"game": asdict(cfg), "groups": a.groups, "seed": a.seed,
              "personas": a.personas, "variant": a.variant}
    run = Run(a.out, f"game-{'p' if a.punishment else 'n'}", config, llm, used)
    run.manifest["people"] = people
    run.manifest["diversity"] = diversity(people, spec)
    groups = []
    for g in range(a.groups):
        mem = [(p, describe(p, spec)) for p in people[g * cfg.group_size:(g + 1) * cfg.group_size]]
        grp = Group(g, mem, llm, prompts, cfg, run, seed=f"{a.seed}-{g}")
        grp.play()
        groups.append(grp)
    rows = [json.loads(line) for line in open(os.path.join(run.dir, "events.jsonl"))]
    by_round = {}
    for row in rows:
        by_round.setdefault(row["round"], []).extend(row["contribs"])
    summary = {"mean_share_by_round": {r: round(mean(v) / cfg.endowment, 3)
                                       for r, v in sorted(by_round.items())}}
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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("game", "probe"):
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
    sub.choices["probe"].add_argument("--n", type=int, default=12)
    a = ap.parse_args()
    {"game": cmd_game, "probe": cmd_probe}[a.cmd](a)
