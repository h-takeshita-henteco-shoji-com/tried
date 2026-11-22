"""社会実験のシミュレーションを動かす入り口。

使い方:
  python run.py game  --llm dummy:0 --groups 6 --rounds 10 [--punishment] [--matching stranger] [--variant neutral]
  python run.py holdout --llm dummy:0 --proposer buyer --periods 10 [--delay] --groups 10
  python run.py siting --llm dummy:0 --n 30 [--no-comp]
  python run.py probe --llm claude:claude-haiku-5-5 --n 12
出力: runs/<日時>-<名前>/ に manifest.json・calls.jsonl・events.jsonl
"""
import argparse
import json
import os
import random
import sys
from dataclasses import asdict
from statistics import mean

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.games import holdout, siting  # noqa: E402
from sim.games.public_goods import Config, Session  # noqa: E402
from sim.llm import backend  # noqa: E402
from sim.persona import describe, diversity, generate, load_spec  # noqa: E402
from sim.probes import first_round, punish_order  # noqa: E402
from sim.record import Run  # noqa: E402
from sim.strategy import beliefs, measure  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPTS = os.path.join(HERE, "prompts", "pgg")
VARIANTS = ["neutral", "paraphrase", "named"]


def load_prompts(variant="neutral", rule="fg2000", identified=False):
    punish = {"fg2000": "punish.fg2000.md", "bpp": "punish.bpp.md"}.get(rule, "punish.neutral.md")
    if identified and rule == "bpp":
        punish = "punish.bpp.identified.md"
    files = {"system": "system.md", "punish": punish, "strategy": "strategy.md", "belief": "belief.md",
             "chat": "chat.md", "talk": "talk.md", "talk_punish": "talk_punish.md",
             "plan": "plan.md", "punish_plan": "punish_plan.md"}
    files.update({v: f"contribute.{v}.md" for v in VARIANTS})
    paths = {k: os.path.join(PROMPTS, f) for k, f in files.items()}
    texts = {k: open(p, encoding="utf-8").read() for k, p in paths.items()}
    texts["contribute"] = texts[variant]
    return texts, paths


def cmd_game(a):
    llm = backend(a.llm)
    chat = tuple(int(x) for x in a.chat.split(",")) if a.chat else ()
    cfg = Config(rounds=a.rounds, punishment=a.punishment, matching=a.matching, punish_rule=a.rule,
                 memory_reasons=a.memory, sample_dist=a.dist, belief_state=a.belief, bots=a.bots, bot_punish=a.bot_punish, dist_rho=a.rho,
                 endowment=a.endowment, mpcr=a.mpcr, group_size=a.size,
                 chat_rounds=chat, chat_turns=a.chat_turns, cheap_talk=a.cheap_talk,
                 identified=a.identified, plan_phases=a.plan)
    if a.plan and not a.identified:
        raise SystemExit("--plan は --identified と一緒に使う")
    if a.plan and a.belief:
        raise SystemExit("--plan は --belief の代わり(作戦と印象を次の回に渡す)なので、一緒には使わない")
    if a.identified and a.matching != "partner":
        raise SystemExit("--identified は、毎回同じ相手(partner)のときだけ使える")
    if a.rule == "bpp":   # 1人への減点の上限は、相手の稼ぎの最大(全員が全額を入れたとき)
        cfg.punish_max = int(cfg.endowment + cfg.mpcr * cfg.endowment * cfg.group_size)
    spec = load_spec(os.path.join(HERE, "personas", f"{a.personas}.json"))
    people = generate(spec, cfg.group_size * a.groups, a.seed, distinct=a.distinct, block=cfg.group_size,
                      fixed={"trait": a.traits.split(",")} if a.traits else None)
    if a.traits and len(a.traits.split(",")) != cfg.group_size:
        raise SystemExit("--traits は組の人数と同じ数だけ書く")
    prompts, paths = load_prompts(a.variant, a.rule, a.identified)
    if a.motive:   # 性格に関係なく全員に持たせる動機を、システムの指示の末尾に足す
        mpath = os.path.join(HERE, "prompts", "pgg", "motives", f"{a.motive}.md")
        prompts["system"] = prompts["system"].rstrip("\n") + "\n" + open(mpath, encoding="utf-8").read()
        paths["motive"] = mpath
    used = [paths["system"], paths[a.variant]] + ([paths["punish"]] if a.punishment else []) \
        + ([paths["chat"]] if chat else []) + ([paths["talk"]] if a.cheap_talk else []) \
        + ([paths["talk_punish"]] if a.cheap_talk and a.punishment else []) \
        + ([paths["plan"], paths["punish_plan"]] if a.plan else []) + ([paths["motive"]] if a.motive else [])
    config = {"game": asdict(cfg), "groups": a.groups, "seed": a.seed,
              "personas": a.personas, "variant": a.variant, "distinct": a.distinct, "traits": a.traits, "motive": a.motive}
    name = f"game-{a.matching}-{'p' if a.punishment else 'n'}" + ("-mem" if a.memory else "") + ("-dist" if a.dist else "") + (f"-rho{a.rho:g}" if a.rho else "") + ("-belief" if a.belief else "") + (f"-hybrid{a.hybrid:g}" if a.hybrid is not None else "") + ("p" if a.hybrid_proposer else "") + (f"-bots{a.bots}" if a.bots else "") + ("p" if a.bot_punish else "") \
        + (f"-{a.rule}" if a.rule != "fg2000" else "") + ("-chat" if chat else "") + ("-talk" if a.cheap_talk else "") + ("-id" if a.identified else "") + ("-plan" if a.plan else "") + (f"-uniq{a.distinct}" if a.distinct else "") + ("-traits" if a.traits else "") + (f"-m{a.motive}" if a.motive else "")
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


def cmd_holdout(a):
    """Cadigan ほか(2009)のホールドアウトの交渉(#181)。1回の実行で1条件を回す。"""
    llm = backend(a.llm)
    cfg = holdout.Config(proposer=a.proposer, periods=a.periods, delay=a.delay, reason_first=a.order == "reason",
                          remind=a.remind, memory=a.memory, emotion=a.emotion, damp=a.damp, belief=a.belief or a.hybrid is not None, hybrid_mu=a.hybrid, hybrid_proposer=a.hybrid_proposer, buyer_bot=a.buyer_bot is not None,
                          bot_step=a.buyer_bot or 0)
    if a.damp is not None and a.hybrid_proposer:
        raise SystemExit("--damp と --hybrid-proposer は一緒に使わない")
    if a.hybrid_proposer and a.hybrid is None:
        raise SystemExit("--hybrid-proposer は --hybrid と一緒に使う")
    if a.buyer_bot is not None and a.proposer != "buyer":
        raise SystemExit("--buyer-bot は --proposer buyer のときだけ使う")
    if a.delay and a.periods == 1:
        raise SystemExit("--delay は --periods 2 以上のときだけ使う")
    prompts, paths = holdout.load_prompts(os.path.join(HERE, "prompts"))
    if a.motive:   # #173 と同じく、全員に同じ動機の一文を、決まりの文の末尾に足す
        paths["motive"] = os.path.join(HERE, "prompts", "holdout", "motives", f"{a.motive}.md")
        prompts["rules"] = prompts["rules"].rstrip("\n") + "\n" + open(paths["motive"], encoding="utf-8").read()
    spec = load_spec(os.path.join(HERE, "personas", f"{a.personas}.json"))
    people = generate(spec, 3 * a.groups, a.seed)
    mem = [(p, describe(p, spec)) for p in people]
    groups = [mem[3 * g:3 * g + 3] for g in range(a.groups)]
    name = f"holdout-{a.proposer}-t{a.periods}" + ("-delay" if a.delay else "") + f"-{a.personas}" \
        + ("-answerfirst" if a.order == "answer" else "") + (f"-m{a.motive}" if a.motive else "") + ("-remind" if a.remind else "") \
        + ("-memory" if a.memory else "") + ("-belief" if a.belief else "") + ("-emotion" if a.emotion else "") + (f"-hybrid{a.hybrid:g}" if a.hybrid is not None else "") + ("p" if a.hybrid_proposer else "") + (f"-damp{a.damp:g}" if a.damp is not None else "") + (f"-bot{a.buyer_bot}" if a.buyer_bot is not None else "")
    config = {"game": asdict(cfg), "groups": a.groups, "seed": a.seed, "personas": a.personas, "motive": a.motive}
    run = Run(a.out, name, config, llm, list(paths.values()))
    run.manifest["people"] = people
    results, summary = holdout.play_all(groups, llm, prompts, cfg, run, workers=a.workers)
    run.finish(summary)
    print(run.dir)
    print(json.dumps(summary, ensure_ascii=False))
    print(f"calls={run.calls} cost_usd={run.cost:.4f}")


def cmd_siting(a):
    """Frey と Oberholzer-Gee(1997)の、処分場の受け入れの面接調査(#170)。"""
    llm = backend(a.llm)
    cfg = siting.Config(compensation=not a.no_comp, show_prev=not a.fresh, form=a.form, appraise=a.appraise, own_motive=a.own_motive)
    prompts, paths = siting.load_prompts(os.path.join(HERE, "prompts"))
    spec = load_spec(os.path.join(HERE, "personas", f"{a.personas}.json"))
    rng = random.Random(a.seed)
    people = [siting.fix_person(p, rng) for p in generate(spec, a.n, a.seed)]
    name = f"siting-{a.personas}" + ("-nocomp" if a.no_comp else "") + ("-fresh" if a.fresh else "") + (f"-{a.form}" if a.form != "cash" else "") + ("-appraise" if a.appraise else "") + ("-own" if a.own_motive else "")
    run = Run(a.out, name, {"game": asdict(cfg), "n": a.n, "seed": a.seed, "personas": a.personas}, llm, list(paths.values()))
    run.manifest["people"] = people
    desc2 = None
    if a.own_motive:   # 考え方の3文を外した人物像(swiss1993 の書き方)
        base = load_spec(os.path.join(HERE, "personas", "swiss1993.json"))
        desc2 = [describe(p, base) for p in people]
    rows, summary = siting.play_all([(p, describe(p, spec)) for p in people], llm, prompts, cfg, run, a.seed, workers=a.workers, desc2=desc2)
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
    for name in ("game", "probe", "strategy", "holdout", "siting"):
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
    g.add_argument("--rule", default="fg2000", choices=["fg2000", "flat", "bpp"],
                   help="減点の方式。bpp は Bochet ほか(2006): 1点につき付けた人0.25、付けられた人1")
    g.add_argument("--endowment", type=int, default=20)
    g.add_argument("--mpcr", type=float, default=0.4)
    g.add_argument("--size", type=int, default=4, help="組の人数")
    g.add_argument("--chat", default="", help="この回の前にチャットする。例: 1,4,7")
    g.add_argument("--chat-turns", type=int, default=3, help="1回のチャットで全員が何巡話すか")
    g.add_argument("--cheap-talk", action="store_true", help="毎回、決める前に入れるかもしれない量を見せ合う")
    g.add_argument("--identified", action="store_true",
                   help="全員に最後まで同じ記号を付け、誰が誰に何点減点したかを全員に見せる(--rule bpp、毎回同じ相手のとき)")
    g.add_argument("--plan", action="store_true",
                   help="入れる前と減点の前に、作戦を考える段を挟む(--identified と一緒に)")
    g.add_argument("--distinct", default=None, help="組の中で重ならないようにする人物像の属性。例: trait(毎回同じ相手のとき)")
    g.add_argument("--traits", default=None, help="組の4人の性格を順に指定する。例: 慎重,人づきあいが好き,負けず嫌い,疑い深い")
    g.add_argument("--motive", default=None, help="全員に持たせる動機。prompts/pgg/motives/<名前>.md")
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
    h = sub.choices["holdout"]
    h.add_argument("--proposer", default="buyer", choices=["buyer", "seller"], help="値段を出す側")
    h.add_argument("--periods", type=int, default=10, help="最大の期の数。1なら1回だけ")
    h.add_argument("--delay", action="store_true", help="断られるたびに全員の稼ぎを5%%ずつ減らす")
    h.add_argument("--groups", type=int, default=10)
    h.add_argument("--personas", default="students_notrait")
    h.add_argument("--order", default="reason", choices=["reason", "answer"], help="理由と答えのどちらを先に書かせるか")
    h.add_argument("--motive", default=None, help="全員に持たせる動機。prompts/holdout/motives/<名前>.md")
    h.add_argument("--belief", action="store_true", help="受ける側に、断ったときの相手の次の値段と、その見込みを書かせる")
    h.add_argument("--damp", type=float, default=None, help="出す側の譲り幅を、AIが譲った幅のこの割合に抑える(最後の期は除く)")
    h.add_argument("--emotion", action="store_true", help="受ける側に、提示をどれくらい不公平と感じたか(0〜100)を書かせる")
    h.add_argument("--hybrid", type=float, default=None,
                   help="組み合わせ型: AIの見込みを使い、増え方がしきい値(平均このドル数)を超えたら断る。--belief を含む")
    h.add_argument("--hybrid-proposer", action="store_true", help="値段を出す側にも組み合わせ型を使う(--hybrid と一緒に)")
    h.add_argument("--memory", action="store_true", help="自分が前の期に書いた理由も渡す")
    h.add_argument("--buyer-bot", type=int, default=None, help="買い手をプログラムにする。1期目35ドル、断られるたびにこのドル数だけ上げる")
    h.add_argument("--remind", action="store_true", help="毎期、残りの期の数と、断ったときに稼ぎが減るかを知らせる")
    h.add_argument("--workers", type=int, default=6, help="同時に回す組の数")
    st = sub.choices["siting"]
    st.add_argument("--n", type=int, default=30, help="住民の人数")
    st.add_argument("--personas", default="swiss1993")
    st.add_argument("--no-comp", action="store_true", help="補償なしの問い(問1)だけ聞く")
    st.add_argument("--fresh", action="store_true", help="問2で問1の答えを見せず、別に聞く")
    st.add_argument("--form", default="cash", choices=["cash", "public", "none"], help="補償の形。public は村に同じ額の公共の設備、none は補償なしでもう一度聞く")
    st.add_argument("--appraise", action="store_true", help="問2で、補償の受け止めを0〜100で書かせる")
    st.add_argument("--own-motive", action="store_true", help="問2では考え方の3文を外し、問1の自分の理由だけを渡す")
    st.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    {"game": cmd_game, "probe": cmd_probe, "strategy": cmd_strategy, "holdout": cmd_holdout, "siting": cmd_siting}[a.cmd](a)
