"""ルールを動かす部品(ホールドアウトの交渉)。値段の受け渡しと稼ぎの計算はプログラムで行う。

子07(#181)で Cadigan, Schmitt, Shupp & Swope(2009)を再現する。既定の設定は論文に合わせてある。
- 3人1組。買い手1人、売り手2人。各組は交渉を1回だけ行う
- 買い手は2つの品物を両方買えたときだけ価値 V=90。売り手の費用は各 c=30
- proposer="buyer": 買い手が売り手ごとに買う値段を出し、売り手が受けるか断る
  proposer="seller": 売り手がそれぞれ売る値段を出し、買い手が売り手ごとに受けるか断る
- 同じ期の提示は同時。決まった売り手は、そのあと何も決めない
- 売り手は、もう一人への提示を見ない。決まった値段だけを知らされる
- periods 期までに両方決まらなければ、3人とも0(決まった売り手も0)
- delay=True: 断られるたびに、全員の稼ぎが5%ずつ減る(論文 3.1。2回なら10%)
- 値段は1ドル単位(論文は1セント単位)

論文で決まっていないところ(作り直した部分):
- 遅れの損で今どれだけ減っているかは、3人全員に知らせる(売り手が自分の稼ぎを知るのに要るため)
- 値段は0〜90ドル。買い手の稼ぎがマイナスになる値段も受け付ける
"""
import json
import random
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

ACCEPT, REJECT = "売る", "断る"
BOT_REASON = "(プログラムの買い手)"
SELLER_BELIEF = ("\nあわせて、もし今期あなたが断ったら、買い手が次の期にあなたへいくらを出すと思うかを next_price(ドル)で、"
                 "次の期の値段が今期より高くなる見込みを chance_up(0〜100%)で答えてください。")
BUYER_PROPOSER_BELIEF = ("\nあわせて、今期あなたが出す値段を受けてもらえる見込みを accept_new_番号(0〜100%)で、"
                         "もし{who}を、もう一度出したら受けてもらえる見込みを accept_old_番号(0〜100%)で答えてください。")
SELLER_PROPOSER_BELIEF = ("\nあわせて、今期あなたが出す値段を買い手が買う見込みを accept_new(0〜100%)で、"
                          "もし前の期と同じ{prev}ドルを、もう一度出したら買う見込みを accept_old(0〜100%)で答えてください。")
BUYER_BELIEF = ("\nあわせて、もし今期あなたが断ったら、その売り手が次の期にいくらを出すと思うかを next_price_番号(ドル)で、"
                "次の期の値段が今期より低くなる見込みを chance_down_番号(0〜100%)で答えてください。")
BUY, NO = "買う", "断る"
# 受け止め方を数字で書かせる(#181 違い1。添付メモの Emotion: 出来事をどう評価したか)
SELLER_EMOTION = "\nあわせて、買い手が出したこの値段を、あなたはどれくらい不公平だと感じるかを unfair(0=まったく感じない〜100=とても強く感じる)で答えてください。"
BUYER_EMOTION = "\nあわせて、それぞれの売り手が出した値段を、あなたはどれくらい不公平だと感じるかを unfair_番号(0=まったく感じない〜100=とても強く感じる)で答えてください。"


@dataclass
class Config:
    proposer: str = "buyer"     # buyer / seller
    periods: int = 10
    delay: bool = False
    value: int = 90
    cost: int = 30
    max_price: int = 90
    delay_step: float = 0.05
    memory: bool = False        # 自分が前の期に書いた理由も渡す(#181 検証)
    buyer_bot: bool = False     # 買い手をプログラムにする(#181 検証。proposer="buyer" のときだけ)
    bot_start: int = 35
    bot_step: int = 1
    damp: float = None          # 出す側の譲り幅を、AIが譲った幅のこの割合に抑える(#181 意図の持続)
    hybrid_proposer: bool = False  # 出す側にも組み合わせ型を使う(#181)
    hybrid_mu: float = None     # 組み合わせ型: 断るしきい値の平均(ドル)。belief=True と一緒に使う(#181)
    belief: bool = False        # 受ける側に、相手の次の値段の見込みを数字で書かせる(#181 検証)
    emotion: bool = False       # 受ける側に、提示をどれくらい不公平と感じたかを書かせる(#181 違い1)
    remind: bool = False        # 残りの期と、断ったときの損を毎期知らせる(#181 検証)
    reason_first: bool = True   # 理由を先に書かせる(数字を先に答えさせると理由が後付けになるおそれ、#173)


def _schema(fields, reason_first):
    props = dict(fields)
    keys = list(fields)
    if reason_first:
        props = {"reason": {"type": "string"}, **props}
        keys = ["reason"] + keys
    else:
        props["reason"] = {"type": "string"}
        keys = keys + ["reason"]
    return {"type": "object", "properties": props, "required": keys}


def label(s):
    return f"売り手{s + 1}"


def payoffs(prices, rejections, cfg):
    """両方決まったときの稼ぎ(買い手, 売り手1, 売り手2)。決まらなければ全員0。"""
    if any(p is None for p in prices):
        return [0.0, 0.0, 0.0]
    mult = max(0.0, 1 - cfg.delay_step * rejections) if cfg.delay else 1.0
    buyer = (cfg.value - sum(prices)) * mult
    return [round(buyer, 2)] + [round((p - cfg.cost) * mult, 2) for p in prices]


def rules_text(template, cfg, role):
    if cfg.proposer == "buyer":
        proposer_rule = ("- 毎期、買い手が、まだ売り買いが決まっていない売り手ごとに、買う値段を出します。"
                         "売り手は、その値段で売るか、断るかだけを選びます。2人への値段は同時に出します。")
    else:
        proposer_rule = ("- 毎期、まだ売り買いが決まっていない売り手が、それぞれ売る値段を出します。"
                         "買い手は、売り手ごとに、その値段で買うか、断るかだけを選びます。2人の値段は同時に出します。")
    if cfg.periods == 1:
        period_rule = "- やり取りは1期だけです。"
        fail_rule = "1期目で両方の売り買いが決まらなければ、3人とも稼ぎは0です(売り買いが決まった売り手も0です)。"
    else:
        who = "買い手" if cfg.proposer == "buyer" else "売り手"
        period_rule = (f"- やり取りは最大{cfg.periods}期です。断られたら、{who}は次の期に新しい値段を出せます。"
                       "前より上げる、下げるという決まりはありません。")
        fail_rule = (f"{cfg.periods}期目が終わるまでに両方の売り買いが決まらなければ、"
                     "3人とも稼ぎは0です(売り買いが決まった売り手も0です)。")
    delay_rule = ("- 値段が断られるたびに、3人全員の稼ぎが5%ずつ減ります(2回断られれば10%減ります)。"
                  if cfg.delay and cfg.periods > 1 else "")
    text = template.format(role=role, cost=cfg.cost, value=cfg.value, proposer_rule=proposer_rule,
                           period_rule=period_rule, delay_rule=delay_rule, fail_rule=fail_rule)
    return "\n".join(line for line in text.split("\n") if line != "")


class Group:
    """1組の交渉。members は [(人物像, 説明文)] を [買い手, 売り手1, 売り手2] の順に。"""

    def __init__(self, gid, members, llm, prompts, cfg, run):
        self.gid = gid
        self.members = members
        self.llm = llm
        self.p = prompts
        self.cfg = cfg
        self.run = run
        self.prices = [None, None]      # 決まった値段
        self.closed_at = [None, None]   # 決まった期
        self.rejections = 0
        self.log = []                   # 期ごとの提示と答え
        self._rejected_by = [0, 0]      # 売り手ごとの、断った回数
        # 組み合わせ型のしきい値(ドル)。人ごとに、平均 hybrid_mu・標準偏差 hybrid_mu/2 の正規分布から引く(0未満は0)
        rng = random.Random(f"{cfg.hybrid_mu}-{gid}")
        self.theta = [max(0.0, rng.gauss(cfg.hybrid_mu, cfg.hybrid_mu / 2)) if cfg.hybrid_mu is not None else None
                      for _ in range(3)]

    # --- 問いを作る部品 ---
    def _system(self, who):
        role = "買い手" if who == 0 else label(who - 1)
        persona_sys = self.p["system"].format(persona=self.members[who][1])
        return persona_sys.rstrip("\n") + "\n\n" + rules_text(self.p["rules"], self.cfg, role)

    def _status(self, t):
        text = ""
        if self.cfg.delay and self.cfg.periods > 1:
            pct = round(min(1.0, self.cfg.delay_step * self.rejections) * 100)
            text += f"\nこれまでに値段が断られた回数は合計{self.rejections}回で、3人の稼ぎは{pct}%減っています。"
        if self.cfg.remind and self.cfg.periods > 1:   # 決まりからそのまま言える、待つことの損得(#181 検証)
            left = self.cfg.periods - t
            if t == self.cfg.periods:
                text += "\nこれが最後の期です。今期で両方決まらなければ、3人とも稼ぎは0です。"
            elif self.cfg.delay:
                text += f"\nこの期のあとに、まだ{left}期あります。今期に値段が断られると、3人の稼ぎがさらに5%減ります。"
            else:
                text += f"\nこの期のあとに、まだ{left}期あります。今期に値段が断られても、稼ぎは減りません。"
        return text

    def _history(self, who):
        """who=0 は買い手。売り手は自分のやり取りと、もう一人の決まった値段だけを見る。"""
        lines = []
        for row in self.log:
            t = row["period"]
            parts = []
            for s in (0, 1):
                if s not in row["offers"]:
                    continue
                price, ok = row["offers"][s], row["accepted"][s]
                if who == 0:
                    if self.cfg.proposer == "buyer":
                        parts.append(f"{label(s)}に{price}ドルを出し、" + ("売ってもらえた" if ok else "断られた"))
                    else:
                        parts.append(f"{label(s)}が{price}ドルを出し、あなたは" + ("買った" if ok else "断った"))
                elif who - 1 == s:
                    if self.cfg.proposer == "buyer":
                        parts.append(f"買い手が{price}ドルを出し、あなたは" + ("売った" if ok else "断った"))
                    else:
                        parts.append(f"あなたが{price}ドルを出し、買い手は" + ("買った" if ok else "断った"))
                elif ok:
                    parts.append(f"もう一人の売り手は{price}ドルで売り買いが決まった")
            if parts:
                lines.append(f"第{t}期: " + "。".join(parts) + "。")
                mine = row["reasons"].get("buyer" if who == 0 else label(who - 1))
                if self.cfg.memory and mine and mine != BOT_REASON:   # 自分がその期に書いた理由も渡す(#181 検証)
                    lines.append(f"  このとき、あなたが書いた理由: {mine}")
        return "\n".join(lines) if lines else "(まだありません)"

    def _ask(self, who, prompt, schema, tag):
        system = self._system(who)
        reply = self.llm.ask(system, prompt, schema)
        self.run.call(self.members[who][0]["id"], system, prompt, reply, tag=f"g{self.gid}:{tag}")
        return reply.output

    def _base(self, t):
        return {"periods": self.cfg.periods, "period": t, "status": self._status(t), "max": self.cfg.max_price}

    def _ask_belief(self, t):
        """受ける側に、断ったときの相手の次の値段の見込みを聞くか(最後の期は次がないので聞かない)。"""
        return self.cfg.belief and t < self.cfg.periods

    def _respond(self, t, s, offers):
        prompt = self.p["seller_respond"].format(price=offers[s], history=self._history(s + 1), **self._base(t))
        fields = {}
        if self._ask_belief(t):   # 信念を数字で書かせる(#181 検証。答えより前に書かせる)
            prompt += SELLER_BELIEF
            fields = {"next_price": {"type": "integer", "minimum": 0, "maximum": self.cfg.max_price},
                      "chance_up": {"type": "integer", "minimum": 0, "maximum": 100}}
        if self.cfg.emotion:
            prompt += SELLER_EMOTION
            fields["unfair"] = {"type": "integer", "minimum": 0, "maximum": 100}
        fields["decision"] = {"type": "string", "enum": [ACCEPT, REJECT]}
        return s, self._ask(s + 1, prompt, _schema(fields, self.cfg.reason_first), f"t{t}:respond{s + 1}")

    @staticmethod
    def _seller_beliefs(answers):
        return {label(s): {"next_price": a["next_price"], "chance": a["chance_up"]}
                for s, a in answers.items() if "next_price" in a}

    def _gain(self, s, cur, nxt, offers):
        """断って、次の期に予想どおりの値段で決まったときの、自分の稼ぎの増え方(遅れの損を引いたあと)。"""
        cfg = self.cfg
        m = max(0.0, 1 - cfg.delay_step * self.rejections) if cfg.delay else 1.0
        step = cfg.delay_step if cfg.delay else 0.0
        if cfg.proposer == "buyer":   # 受ける側は売り手
            return (nxt - cfg.cost) * (m - step) - (cur - cfg.cost) * m
        other = 1 - s                 # 受ける側は買い手。もう一人の値段は、今期の要求か決まった値段
        p_other = offers.get(other, self.prices[other]) or 0
        return (cfg.value - p_other - nxt) * (m - step) - (cfg.value - p_other - cur) * m

    def _prev_offer(self, s):
        """その売り手との、前の期の値段(断られたもの)。なければ None。"""
        for row in reversed(self.log):
            if s in row["offers"]:
                return row["offers"][s]
        return None

    def _rule_propose(self, buyer, offers, q):
        """出す側の組み合わせ型(#181): AIが新しい値段で譲ったとき、前の値段のまま出すかを決まりで決める。
        見込み×自分の取り分 を比べ、前の値段の期待がしきい値ぶん下回らない限り、前の値段を出す。"""
        cfg = self.cfg
        out, log = dict(offers), {}
        for s, (q_new, q_old) in q.items():
            prev, new = self._prev_offer(s), offers[s]
            if cfg.proposer == "buyer":
                if new <= prev:      # 譲っていない(下げた・同じ)ならそのまま
                    continue
                p_other = offers.get(1 - s, self.prices[1 - s]) or 0
                v_new, v_old = cfg.value - p_other - new, cfg.value - p_other - prev
                who = 0
            else:
                if new >= prev:
                    continue
                v_new, v_old = new - cfg.cost, prev - cfg.cost
                who = s + 1
            e_new, e_old = q_new / 100 * v_new, q_old / 100 * v_old
            hold = e_old + self.theta[who] >= e_new
            log[label(s)] = {"ai": new, "prev": prev, "q_new": q_new, "q_old": q_old, "hold": hold}
            if hold:
                out[s] = prev
        return out, log

    def _damp(self, t, offers):
        """出す側の意図の持続(#181): AIが前の値段から譲ったとき、実際に譲るのはその幅の damp 割だけ。
        譲っていない(据え置き・強気に戻す)ときと、最後の期は、AIの値段のまま。"""
        if self.cfg.damp is None or t == self.cfg.periods:
            return offers, None
        out, log = dict(offers), {}
        sign = 1 if self.cfg.proposer == "buyer" else -1   # 買い手は上げると譲り、売り手は下げると譲る
        for s, new in offers.items():
            prev = self._prev_offer(s)
            if prev is None or (new - prev) * sign <= 0:
                continue
            out[s] = prev + int((new - prev) * self.cfg.damp + 0.5 * sign)
            log[label(s)] = {"ai": new, "prev": prev, "sent": out[s]}
        return out, log

    def _rule_decide(self, open_s, offers, beliefs, accepted):
        """組み合わせ型(#181): AIが書いた次の値段の見込みを使い、決まりで売る・断るを決める。
        増え方が、受ける人ごとのしきい値を超えたら断る。最後の期は見込みがないので、AIの答えのまま。"""
        out = dict(accepted)
        for s in open_s:
            b = beliefs.get(label(s))
            if not b:
                continue
            who = 0 if self.cfg.proposer == "seller" else s + 1
            out[s] = self._gain(s, offers[s], b["next_price"], offers) <= self.theta[who]
        return out

    # --- 1期 ---
    def _period(self, t, pool):
        cfg = self.cfg
        open_s = [s for s in (0, 1) if self.prices[s] is None]
        price_f = {"type": "integer", "minimum": 0, "maximum": cfg.max_price}
        offers, reasons, beliefs, emotions = {}, {}, {}, {}
        proposer_rule = damp_log = None
        if cfg.proposer == "buyer" and cfg.buyer_bot:
            # 買い手をプログラムにする: 1期目に bot_start ドル、その売り手に断られるたびに bot_step ドル上げる
            offers = {s: min(cfg.max_price, cfg.bot_start + cfg.bot_step * self._rejected_by[s]) for s in open_s}
            reasons["buyer"] = BOT_REASON
            answers = dict(pool.map(lambda s: self._respond(t, s, offers), open_s))
            accepted = {s: answers[s]["decision"] == ACCEPT for s in open_s}
            for s in open_s:
                reasons[label(s)] = answers[s]["reason"]
            beliefs = self._seller_beliefs(answers)
            emotions = {label(s): a["unfair"] for s, a in answers.items() if "unfair" in a}
        elif cfg.proposer == "buyer":
            fields = {f"price_{s + 1}": price_f for s in open_s}
            targets = "と".join(label(s) for s in open_s)
            prompt = self.p["buyer_offer"].format(targets=targets, history=self._history(0), **self._base(t))
            held = [s for s in open_s if self._prev_offer(s) is not None] if cfg.hybrid_proposer else []
            if held:   # 出す側の組み合わせ型: 前と同じ値段と、新しい値段が受けられる見込みを書かせる
                prompt += BUYER_PROPOSER_BELIEF.format(who="、".join(f"{label(s)}には前の期の{self._prev_offer(s)}ドル" for s in held))
                for s in held:
                    fields[f"accept_new_{s + 1}"] = {"type": "integer", "minimum": 0, "maximum": 100}
                    fields[f"accept_old_{s + 1}"] = {"type": "integer", "minimum": 0, "maximum": 100}
            out = self._ask(0, prompt, _schema(fields, cfg.reason_first), f"t{t}:offer")
            offers = {s: out[f"price_{s + 1}"] for s in open_s}
            offers, damp_log = self._damp(t, offers)
            reasons["buyer"] = out["reason"]
            if held:
                q = {s: (out[f"accept_new_{s + 1}"], out[f"accept_old_{s + 1}"]) for s in held}
                offers, proposer_rule = self._rule_propose(0, offers, q)

            answers = dict(pool.map(lambda s: self._respond(t, s, offers), open_s))
            accepted = {s: answers[s]["decision"] == ACCEPT for s in open_s}
            for s in open_s:
                reasons[label(s)] = answers[s]["reason"]
            beliefs = self._seller_beliefs(answers)
            emotions = {label(s): a["unfair"] for s, a in answers.items() if "unfair" in a}
        else:
            def demand(s):
                prompt = self.p["seller_demand"].format(history=self._history(s + 1), **self._base(t))
                fields = {"price": price_f}
                prev = self._prev_offer(s) if cfg.hybrid_proposer else None
                if prev is not None:
                    prompt += SELLER_PROPOSER_BELIEF.format(prev=prev)
                    fields["accept_new"] = {"type": "integer", "minimum": 0, "maximum": 100}
                    fields["accept_old"] = {"type": "integer", "minimum": 0, "maximum": 100}
                return s, self._ask(s + 1, prompt, _schema(fields, cfg.reason_first), f"t{t}:demand{s + 1}")
            answers = dict(pool.map(demand, open_s))
            offers = {s: answers[s]["price"] for s in open_s}
            offers, damp_log = self._damp(t, offers)
            q = {s: (a["accept_new"], a["accept_old"]) for s, a in answers.items() if "accept_new" in a}
            if q:
                offers, proposer_rule = self._rule_propose(None, offers, q)
            for s in open_s:
                reasons[label(s)] = answers[s]["reason"]
            demands = "\n".join(f"{label(s)}: {offers[s]}ドル" for s in open_s)
            fields = {}
            prompt = self.p["buyer_respond"].format(demands=demands, history=self._history(0), **self._base(t))
            if self._ask_belief(t):
                prompt += BUYER_BELIEF
                for s in open_s:
                    fields[f"next_price_{s + 1}"] = {"type": "integer", "minimum": 0, "maximum": cfg.max_price}
                    fields[f"chance_down_{s + 1}"] = {"type": "integer", "minimum": 0, "maximum": 100}
            if cfg.emotion:
                prompt += BUYER_EMOTION
                fields.update({f"unfair_{s + 1}": {"type": "integer", "minimum": 0, "maximum": 100} for s in open_s})
            fields.update({f"decision_{s + 1}": {"type": "string", "enum": [BUY, NO]} for s in open_s})
            out = self._ask(0, prompt, _schema(fields, cfg.reason_first), f"t{t}:respond")
            accepted = {s: out[f"decision_{s + 1}"] == BUY for s in open_s}
            reasons["buyer"] = out["reason"]
            if cfg.emotion:
                emotions = {label(s): out[f"unfair_{s + 1}"] for s in open_s}
            if self._ask_belief(t):
                beliefs = {label(s): {"next_price": out[f"next_price_{s + 1}"], "chance": out[f"chance_down_{s + 1}"]}
                           for s in open_s}
        ai_accepted = None
        if cfg.hybrid_mu is not None and beliefs:
            ai_accepted = {label(s): v for s, v in accepted.items()}
            accepted = self._rule_decide(open_s, offers, beliefs, accepted)
        for s in open_s:
            if accepted[s]:
                self.prices[s] = offers[s]
                self.closed_at[s] = t
            else:
                self.rejections += 1
                self._rejected_by[s] += 1
        row = {"period": t, "offers": offers, "accepted": accepted, "rejections_total": self.rejections,
               "reasons": reasons, "beliefs": beliefs}
        if ai_accepted is not None:
            row["ai_accepted"] = ai_accepted
        if emotions:
            row["emotions"] = emotions
        if damp_log:
            row["damp"] = damp_log
        if proposer_rule:
            row["proposer_rule"] = proposer_rule
        self.log.append(row)
        return row

    def play(self, inner_workers=2):
        with ThreadPoolExecutor(inner_workers) as pool:
            for t in range(1, self.cfg.periods + 1):
                self._period(t, pool)
                if all(p is not None for p in self.prices):
                    break
        pay = payoffs(self.prices, self.rejections, self.cfg)
        result = {
            "group": self.gid,
            "members": [m[0]["id"] for m in self.members],
            "rounds": [{**r, "offers": {label(s): v for s, v in r["offers"].items()},
                        "accepted": {label(s): v for s, v in r["accepted"].items()}} for r in self.log],
            "prices": self.prices,
            "closed_at": self.closed_at,
            "rejections": self.rejections,
            "complete": all(p is not None for p in self.prices),
            "payoffs": pay,
            "efficiency": round(sum(pay) / (self.cfg.value - 2 * self.cfg.cost), 4),
            "theta": self.theta,
        }
        self.run.event(result)
        return result


def summarize(results, cfg):
    """回す前に決めた物差し(05-再現の設計.md)を、条件ごとに数える。"""
    first = [r["rounds"][0] for r in results]
    amounts = [v for f in first for v in f["offers"].values()]
    rej = [not v for f in first for v in f["accepted"].values()]
    out = {
        "groups": len(results),
        "first_amount_mean": round(sum(amounts) / len(amounts), 2),
        "first_reject_rate": round(sum(rej) / len(rej), 3),
        "failed": sum(not r["complete"] for r in results),
        "efficiency": round(sum(r["efficiency"] for r in results) / len(results), 3),
        # 同じ問いに同じ答えを返す癖(#173)を見る: 1期目の額が何種類あるか
        "first_amount_kinds": len(set(amounts)),
    }
    if cfg.periods > 1:
        out["rejections_per_group"] = round(sum(r["rejections"] for r in results) / len(results), 2)
    # 粘った持ち主ほど稼ぐか: 1期目に断った売り手の、決まった値段と1期目の提示の差
    if cfg.proposer == "buyer" and cfg.periods > 1:
        gains = []
        for r in results:
            f = r["rounds"][0]
            for s in (0, 1):
                key = label(s)
                if key in f["accepted"] and not f["accepted"][key] and r["prices"][s] is not None:
                    gains.append(r["prices"][s] - f["offers"][key])
        out["holdout_gain_mean"] = round(sum(gains) / len(gains), 2) if gains else None
    return out


def play_all(groups, llm, prompts, cfg, run, workers=6):
    """組ごとに並べて回す。groups は [[買い手, 売り手1, 売り手2], ...](各要素は (人物像, 説明文))。"""
    def one(args):
        gid, mem = args
        return Group(gid, mem, llm, prompts, cfg, run).play()
    with ThreadPoolExecutor(workers) as pool:
        results = list(pool.map(one, enumerate(groups)))
    return results, summarize(results, cfg)


def load_prompts(root):
    names = ["rules", "buyer_offer", "seller_respond", "seller_demand", "buyer_respond"]
    paths = {k: f"{root}/holdout/{k}.md" for k in names}
    paths["system"] = f"{root}/pgg/system.md"
    return {k: open(p, encoding="utf-8").read() for k, p in paths.items()}, paths


if __name__ == "__main__":
    print(json.dumps(payoffs([40, 40], 3, Config(delay=True)), ensure_ascii=False))
