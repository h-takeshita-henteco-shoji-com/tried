"""迷惑施設の受け入れを聞く調査(#170)。Frey と Oberholzer-Gee(1997)の面接調査を、AIの住民で再現する。

論文に合わせたところ:
- 説明のあと、同じ人に、補償なしの問い(問1)→補償ありの問い(問2)の順に聞く
- 補償は1人1年あたり2,500/5,000/7,500フランのどれか。人ごとに割り当てる(3つを同じ人数ずつ)
- 家族の合計額は、1人あたりの額 × 世帯の人数で計算して伝える
- 問2に反対した人には、金額を上げて聞き直す(2,500→3,650、5,000→7,500、7,500→10,000フラン)
- 聞き直しでも反対した人には、理由を聞く(問3)。論文では問2に反対した人に聞いている

論文で決まっていないところ(作り直した部分):
- 説明の文は、論文の要約から作った。論文の説明はもっと詳しく、事故の確率なども先に聞いている
- 問3は、聞き直しのあとに聞く(論文では順番が書かれていない)
- 人物像の矛盾(若い年金暮らし、1人暮らしで家事だけ)は、fix_person で直す
"""
import random
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

ANSWERS = ["賛成", "反対", "どちらでもない"]
RAISE = {2500: 3650, 5000: 7500, 7500: 10000}


@dataclass
class Config:
    amounts: tuple = (2500, 5000, 7500)
    raise_offer: bool = True    # 問2に反対した人に、金額を上げて聞き直す
    ask_reasons: bool = True    # 最後まで反対した人に、問3を聞く
    compensation: bool = True   # False なら問1だけ聞く
    form: str = "cash"          # cash: 家族に現金 / public: 村に同じ額の公共の設備(#170 確かめる3) / none: 補償なしでもう一度聞く
    appraise: bool = False      # 問2で、補償の受け止め(償い・買収・外から動かす)を0〜100で書かせる
    own_motive: bool = False    # 問2では人物像から考え方の3文を外し、問1で自分が書いた理由だけを渡す(根1)
    show_prev: bool = True      # 問2で、問1の答えを見せる。False なら問2を別に聞く(論文からは外れる。前の答えに引きずられるかの確かめ)


def _schema(extra=None):
    props = {"reason": {"type": "string"}, "answer": {"type": "string", "enum": ANSWERS}}
    props.update(extra or {})
    return {"type": "object", "properties": props, "required": list(props)}


Q3_SCHEMA = {"type": "object",
             "properties": {"reason": {"type": "string"}, "higher_comp": {"type": "boolean"},
                            "danger_signal": {"type": "boolean"}},
             "required": ["reason", "higher_comp", "danger_signal"]}


def fmt(n):
    return f"{n:,}"


APPRAISE = {k: {"type": "integer", "minimum": 0, "maximum": 100} for k in ("compensation", "bribe", "control")}


def interview(i, person, desc, amount, llm, prompts, cfg, run, desc2=None):
    """1人に、問1から順に聞く。答えを1つの記録にまとめて返す。"""
    system = prompts["system"].format(persona=desc)
    brief = prompts["briefing"].rstrip("\n") + "\n\n"
    row = {"id": person["id"], "person": person, "amount": amount}

    def ask(tag, body, schema, sys_=None):
        prompt = brief + body
        reply = llm.ask(sys_ or system, prompt, schema)
        run.call(person["id"], sys_ or system, prompt, reply, tag=f"{person['id']}:{tag}")
        return reply.output

    q1 = ask("q1", prompts["q1"], _schema())
    row["q1"] = q1
    if not cfg.compensation:
        return row
    size = int(person["household"].rstrip("人"))
    q1_text = prompts["q1"].split("\n\nanswer")[0]
    q2_key = "q2" if cfg.show_prev else "q2_fresh"
    if cfg.form == "public":
        q2_key = "q2_public"
    if cfg.form == "none":   # 補償なしの問いを、同じ形でもう一度聞く(own_motive の比べる相手)
        q2_key = "q2_none"
    body = prompts[q2_key].format(q1_text=q1_text, q1_answer=q1["answer"], q1_reason=q1["reason"],
                                  per_person=fmt(amount), family=fmt(amount * size), village=fmt(amount * 2000))
    if cfg.appraise:
        body = body.rstrip("\n") + "\n" + prompts["appraise"]
    sys2 = prompts["system"].format(persona=desc2) if cfg.own_motive else None
    q2 = ask("q2", body, _schema(APPRAISE if cfg.appraise else None), sys2)
    row["q2"] = q2
    last = q2
    if q2["answer"] == "反対" and cfg.raise_offer and cfg.form == "cash":
        a2 = RAISE[amount]
        last = ask("q2_raise", prompts["q2_raise"].format(prev_answer=q2["answer"], prev_reason=q2["reason"],
                                                           per_person=fmt(amount), per_person2=fmt(a2),
                                                           family2=fmt(a2 * size)), _schema())
        row["q2_raise"] = {"amount": a2, **last}
    if last["answer"] == "反対" and cfg.ask_reasons:
        row["q3"] = ask("q3", prompts["q3"].format(prev_reason=last["reason"]), Q3_SCHEMA)
    run.event(row)
    return row


def share(rows, key, ans="賛成"):
    xs = [r[key]["answer"] for r in rows if key in r]
    return round(100 * sum(x == ans for x in xs) / len(xs), 1) if xs else None


def summarize(rows, cfg):
    out = {"n": len(rows)}
    for a in ANSWERS:
        out[f"q1_{a}"] = share(rows, "q1", a)
    if cfg.compensation:
        for a in ANSWERS:
            out[f"q2_{a}"] = share(rows, "q2", a)
        out["q2_賛成_by_amount"] = {str(m): share([r for r in rows if r["amount"] == m], "q2") for m in cfg.amounts}
        # 問1で賛成した人のうち、問2で賛成をやめた人の割合
        yes1 = [r for r in rows if r["q1"]["answer"] == "賛成"]
        out["q1賛成→q2賛成以外"] = round(100 * sum(r["q2"]["answer"] != "賛成" for r in yes1) / len(yes1), 1) if yes1 else None
        no1 = [r for r in rows if r["q1"]["answer"] != "賛成"]
        out["q1賛成以外→q2賛成"] = round(100 * sum(r["q2"]["answer"] == "賛成" for r in no1) / len(no1), 1) if no1 else None
        raised = [r for r in rows if "q2_raise" in r]
        out["聞き直しで賛成に変えた人数"] = sum(r["q2_raise"]["answer"] == "賛成" for r in raised)
        q3 = [r["q3"] for r in rows if "q3" in r]
        if q3:
            out["q3_n"] = len(q3)
            out["q3_もっと高い補償"] = round(100 * sum(x["higher_comp"] for x in q3) / len(q3), 1)
            out["q3_危険のしるし"] = round(100 * sum(x["danger_signal"] for x in q3) / len(q3), 1)
        if cfg.appraise:
            for k in ("compensation", "bribe", "control"):
                xs = [r["q2"][k] for r in rows]
                out[f"受け止め_{k}"] = round(sum(xs) / len(xs), 1)
                for a in ("賛成", "反対"):
                    ys = [r["q2"][k] for r in rows if r["q2"]["answer"] == a]
                    out[f"受け止め_{k}_{a}"] = round(sum(ys) / len(ys), 1) if ys else None
    return out


def fix_person(p, rng):
    """人物像の矛盾を直す。年金暮らしは63歳以上、1人暮らしなら家事だけの暮らしにしない。"""
    if p["job"].startswith("仕事を退き") and p["age"] < 63:
        p["age"] = rng.randint(63, 79)
    if not p["job"].startswith("仕事を退き") and p["age"] >= 66:
        p["job"] = "仕事を退き、年金で暮らしている"
    if p["job"] == "家事をしている" and p["household"] == "1人":
        p["household"] = rng.choice(["2人", "3人", "4人"])
    return p


def assign_amounts(n, cfg, seed):
    """補償の額を、3つが同じ人数ずつになるように、くじで割り当てる。"""
    xs = [cfg.amounts[i % len(cfg.amounts)] for i in range(n)]
    random.Random(seed).shuffle(xs)
    return xs


def play_all(people, llm, prompts, cfg, run, seed, workers=8, desc2=None):
    """people は [(人物像, 説明文), ...]。desc2 は、考え方の3文を外した説明文(own_motive のとき)。"""
    amounts = assign_amounts(len(people), cfg, seed)

    def one(i):
        p, desc = people[i]
        return interview(i, p, desc, amounts[i], llm, prompts, cfg, run, desc2[i] if desc2 else None)
    with ThreadPoolExecutor(workers) as pool:
        rows = list(pool.map(one, range(len(people))))
    return rows, summarize(rows, cfg)


def load_prompts(root):
    names = ["system", "briefing", "q1", "q2", "q2_fresh", "q2_public", "q2_none", "appraise", "q2_raise", "q3"]
    paths = {k: f"{root}/siting/{k}.md" for k in names}
    return {k: open(p, encoding="utf-8").read() for k, p in paths.items()}, paths
