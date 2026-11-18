"""ルールを動かす部品(公共財ゲーム)。拠出の配分と罰の計算はプログラムで行う。

子01(#169)で Fehr & Gächter(2000)を再現する。既定の設定は論文に合わせてある。
- 罰の費用: 1人に付ける点数ごとに PUNISH_COST_TABLE(10点で30)
- 罰の効き目: 受けた点数1点ごとに第1段の利得を10%減らす。10点で打ち切り
- 組み方: partner(毎回同じ相手)と stranger(毎回組み替え)
子00(#168)の試運転で使った、1点につき一定の費用と効き目の罰は punish_rule="flat" で残す。

#173 で Bochet, Page & Putterman(2006)の「話し合いと減点の公共財ゲーム」を足した。
- punish_rule="bpp": 減点1点につき、付けた人が0.25払い、付けられた人が1減る。
  1人への減点は相手のその回の稼ぎまで、減点に使う額は自分のその回の稼ぎまで。稼ぎは0未満にしない
- chat_rounds: この回の前に、組の中でチャットする(論文は1・4・7回目の前)。1人ずつ順に chat_turns 巡話す
- cheap_talk: 毎回、決める前に「入れるかもしれない量」を見せ合う。拘束力はない。
  減点ありなら、見せ合ったあとに「付けるかもしれない減点」も見せ合う
"""
import json
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


def contribute_schema(endowment):
    s = json.loads(json.dumps(CONTRIBUTE_SCHEMA))
    s["properties"]["contribution"]["maximum"] = endowment
    return s


CHAT_SCHEMA = {
    "type": "object",
    "properties": {"message": {"type": "string"}},
    "required": ["message"],
}

TALK_SCHEMA_REASON = {"type": "string"}
CHAT_MAX_CHARS = 120   # 1回の発言の長さ。長い分は切る


DIST_NOTE = ("\n0から{e}のそれぞれを入れる確率を、合計がちょうど100になる整数で答えてください(p0〜p{e})。"
             "実際に入れる量は、この確率に従ってくじで決まります。")


BELIEF_NOTE = ("\nあわせて、今回ほかの人が平均で何ポイント入れると思うかを expect(0〜{e}の整数)で答えてください。"
               "次の回の自分に残したいことを、note に60字以内で書いてください。")


# 名前つき(#173 案B)のときのメモ。感じたことも書かせる
FEEL_NOTE = ("\nあわせて、今回ほかの人が平均で何ポイント入れると思うかを expect(0〜{e}の整数)で答えてください。"
             "これまでのやり取りで感じたこと(ほかの人への気持ちも含めて)と、次の回の自分に残したいことを、"
             "note に80字以内で書いてください。")


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


def plan_schema(letters, endowment, max_points):
    """作戦を考える段(入れる前)。相手ごとの印象と予想を先に、作戦を最後に書かせる。"""
    props = {}
    for L in letters:
        props[f"{L}_impression"] = {"type": "string"}
        props[f"{L}_contrib"] = {"type": "integer", "minimum": 0, "maximum": endowment}
        props[f"{L}_punish_me"] = {"type": "integer", "minimum": 0, "maximum": max_points}
    for key in ("situation", "feeling", "plan"):
        props[key] = {"type": "string"}
    return {"type": "object", "properties": props, "required": list(props)}


def punish_plan_schema(letters):
    """減点の作戦を考える段(全員の量が出たあと)。"""
    props = {}
    for L in letters:
        props[f"{L}_judge"] = {"type": "string"}
        props[f"{L}_impression"] = {"type": "string"}
    for key in ("retaliation", "plan"):
        props[key] = {"type": "string"}
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
    bpp_cost: float = 0.25     # bpp のとき: 減点1点を付ける人が払う量
    chat_rounds: tuple = ()    # この回の前にチャットする(#173、論文は (1, 4, 7))
    chat_turns: int = 3        # 1回のチャットで、全員が何巡話すか
    cheap_talk: bool = False   # 毎回、決める前に入れるかもしれない量を見せ合う(#173)
    plan_phases: bool = False  # 入れる前と減点の前に、作戦を考える段を挟む(#173。identified のときだけ)
    identified: bool = False   # 全員に最後まで同じ記号(A〜D)を付け、誰が誰に何点減点したかを全員に見せる(#173 案B)


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
        elif cfg.punish_rule == "bpp":
            out.append(round(max(0.0, base[j] - sum(given) * cfg.bpp_cost - received), 2))
        else:
            out.append(round(base[j] - sum(given) * cfg.punish_cost - received * cfg.punish_impact, 2))
    return out


def clamp_bpp(points, base, cfg):
    """論文の2つの上限を当てる。1人への減点は相手のその回の稼ぎまで、使う額は自分の稼ぎまで。"""
    n = len(base)
    for i in range(n):
        for j in range(n):
            if i != j:
                points[i][j] = max(0, min(points[i][j], int(base[j])))
        spend = sum(points[i][j] for j in range(n) if j != i) * cfg.bpp_cost
        if spend > base[i]:
            ratio = base[i] / spend
            for j in range(n):
                if j != i:
                    points[i][j] = int(points[i][j] * ratio)
    return points


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
        elif cfg.punish_rule == "bpp":
            lines.append("毎回、全員が入れたポイントを見たあとで、ほかの人に「減点」を付ける段があります。"
                         f"減点1点につき、付けた人は{cfg.bpp_cost:g}ポイントを払い、付けられた人は1ポイント減ります。")
        else:
            lines.append("毎回、全員が入れたポイントを見たあとで、ほかの人に「減点」を付ける段があります。")
    if cfg.chat_rounds:
        when = "・".join(f"第{r}回" for r in cfg.chat_rounds)
        lines.append(f"{when}の前に、グループの中でチャットで話し合う時間があります。")
    if cfg.cheap_talk:
        lines.append("毎回、決める前に、入れるかもしれないポイントを見せ合う段があります。言った量に縛られません。")
    if cfg.identified:
        lines.append("参加者には、最後まで同じ記号(A、B、C…)が付いています。"
                     "誰が何ポイント入れたか、誰が誰に何点の減点を付けたかは、毎回全員に知らされます。")
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
        self.chats = [[] for _ in members]     # 各人が参加したチャットの記録(文章)
        self.state = [None for _ in members]   # belief_state のとき、前の回の (見込み, メモ)
        self.totals = [0.0 for _ in members]   # ここまでの稼ぎの合計
        self.carry = [None for _ in members]   # plan_phases のとき、前の回の終わりの {印象, 作戦}
        n = len(members)
        assert n % cfg.group_size == 0, "人数がグループの大きさで割り切れない"
        self.fixed = [list(range(g, g + cfg.group_size)) for g in range(0, n, cfg.group_size)]
        self.bots = {k * cfg.group_size for k in range(cfg.bots)}   # partner では、前から bots 組に1人ずつ

    def _ask(self, i, prompt, schema, tag):
        system = self.p["system"].format(persona=self.members[i][1])
        reply = self.llm.ask(system, prompt, schema)
        self.run.call(self.members[i][0]["id"], system, prompt, reply, tag)
        return reply.output

    def _letter(self, pos):
        return chr(ord("A") + pos)

    def _history_text(self, i):
        me = f"あなたの記号は「{self._letter(i % self.cfg.group_size)}」です。\n" if self.cfg.identified else ""
        if not self.history[i]:
            return me + "(まだありません)"
        text = me + "\n".join(self.history[i])
        if self.cfg.identified:
            k = self.cfg.group_size
            g0 = i - i % k
            tot = "、".join(f"{self._letter(q)} {self.totals[g0 + q]:g}" + ("(あなた)" if g0 + q == i else "")
                           for q in range(k))
            text += f"\nここまでの稼ぎの合計: {tot}"
        if self.cfg.plan_phases and self.carry[i]:
            imp = "\n".join(f"- {L}: {t}" for L, t in self.carry[i]["impressions"].items())
            text += (f"\n\n前の回の終わりに、あなたがほかの人に持っていた印象:\n{imp}"
                     f"\n前の回に、あなたが立てた作戦: {self.carry[i]['plan']}")
        if self.cfg.belief_state and self.state[i]:
            exp, note = self.state[i]
            note = " ".join(note.split())[:100]
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

    def _base_fields(self, i, r, extra):
        cfg = self.cfg
        return dict(n=cfg.group_size, endowment=cfg.endowment, mpcr=cfg.mpcr, rounds=cfg.rounds,
                    round=r, history=self._history_text(i), rules_extra=extra)

    def _chat_text(self, i):
        if not self.chats[i]:
            return ""
        return "\n\nこれまでのグループの話し合い:\n" + "\n\n".join(self.chats[i])

    def _chat_stage(self, r, groups, extra):
        """組ごとに、1人ずつ順に発言する。組どうしは並行に進める。"""
        cfg = self.cfg
        k = cfg.group_size

        def one_group(g):
            mem = groups[g]
            order = list(range(k))
            random.Random(f"{self.seed}-chat-{g}-{r}").shuffle(order)
            letters = {pos: chr(ord("A") + idx) for idx, pos in enumerate(order)}
            if cfg.identified:
                letters = {pos: self._letter(pos) for pos in range(k)}
            lines = []
            for turn in range(1, cfg.chat_turns + 1):
                for pos in order:
                    i = mem[pos]
                    transcript = "\n".join(f"{x['label']}: {x['text']}" for x in lines) or "(まだ誰も発言していません)"
                    prompt = self.p["chat"].format(
                        **self._base_fields(i, r, extra), me=letters[pos], turns=cfg.chat_turns, turn=turn,
                        transcript=transcript, max=CHAT_MAX_CHARS, past=self._chat_text(i))
                    out = self._ask(i, prompt, CHAT_SCHEMA, f"g{g}r{r}:chat{turn}")
                    text = " ".join(out["message"].split())[:CHAT_MAX_CHARS]
                    lines.append({"pos": pos, "label": letters[pos], "turn": turn, "text": text})
            body = "\n".join(f"{x['label']}: {x['text']}" for x in lines)
            for pos, i in enumerate(mem):
                self.chats[i].append(f"(第{r}回の前。あなたは{letters[pos]})\n{body}")
            return lines

        with ThreadPoolExecutor(min(self.workers, len(groups))) as ex:
            return list(ex.map(one_group, range(len(groups))))

    def _talk_stage(self, r, groups, extra):
        """入れるかもしれない量を見せ合う。減点ありなら、付けるかもしれない減点も見せ合う。"""
        cfg = self.cfg
        k = cfg.group_size
        jobs = [(g, pos) for g in range(len(groups)) for pos in range(k)]
        said = [[0] * k for _ in groups]
        why = [[""] * k for _ in groups]
        schema = {"type": "object", "properties": {
            "possible": {"type": "integer", "minimum": 0, "maximum": cfg.endowment}, "reason": TALK_SCHEMA_REASON},
            "required": ["possible", "reason"]}

        def say(job):
            g, pos = job
            i = groups[g][pos]
            prompt = self.p["talk"].format(**self._base_fields(i, r, extra), past=self._chat_text(i))
            out = self._ask(i, prompt, schema, f"g{g}r{r}:talk")
            said[g][pos] = out["possible"]
            why[g][pos] = out["reason"]

        self._map(say, jobs)
        maybe = [[[0] * k for _ in range(k)] for _ in groups]
        if cfg.punishment:
            def threat(job):
                g, pos = job
                i = groups[g][pos]
                others = [q for q in range(k) if q != pos]
                labels = [chr(ord("A") + idx) for idx in range(len(others))]
                table = "\n".join(f"- {lab}: {said[g][q]} ポイント入れるかもしれないと言った"
                                  for lab, q in zip(labels, others))
                prompt = self.p["talk_punish"].format(
                    round=r, mine=said[g][pos], table=table, max=cfg.punish_max, cost=cfg.bpp_cost)
                out = self._ask(i, prompt, punish_schema(labels, cfg.punish_max), f"g{g}r{r}:talk_punish")
                for lab, q in zip(labels, others):
                    maybe[g][pos][q] = out[lab]

            self._map(threat, jobs)
        return said, why, maybe

    def _talk_text(self, g, pos, said, maybe):
        k = self.cfg.group_size
        others = ", ".join(str(said[g][q]) for q in range(k) if q != pos)
        text = (f"\n\n今回、決める前に見せ合った「入れるかもしれない量」: あなたは{said[g][pos]}、"
                f"ほかの人は {others}(言った量に縛られません)")
        if self.cfg.punishment:
            recv = sum(maybe[g][q][pos] for q in range(k) if q != pos)
            text += f"\nほかの人が、あなたに付けるかもしれないと言った減点: 合計{recv}点"
        return text

    def play_round(self, r):
        cfg = self.cfg
        groups = self._groups()
        where = {i: (g, pos) for g, mem in enumerate(groups) for pos, i in enumerate(mem)}
        extra = rules_extra(cfg)
        chat = self._chat_stage(r, groups, extra) if r in cfg.chat_rounds else None
        talk = self._talk_stage(r, groups, extra) if cfg.cheap_talk else None
        plans = self._plan_stage(r, groups, extra, where) if cfg.plan_phases else None

        def contribute(i):
            if i in self.bots:
                return {"contribution": cfg.endowment, "reason": "(固定の参加者: 毎回全額)"}
            history = self._history_text(i) + self._chat_text(i)
            if plans:
                history += self._plan_text(i, plans[i])
            if talk:
                g, pos = where[i]
                history += self._talk_text(g, pos, talk[0], talk[2])
            prompt = self.p["contribute"].format(
                n=cfg.group_size, endowment=cfg.endowment, mpcr=cfg.mpcr, rounds=cfg.rounds,
                round=r, history=history, rules_extra=extra)
            schema = dist_schema(cfg.endowment) if cfg.sample_dist else contribute_schema(cfg.endowment)
            if cfg.sample_dist:
                prompt += DIST_NOTE.format(e=cfg.endowment)
            if cfg.belief_state:
                prompt += (FEEL_NOTE if cfg.identified else BELIEF_NOTE).format(e=cfg.endowment)
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
        pplans = {}
        if cfg.punishment:
            points, orders, pplans = self._punish_stage(r, groups, contribs, bases, plans)
        for g, mem in enumerate(groups):
            final = apply_punishment(bases[g], points[g], cfg)
            for pos, i in enumerate(mem):
                self.totals[i] += final[pos]
            self.run.event({"group": g, "round": r, "members": [self.members[i][0]["id"] for i in mem],
                            "contribs": contribs[g], "base": bases[g], "points": points[g],
                            "final": final, "reasons": [outs[i]["reason"] for i in mem],
                            "punish_orders": orders[g],
                            "chat": chat[g] if chat else None,
                            "talk": talk[0][g] if talk else None,
                            "talk_reasons": talk[1][g] if talk else None,
                            "talk_points": talk[2][g] if talk and cfg.punishment else None,
                            "expects": [outs[i].get("expect") for i in mem] if cfg.belief_state else None,
                            "plans": [plans[i] for i in mem] if plans else None,
                            "punish_plans": [pplans.get(i) for i in mem] if plans else None})
            for pos, i in enumerate(mem):
                others = ", ".join(str(c) for q, c in enumerate(contribs[g]) if q != pos)
                line = (f"第{r}回: あなたは{contribs[g][pos]}を入れ、ほかの人は {others} を入れた。"
                        f"あなたの稼ぎは{final[pos]:g}になった。")
                if cfg.identified:
                    line = self._named_line(r, pos, contribs[g], points[g], final)
                elif cfg.punishment:
                    recv = sum(points[g][q][pos] for q in range(k) if q != pos)
                    line += f" あなたが受けた減点は{recv}点だった。"
                if cfg.memory_reasons:
                    why = " ".join(outs[i]["reason"].split())
                    line += f"\n  (このときのあなたの考え: {why[:150]})"
                self.history[i].append(line)
                if cfg.belief_state:
                    self.state[i] = (outs[i]["expect"], outs[i]["note"])
                if plans:
                    others = [self._letter(q) for q in range(k) if q != pos]
                    pp = pplans.get(i) or {}
                    self.carry[i] = {"impressions": {L: pp.get(f"{L}_impression") or plans[i][f"{L}_impression"]
                                                     for L in others},
                                     "plan": plans[i]["plan"]}

    def _named_line(self, r, pos, contribs, points, final):
        """記号つきの、ある回の結果。誰が誰に何点減点したかも書く。"""
        k = self.cfg.group_size
        L = self._letter
        put = "、".join(f"{L(q)} {contribs[q]}" + ("(あなた)" if q == pos else "") for q in range(k))
        line = f"第{r}回: 入れた量は {put}。"
        if self.cfg.punishment:
            pairs = [f"{L(a)}→{L(b)} {points[a][b]}点" for a in range(k) for b in range(k)
                     if a != b and points[a][b] > 0]
            line += f" 減点は {'、'.join(pairs) if pairs else 'なし'}。"
        return line + f" あなたの稼ぎは{final[pos]:g}になった。"

    def _plan_stage(self, r, groups, extra, where):
        """入れる前に、相手ごとの印象と予想、状況の見立て、感じたこと、作戦を書かせる。"""
        cfg = self.cfg
        k = cfg.group_size

        def one(i):
            g, pos = where[i]
            letters = [self._letter(q) for q in range(k) if q != pos]
            prompt = self.p["plan"].format(**self._base_fields(i, r, extra), past=self._chat_text(i),
                                           me=self._letter(pos), others="・".join(letters), max=cfg.punish_max)
            return self._ask(i, prompt, plan_schema(letters, cfg.endowment, cfg.punish_max), f"g{g}r{r}:plan")

        outs = self._map(one, range(len(self.members)))
        return {i: o for i, o in enumerate(outs)}

    def _plan_text(self, i, plan):
        k = self.cfg.group_size
        pos = i % k
        lines = [f"- {self._letter(q)}: {plan[f'{self._letter(q)}_impression']}"
                 f"(入れると予想: {plan[f'{self._letter(q)}_contrib']}、あなたへの減点の予想: {plan[f'{self._letter(q)}_punish_me']}点)"
                 for q in range(k) if q != pos]
        return ("\n\nこの回の前に、あなたが考えたこと:\nほかの人の印象と予想:\n" + "\n".join(lines)
                + f"\n状況の見立て: {plan['situation']}\n感じたこと: {plan['feeling']}\n作戦: {plan['plan']}")

    def _punish_stage(self, r, groups, contribs, bases, plans=None):
        cfg = self.cfg
        k = cfg.group_size
        points = [[[0] * k for _ in range(k)] for _ in groups]
        # 並び順はスレッドに入る前に決める。seed が同じなら同じ順になるように
        orders = []
        for _ in groups:
            per = []
            for pos in range(k):
                others = [q for q in range(k) if q != pos]
                if cfg.shuffle_order and not cfg.identified:
                    self.rng.shuffle(others)
                per.append(others)
            orders.append(per)   # 誰にどのラベル(A・B・C)を見せたか。記録に残す
        jobs = [(g, pos) for g in range(len(groups)) for pos in range(k)]
        pplans = {}

        def one(job):
            g, pos = job
            others = orders[g][pos]
            labels = [chr(ord("A") + idx) for idx in range(len(others))]
            if cfg.identified:
                labels = [self._letter(q) for q in others]
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
                cost=cfg.bpp_cost if cfg.punish_rule == "bpp" else cfg.punish_cost,
                impact=cfg.punish_impact, payoff=bases[g][pos],
                me=self._letter(pos), history=self._history_text(groups[g][pos]) + self._chat_text(groups[g][pos]),
                n=cfg.group_size, endowment=cfg.endowment, mpcr=cfg.mpcr, rounds=cfg.rounds,
                rules_extra=rules_extra(cfg),
                cost_table=cost_table_text())
            if plans:
                i = groups[g][pos]
                compare = "\n".join(f"- {L}: 予想 {plans[i][f'{L}_contrib']}、実際 {contribs[g][q]}"
                                     for L, q in zip(labels, others))
                pp_prompt = self.p["punish_plan"].format(
                    head=prompt.rsplit("それぞれに何点付けますか。", 1)[0].rstrip(),
                    plan=self._plan_text(i, plans[i]), compare=compare, others="・".join(labels))
                pp = self._ask(i, pp_prompt, punish_plan_schema(labels), f"g{g}r{r}:punish_plan")
                pplans[i] = pp
                judges = "\n".join(f"- {L}: {pp[f'{L}_judge']}(印象: {pp[f'{L}_impression']})" for L in labels)
                prompt = (prompt.rsplit("それぞれに何点付けますか。", 1)[0]
                          + f"いま、あなたが考えた減点の作戦:\n{judges}\n仕返しのおそれ: {pp['retaliation']}"
                          f"\n作戦: {pp['plan']}\n\nこの作戦をふまえて、それぞれに何点付けますか。")
            out = self._ask(groups[g][pos], prompt, punish_schema(labels, cfg.punish_max),
                            f"g{g}r{r}:punish")
            for lab, q in zip(labels, others):
                points[g][pos][q] = out[lab]

        self._map(one, jobs)
        if cfg.punish_rule == "bpp":
            for g in range(len(groups)):
                clamp_bpp(points[g], bases[g], cfg)
        return points, orders, pplans

    def play(self):
        for r in range(1, self.cfg.rounds + 1):
            self.play_round(r)
            print(f"  round {r} done, calls={self.run.calls} cost={self.run.cost:.4f}", flush=True)
