"""ルールを動かす部品(公共財ゲーム)。拠出の配分と罰の計算はプログラムで行う。

子01(#169)で Fehr & Gächter(2000)を再現するための試運転。
罰の費用と効き目は設定で変える。元論文の正確な値は #169 で確かめる。
"""
import random
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

CONTRIBUTE_SCHEMA = {
    "type": "object",
    "properties": {
        "contribution": {"type": "integer", "minimum": 0, "maximum": 20},
        "reason": {"type": "string"},
    },
    "required": ["contribution", "reason"],
}


def punish_schema(labels, max_points):
    props = {lab: {"type": "integer", "minimum": 0, "maximum": max_points} for lab in labels}
    props["reason"] = {"type": "string"}
    return {"type": "object", "properties": props, "required": list(props)}


@dataclass
class Config:
    group_size: int = 4
    endowment: int = 20
    mpcr: float = 0.4          # 共同の財布に1入れたとき、1人に返る量
    rounds: int = 10
    punishment: bool = False
    punish_max: int = 10       # 1人に付けられる罰の上限
    punish_cost: int = 1       # 罰1点を付ける人が払う量
    punish_impact: int = 3     # 罰1点で相手が減る量
    shuffle_order: bool = True  # 罰の段で、他の人を並べる順をラウンドごとに混ぜる


def payoffs(contribs, cfg):
    pot = sum(contribs) * cfg.mpcr
    return [round(cfg.endowment - c + pot, 2) for c in contribs]


def apply_punishment(base, points, cfg):
    """points[i][j] は i が j に付けた罰。"""
    n = len(base)
    out = []
    for j in range(n):
        given = sum(points[j][k] for k in range(n) if k != j) * cfg.punish_cost
        received = sum(points[i][j] for i in range(n) if i != j) * cfg.punish_impact
        out.append(round(base[j] - given - received, 2))
    return out


class Group:
    def __init__(self, gid, members, llm, prompts, cfg, run, seed):
        self.gid = gid
        self.members = members      # [(persona, persona_text)]
        self.llm = llm
        self.p = prompts            # {"system", "contribute", "punish"} の本文
        self.cfg = cfg
        self.run = run
        self.rng = random.Random(seed)
        self.history = [[] for _ in members]   # 各人に見せる過去のラウンド

    def _ask(self, i, prompt, schema, tag):
        system = self.p["system"].format(persona=self.members[i][1])
        reply = self.llm.ask(system, prompt, schema)
        self.run.call(self.members[i][0]["id"], system, prompt, reply, tag)
        return reply.output

    def _history_text(self, i):
        if not self.history[i]:
            return "(まだありません)"
        return "\n".join(self.history[i])

    def play_round(self, r):
        cfg = self.cfg
        n = len(self.members)
        prompts = [self.p["contribute"].format(
            n=n, endowment=cfg.endowment, mpcr=cfg.mpcr, rounds=cfg.rounds, round=r,
            history=self._history_text(i)) for i in range(n)]
        with ThreadPoolExecutor(n) as ex:
            outs = list(ex.map(lambda i: self._ask(i, prompts[i], CONTRIBUTE_SCHEMA,
                                                   f"g{self.gid}r{r}:contribute"), range(n)))
        contribs = [o["contribution"] for o in outs]
        base = payoffs(contribs, cfg)
        points = [[0] * n for _ in range(n)]
        self.last_orders = None
        if cfg.punishment:
            points = self._punish_stage(r, contribs, base)
        final = apply_punishment(base, points, cfg)
        self.run.event({"group": self.gid, "round": r, "contribs": contribs,
                        "base": base, "points": points, "final": final,
                        "reasons": [o["reason"] for o in outs],
                        "punish_orders": self.last_orders})
        for i in range(n):
            others = ", ".join(str(c) for k, c in enumerate(contribs) if k != i)
            line = (f"第{r}回: あなたは{contribs[i]}を入れ、ほかの人は {others} を入れた。"
                    f"あなたの手元は{final[i]:g}になった。")
            if cfg.punishment:
                recv = sum(points[k][i] for k in range(n) if k != i)
                line += f" あなたが受けた罰は{recv}点だった。"
            self.history[i].append(line)
        return contribs, final

    def _punish_stage(self, r, contribs, base):
        cfg = self.cfg
        n = len(self.members)
        points = [[0] * n for _ in range(n)]
        # 並び順はスレッドに入る前に決める。seed が同じなら同じ順になるように
        orders = []
        for i in range(n):
            others = [k for k in range(n) if k != i]
            if cfg.shuffle_order:
                self.rng.shuffle(others)
            orders.append(others)
        self.last_orders = orders   # 誰にどのラベル(A・B・C)を見せたか。記録に残す

        def one(i):
            others = orders[i]
            labels = [chr(ord("A") + idx) for idx in range(len(others))]
            table = "\n".join(f"- {lab}: グループの口座に {contribs[k]} ポイント入れた"
                              for lab, k in zip(labels, others))
            prompt = self.p["punish"].format(
                round=r, mine=contribs[i], table=table, max=cfg.punish_max,
                cost=cfg.punish_cost, impact=cfg.punish_impact, payoff=base[i])
            out = self._ask(i, prompt, punish_schema(labels, cfg.punish_max),
                            f"g{self.gid}r{r}:punish")
            for lab, k in zip(labels, others):
                points[i][k] = out[lab]

        with ThreadPoolExecutor(n) as ex:
            list(ex.map(one, range(n)))
        return points

    def play(self):
        for r in range(1, self.cfg.rounds + 1):
            self.play_round(r)
