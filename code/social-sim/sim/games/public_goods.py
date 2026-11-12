"""ルールを動かす部品(公共財ゲーム)。拠出の配分と罰の計算はプログラムで行う。

子01(#169)で Fehr & Gächter(2000)を再現する。既定の設定は論文に合わせてある。
- 罰の費用: 1人に付ける点数ごとに PUNISH_COST_TABLE(10点で30)
- 罰の効き目: 受けた点数1点ごとに第1段の利得を10%減らす。10点で打ち切り
- 組み方: partner(毎回同じ相手)と stranger(毎回組み替え)
子00(#168)の試運転で使った、1点につき一定の費用と効き目の罰は punish_rule="flat" で残す。
"""
import math
import random
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

PUNISH_COST_TABLE = [0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30]   # 論文の表2

CONTRIBUTE_SCHEMA = {
    "type": "object",
    "properties": {
        "contribution": {"type": "integer", "minimum": 0, "maximum": 20},
        "reason": {"type": "string"},
    },
    "required": ["contribution", "reason"],
}


DIST_NOTE = ("\n0から{e}のそれぞれを入れる確率を、合計がちょうど100になる整数で答えてください(p0〜p{e})。"
             "実際に入れる量は、この確率に従ってくじで決まります。")


BELIEF_NOTE = ("\nあわせて、今回ほかの人が平均で何ポイント入れると思うかを expect(0〜{e}の整数)で答えてください。"
               "次の回の自分に残したいことを、note に60字以内で書いてください。")


def add_belief(schema, endowment):
    s = {"type": "object", "properties": dict(schema["properties"]), "required": list(schema["required"])}
    s["properties"]["expect"] = {"type": "integer", "minimum": 0, "maximum": endowment}
    s["properties"]["note"] = {"type": "string"}
    s["required"] += ["expect", "note"]
    return s


def dist_schema(endowment):
    props = {f"p{k}": {"type": "integer", "minimum": 0, "maximum": 100} for k in range(endowment + 1)}
    props["reason"] = {"type": "string"}
    return {"type": "object", "properties": props, "required": list(props)}


def sample_from(output, endowment, rng):
    """確率の答えを正規化し、くじで拠出を1つ選ぶ。合計が0なら一様に選ぶ。"""
    w = [max(0, output.get(f"p{k}", 0)) for k in range(endowment + 1)]
    if sum(w) == 0:
        w = [1] * (endowment + 1)
    return rng.choices(range(endowment + 1), weights=w)[0], sum(w)


def sample_at(output, endowment, u):
    """確率の答えを累積し、0〜1の位置 u に当たる量を返す(人ごとに位置を固定するとき用)。"""
    w = [max(0, output.get(f"p{k}", 0)) for k in range(endowment + 1)]
    if sum(w) == 0:
        w = [1] * (endowment + 1)
    total, acc = sum(w), 0
    for k, x in enumerate(w):
        acc += x
        if u <= acc / total:
            return k, total
    return endowment, total


def punish_schema(labels, max_points):
    props = {lab: {"type": "integer", "minimum": 0, "maximum": max_points} for lab in labels}
    props["reason"] = {"type": "string"}
    return {"type": "object", "properties": props, "required": list(props)}


def cost_table_text():
    return " / ".join(f"{p}点:{c}" for p, c in enumerate(PUNISH_COST_TABLE))


@dataclass
class Config:
    group_size: int = 4
    endowment: int = 20
    mpcr: float = 0.4          # 共同の財布に1入れたとき、1人に返る量
    rounds: int = 10
    punishment: bool = False
    punish_rule: str = "fg2000"  # "fg2000"(論文どおり)か "flat"(子00の試運転)
    punish_max: int = 10       # 1人に付けられる罰の上限
    punish_cost: int = 1       # flat のとき: 罰1点を付ける人が払う量
    punish_impact: int = 3     # flat のとき: 罰1点で相手が減る量
    matching: str = "partner"  # "partner"(毎回同じ相手)か "stranger"(毎回組み替え)
    shuffle_order: bool = True  # 罰の段で、他の人を並べる順をラウンドごとに混ぜる
    memory_reasons: bool = False  # 過去の回の結果に、自分が書いた拠出の理由も添える(#172 検証5)
    sample_dist: bool = False  # 拠出を確率で答えさせ、プログラムがくじで決める(#172 追加検証)
    belief_state: bool = False  # 毎回、見込みと自分へのメモを答えさせ、次の回に引き継ぐ(#172 追加検証E)
    dist_rho: float = 0.0      # sample_dist のとき、くじの位置の人ごとの固定度合い。0 は毎回独立、1 は毎回同じ位置
    bots: int = 0              # 毎回20を入れ、減点は付けない参加者の数(#172 原因の切り分け)。人の番号 0, 4, 8, … に置く
    bot_punish: bool = False   # 固定の参加者も減点を付ける。ほかの人の平均より少ない人に、差1につき0.2点(rule_model.py と同じ式)


def payoffs(contribs, cfg):
    pot = sum(contribs) * cfg.mpcr
    return [round(cfg.endowment - c + pot, 2) for c in contribs]


def apply_punishment(base, points, cfg):
    """points[i][j] は i が j に付けた罰。"""
    n = len(base)
    out = []
    for j in range(n):
        given = [points[j][k] for k in range(n) if k != j]
        received = sum(points[i][j] for i in range(n) if i != j)
        if cfg.punish_rule == "fg2000":
            cost = sum(PUNISH_COST_TABLE[p] for p in given)
            out.append(round(base[j] * (1 - min(received, 10) / 10) - cost, 2))
        else:
            out.append(round(base[j] - sum(given) * cfg.punish_cost - received * cfg.punish_impact, 2))
    return out


def rules_extra(cfg):
    """拠出の問いに足す説明。組み方と、罰の段があることを先に知らせる(論文の参加者も知っていた)。"""
    lines = []
    if cfg.matching == "partner":
        lines.append(f"グループの顔ぶれは、{cfg.rounds}回を通して変わりません。")
    else:
        lines.append("グループの顔ぶれは、毎回くじで入れ替わります。同じ人とまた組むこともあります。")
    if cfg.punishment:
        if cfg.punish_rule == "fg2000":
            lines.append("毎回、全員が入れたポイントを見たあとで、ほかの人に「減点」を付ける段があります。"
                         "減点1点につき、付けられた人のその回の稼ぎが10%減ります(10点で0)。"
                         "減点を付ける人も、点数に応じてポイントを払います。")
        else:
            lines.append("毎回、全員が入れたポイントを見たあとで、ほかの人に「減点」を付ける段があります。")
    return "\n" + "\n".join(lines) + "\n"


class Session:
    """1回の実験(論文では24人)。組み方に従って毎回グループを作り、全員に同時に聞く。"""

    def __init__(self, members, llm, prompts, cfg, run, seed, workers=12):
        self.members = members      # [(persona, persona_text)]
        self.llm = llm
        self.p = prompts            # {"system", "contribute", "punish"} の本文
        self.cfg = cfg
        self.run = run
        self.rng = random.Random(seed)
        self.seed = seed
        self.workers = workers
        self.history = [[] for _ in members]   # 各人に見せる過去のラウンド
        self.state = [None for _ in members]   # belief_state のとき、前の回の (見込み, メモ)
        n = len(members)
        assert n % cfg.group_size == 0, "人数がグループの大きさで割り切れない"
        self.fixed = [list(range(g, g + cfg.group_size)) for g in range(0, n, cfg.group_size)]
        self.bots = {k * cfg.group_size for k in range(cfg.bots)}   # partner では、前から bots 組に1人ずつ

    def _ask(self, i, prompt, schema, tag):
        system = self.p["system"].format(persona=self.members[i][1])
        reply = self.llm.ask(system, prompt, schema)
        self.run.call(self.members[i][0]["id"], system, prompt, reply, tag)
        return reply.output

    def _history_text(self, i):
        if not self.history[i]:
            return "(まだありません)"
        text = "\n".join(self.history[i])
        if self.cfg.belief_state and self.state[i]:
            exp, note = self.state[i]
            note = " ".join(note.split())[:80]
            text += (f"\n\n前の回に、あなたは「ほかの人は平均{exp}ポイントくらい入れる」と見込んでいた。"
                     f"\n前の回のあなたが、自分に残したメモ: {note}")
        return text

    def _groups(self):
        if self.cfg.matching == "partner":
            return self.fixed
        idx = list(range(len(self.members)))
        self.rng.shuffle(idx)
        k = self.cfg.group_size
        return [idx[g:g + k] for g in range(0, len(idx), k)]

    def _map(self, fn, items):
        with ThreadPoolExecutor(self.workers) as ex:
            return list(ex.map(fn, items))

    def play_round(self, r):
        cfg = self.cfg
        groups = self._groups()
        where = {i: (g, pos) for g, mem in enumerate(groups) for pos, i in enumerate(mem)}
        extra = rules_extra(cfg)

        def contribute(i):
            if i in self.bots:
                return {"contribution": cfg.endowment, "reason": "(固定の参加者: 毎回全額)"}
            prompt = self.p["contribute"].format(
                n=cfg.group_size, endowment=cfg.endowment, mpcr=cfg.mpcr, rounds=cfg.rounds,
                round=r, history=self._history_text(i), rules_extra=extra)
            schema = dist_schema(cfg.endowment) if cfg.sample_dist else CONTRIBUTE_SCHEMA
            if cfg.sample_dist:
                prompt += DIST_NOTE.format(e=cfg.endowment)
            if cfg.belief_state:
                prompt += BELIEF_NOTE.format(e=cfg.endowment)
                schema = add_belief(schema, cfg.endowment)
            out = dict(self._ask(i, prompt, schema, f"g{where[i][0]}r{r}:contribute"))
            if not cfg.sample_dist:
                return out
            # くじはスレッドの順に左右されないよう、seed・人・回から決める
            rng = random.Random(f"{self.seed}-{i}-{r}")
            if cfg.dist_rho <= 0:
                out["contribution"], out["dist_total"] = sample_from(out, cfg.endowment, rng)
                return out
            # 人ごとに決めた位置 z_i と、回ごとのゆらぎを混ぜる(正規分布で混ぜてから0〜1に戻す)
            z_i = random.Random(f"{self.seed}-z-{i}").gauss(0, 1)
            rho = min(cfg.dist_rho, 1.0)
            z = rho * z_i + math.sqrt(1 - rho * rho) * rng.gauss(0, 1)
            u = 0.5 * (1 + math.erf(z / math.sqrt(2)))
            out["contribution"], out["dist_total"] = sample_at(out, cfg.endowment, u)
            out["u"] = round(u, 3)
            return out

        outs = self._map(contribute, range(len(self.members)))
        contribs = [[outs[i]["contribution"] for i in mem] for mem in groups]
        bases = [payoffs(c, cfg) for c in contribs]
        k = cfg.group_size
        points = [[[0] * k for _ in range(k)] for _ in groups]
        orders = [None] * len(groups)
        if cfg.punishment:
            points, orders = self._punish_stage(r, groups, contribs, bases)
        for g, mem in enumerate(groups):
            final = apply_punishment(bases[g], points[g], cfg)
            self.run.event({"group": g, "round": r, "members": [self.members[i][0]["id"] for i in mem],
                            "contribs": contribs[g], "base": bases[g], "points": points[g],
                            "final": final, "reasons": [outs[i]["reason"] for i in mem],
                            "punish_orders": orders[g],
                            "expects": [outs[i].get("expect") for i in mem] if cfg.belief_state else None})
            for pos, i in enumerate(mem):
                others = ", ".join(str(c) for q, c in enumerate(contribs[g]) if q != pos)
                line = (f"第{r}回: あなたは{contribs[g][pos]}を入れ、ほかの人は {others} を入れた。"
                        f"あなたの稼ぎは{final[pos]:g}になった。")
                if cfg.punishment:
                    recv = sum(points[g][q][pos] for q in range(k) if q != pos)
                    line += f" あなたが受けた減点は{recv}点だった。"
                if cfg.memory_reasons:
                    why = " ".join(outs[i]["reason"].split())
                    line += f"\n  (このときのあなたの考え: {why[:150]})"
                self.history[i].append(line)
                if cfg.belief_state:
                    self.state[i] = (outs[i]["expect"], outs[i]["note"])

    def _punish_stage(self, r, groups, contribs, bases):
        cfg = self.cfg
        k = cfg.group_size
        points = [[[0] * k for _ in range(k)] for _ in groups]
        # 並び順はスレッドに入る前に決める。seed が同じなら同じ順になるように
        orders = []
        for _ in groups:
            per = []
            for pos in range(k):
                others = [q for q in range(k) if q != pos]
                if cfg.shuffle_order:
                    self.rng.shuffle(others)
                per.append(others)
            orders.append(per)   # 誰にどのラベル(A・B・C)を見せたか。記録に残す
        jobs = [(g, pos) for g in range(len(groups)) for pos in range(k)]

        def one(job):
            g, pos = job
            others = orders[g][pos]
            labels = [chr(ord("A") + idx) for idx in range(len(others))]
            if groups[g][pos] in self.bots:
                if not cfg.bot_punish:
                    return   # 固定の参加者は減点を付けない
                c = contribs[g]
                for q in others:
                    avg = sum(c[t] for t in range(k) if t != q) / (k - 1)
                    gap = avg - c[q]
                    points[g][pos][q] = min(round(0.2 * gap), cfg.punish_max) if gap > 1 else 0
                return

            table = "\n".join(f"- {lab}: グループの口座に {contribs[g][q]} ポイント入れた"
                              for lab, q in zip(labels, others))
            prompt = self.p["punish"].format(
                round=r, mine=contribs[g][pos], table=table, max=cfg.punish_max,
                cost=cfg.punish_cost, impact=cfg.punish_impact, payoff=bases[g][pos],
                cost_table=cost_table_text())
            out = self._ask(groups[g][pos], prompt, punish_schema(labels, cfg.punish_max),
                            f"g{g}r{r}:punish")
            for lab, q in zip(labels, others):
                points[g][pos][q] = out[lab]

        self._map(one, jobs)
        return points, orders

    def play(self):
        for r in range(1, self.cfg.rounds + 1):
            self.play_round(r)
            print(f"  round {r} done, calls={self.run.calls} cost={self.run.cost:.4f}", flush=True)
