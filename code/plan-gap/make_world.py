"""架空の訪問介護事業所の利用者24人分の書類(ケアプラン・訪問介護計画書・サービス提供記録)を作り、不備とひっかけを混ぜる。

すべて架空。対象月は2026年9月。
出力:
  data/docs/Uxx.md    AI に渡す書類(1人1ファイル)
  data/answers.json   混ぜた不備とひっかけの一覧(AI には渡さない)
使い方: python3 make_world.py
"""
import datetime as dt
import json
import random
from pathlib import Path

import sys
HARD = "--hard" in sys.argv  # 不備の人には、変更を知らせる特記事項を書かない
OUT = Path(__file__).parent / ("data-v2" if HARD else "data")
SEED = 156
Y, M = 2026, 9
WD = "月火水木金土日"

# 計画に書く言い方と、記録に書く言い方(言い換え)
ITEMS = {
    "入浴介助": ("身体", "入浴介助(全身浴。洗身の一部介助、浴槽の出入りの見守り)", ["入浴介助。背中と足を洗う。浴槽の出入りを見守り", "全身浴。洗身の一部介助、出入りの見守り", "入浴介助。湯温確認、洗身の一部介助、出入りの見守り"]),
    "排せつ介助": ("身体", "排せつ介助(トイレへの誘導、パッド交換)", ["トイレ誘導。パッド交換", "排せつ介助。トイレ誘導、パッド交換", "トイレまで付き添い。パッド交換"]),
    "更衣介助": ("身体", "更衣介助(上衣の着脱の一部介助)", ["更衣の一部介助(上衣)", "着替えの介助。ボタンを手伝う"]),
    "服薬確認": ("身体", "服薬確認(飲み忘れの確認、声かけ)", ["服薬確認。薬を飲んだことを確認", "服薬の声かけ。飲み忘れなし"]),
    "見守り的援助": ("身体", "自立支援の見守り的援助(本人と一緒に調理し、手順を声かけ)", ["本人と一緒に味噌汁を作る。包丁の扱いを見守り", "一緒に調理。手順を声かけし、本人が炒め物を作る"]),
    "掃除": ("生活", "居室の掃除(居間・寝室)", ["掃除機かけ、床拭き(居間、寝室)", "居間と寝室の掃除", "掃除機、拭き掃除(居間、寝室)"]),
    "トイレ掃除": ("生活", "トイレの掃除", ["トイレ掃除", "便器と床の掃除"]),
    "洗濯": ("生活", "洗濯(洗濯機での洗濯、干す、取り込み)", ["洗濯。干す", "洗濯物を干す。前回分を取り込み", "洗濯機を回し、干す"]),
    "調理": ("生活", "調理(昼食と夕食の作り置き)", ["昼食の調理。夕食分を作り置き", "煮物と汁物を調理(昼食と夕食分)", "調理(昼食と夕食の作り置き)"]),
    "買い物": ("生活", "買い物(日用品と食材。近くのスーパー)", ["買い物(食材、トイレットペーパー)", "近くのスーパーで食材を購入", "買い物代行。レシートを本人と確認"]),
    "シーツ交換": ("生活", "シーツ交換", ["シーツ交換", "シーツと枕カバーを交換"]),
}
OFFPLAN = {  # 計画にない内容として混ぜるもの
    "通院介助": ("身体", None, ["通院の付き添い(病院内の移動の介助、受付)"]),
}
HELPERS = ["ヘルパーA", "ヘルパーB", "ヘルパーC", "ヘルパーD", "ヘルパーE", "ヘルパーF", "ヘルパーG", "ヘルパーH"]
CMS = ["ためし居宅介護支援センター(架空)", "みどり居宅介護支援事業所(架空)", "こもれび ケアプランセンター(架空)"]


def days_of_month():
    d = dt.date(Y, M, 1)
    while d.month == M:
        yield d
        d += dt.timedelta(days=1)


def jdate(d):
    return f"{d.year}年{d.month}月{d.day}日"


def hm(t):
    return f"{t // 60:02d}:{t % 60:02d}"


def make_user(i, rng):
    kind = rng.choice(["身体", "生活", "両方"])
    body = [k for k, v in ITEMS.items() if v[0] == "身体"]
    life = [k for k, v in ITEMS.items() if v[0] == "生活"]
    if kind == "身体":
        items = rng.sample(body, 2)
    elif kind == "生活":
        items = rng.sample(life, 2)
    else:
        items = rng.sample(body, 1) + rng.sample(life, 2)
    nweek = rng.choice([2, 2, 3])
    days = sorted(rng.sample([0, 1, 2, 3, 4], nweek))
    start = rng.choice([9 * 60, 9 * 60 + 30, 10 * 60, 13 * 60 + 30, 14 * 60])
    dur = 60 if kind == "両方" else rng.choice([45, 60])
    return {
        "id": f"U{i:02d}", "kaigo": rng.choice(["要介護1", "要介護2", "要介護2", "要介護3"]),
        "cm": rng.choice(CMS), "items": items, "days": days, "start": start, "dur": dur,
        "helpers": rng.sample(HELPERS, 2),
        "cp_made": dt.date(2026, 6, rng.randint(20, 28)),  # ケアプランの作成日
        "period": (dt.date(2026, 7, 1), dt.date(2026, 12, 31)),
        "new": False, "changes": [], "notes": {}, "extra_visits": [], "offplan": {}, "cancel": set(),
        "revised": None,
    }


def schedule(u):
    """記録に載る訪問の一覧(日付、開始、所要)を返す。"""
    first = u.get("first_day", dt.date(Y, M, 1))
    out = []
    for d in days_of_month():
        if d < first or d in u["cancel"]:
            continue
        days, start = u["days"], u["start"]
        for ch in u["changes"]:  # 途中からの曜日・時間の変更
            if d >= ch["from"]:
                days = ch.get("days", days)
                start = ch.get("start", start)
        once = u.get("once", {}).get(d)
        if d.weekday() in days:
            out.append((d, once if once else start, u["dur"]))
        if d in u["extra_visits"]:
            out.append((d, start, u["dur"]))
    return sorted(out)


def plan_block(title, made, agreed, period, items, days, start, dur, note=""):
    lines = [f"### {title}", "", f"- 作成日: {jdate(made)}", f"- 説明と同意: {jdate(agreed)} 本人の署名あり",
             f"- 計画の期間: {jdate(period[0])}〜{jdate(period[1])}",
             f"- 訪問の曜日と時間: 毎週 {'・'.join(WD[x] for x in days)}曜日 {hm(start)}〜{hm(start + dur)}({dur}分)"]
    if note:
        lines.append(f"- 備考: {note}")
    lines += ["- サービスの内容:"]
    for k in items:
        cat, text, _ = ITEMS[k]
        lines.append(f"  - [{'身体介護' if cat == '身体' else '生活援助'}] {text}")
    return lines


def render(u, rng):
    L = [f"# 利用者 {u['id']}(架空)の書類", "", "ためし訪問介護ステーション(架空)。対象月は2026年9月。", "",
         f"- 要介護度: {u['kaigo']}", f"- 担当の居宅介護支援事業所: {u['cm']}", ""]
    # ケアプラン
    cp_items = u.get("cp_items", u["items"])
    cp_days = u.get("cp_days", u["days"])
    L += ["## 1. ケアプラン(居宅サービス計画書)", "", "### 第1表", "",
          f"- 作成日: {jdate(u['cp_made'])}", f"- 同意日: {jdate(u.get('cp_agreed', u['cp_made']))}",
          f"- 計画の期間: {jdate(u['period'][0])}〜{jdate(u['period'][1])}", "",
          "### 第2表(訪問介護の部分)", "",
          "| サービスの内容 | 種別 | 頻度 |", "|---|---|---|"]
    for k in cp_items:
        cat, text, _ = ITEMS[k]
        L.append(f"| {text} | 訪問介護 | 週{len(cp_days)}回 |")
    L += ["", "### 第3表(週間サービス計画)", "",
          f"- 訪問介護: 毎週 {'・'.join(WD[x] for x in cp_days)}曜日 {hm(u['start'])}〜{hm(u['start'] + u['dur'])}"]
    if u.get("cp_revised"):
        r = u["cp_revised"]
        L += ["", f"### ケアプランの変更({jdate(r['date'])}、同日に同意)", "", f"- {r['text']}"]
    # 訪問介護計画書
    vp = u.get("vp", {})
    L += ["", "## 2. 訪問介護計画書", ""]
    L += plan_block("訪問介護計画書", vp.get("made", u["cp_made"] + dt.timedelta(days=3)),
                    vp.get("agreed", u["cp_made"] + dt.timedelta(days=3)), vp.get("period", u["period"]),
                    vp.get("items", u["items"]), u["days"], u["start"], u["dur"])
    if u["revised"]:
        r = u["revised"]
        L += [""] + plan_block("訪問介護計画書(変更後)", r["made"], r["agreed"], (r["from"], u["period"][1]),
                               u["items"], r["days"], r["start"], u["dur"], r["note"])
    # 記録
    L += ["", "## 3. サービス提供記録(2026年9月)", "",
          "| 日付 | 曜日 | 時間 | 担当 | 区分 | 実施した内容 | 特記事項 |", "|---|---|---|---|---|---|---|"]
    for d, st, dur in schedule(u):
        items = list(u["items"])
        rec = []
        for k in items:
            rec.append(rng.choice(ITEMS[k][2]))
        if d in u["offplan"]:
            k = u["offplan"][d]
            src = OFFPLAN.get(k) or ITEMS[k]
            rec.append(rng.choice(src[2]))
            cats = {ITEMS[x][0] for x in items} | {src[0]}
        else:
            cats = {ITEMS[x][0] for x in items}
        kubun = "身体・生活" if len(cats) == 2 else ("身体介護" if "身体" in cats else "生活援助")
        note = u["notes"].get(d, rng.choice(["", "", "", "変わりなし", "表情よく会話あり", "食欲あり"]))
        L.append(f"| {d.month}/{d.day} | {WD[d.weekday()]} | {hm(st)}〜{hm(st + dur)} | {rng.choice(u['helpers'])} | {kubun} | {'。'.join(rec)} | {note} |")
    for d, text in sorted(u.get("extra_notes", {}).items()):
        L.append(f"| {d.month}/{d.day} | {WD[d.weekday()]} | (訪問なし) | - | - | - | {text} |")
    return "\n".join(L) + "\n"


def weekday_dates(wd, after=None, before=None):
    return [d for d in days_of_month() if d.weekday() == wd and (after is None or d >= after) and (before is None or d <= before)]


# ---- 不備(defect)とひっかけ(trap)の作り方 ----

def d_day_change(u, rng):
    old = rng.choice(u["days"])
    new = rng.choice([x for x in range(5) if x not in u["days"]])
    frm = dt.date(Y, M, rng.choice([7, 14]))  # 週の初め(月曜)から切り替える
    u["changes"].append({"from": frm, "days": sorted([x for x in u["days"] if x != old] + [new])})
    if not HARD:
        u["notes"][weekday_dates(new, after=frm)[0]] = "本人の希望で、今週から" + WD[old] + "曜日の訪問を" + WD[new] + "曜日に変更"
    return {"type": "A", "label": "曜日を変えたのに、計画が古いまま", "detail": f"{jdate(frm)}から{WD[old]}曜日の訪問を{WD[new]}曜日に変更。ケアプランと訪問介護計画は直していない"}


def d_time_change(u, rng):
    frm = dt.date(Y, M, 14)
    new = u["start"] + (240 if u["start"] < 12 * 60 else -240)
    first = [d for d, _, _ in schedule(u) if d >= frm][0]
    u["changes"].append({"from": first, "start": new})
    if not HARD:
        u["notes"][first] = "デイサービスの曜日が変わったため、今回から時間を変更"
    return {"type": "A", "label": "時間を変えたのに、計画が古いまま", "detail": f"{jdate(first)}から訪問の時間を{hm(u['start'])}から{hm(new)}に変更。計画は直していない"}


def d_offplan(u, rng):
    visits = [d for d, _, _ in schedule(u)]
    if rng.random() < 0.5:
        k = "通院介助"
    else:
        k = rng.choice([x for x in ITEMS if x not in u["items"] and x != "見守り的援助"])
    ds = rng.sample(visits, 2)
    for d in ds:
        u["offplan"][d] = k
    return {"type": "B", "label": "計画にない内容を提供した", "detail": f"{'、'.join(jdate(d) for d in sorted(ds))}に、計画にない「{k}」を提供"}


def d_consent_late(u, rng):
    first = dt.date(Y, M, rng.choice([1, 2, 3]))
    while first.weekday() not in u["days"]:
        first += dt.timedelta(days=1)
    u["new"] = True
    u["first_day"] = first
    u["cp_made"] = first - dt.timedelta(days=5)
    u["period"] = (dt.date(Y, M, 1), dt.date(2027, 2, 28))
    agreed = first + dt.timedelta(days=rng.choice([5, 7, 9]))
    u["vp"] = {"made": first - dt.timedelta(days=2), "agreed": agreed}
    u["notes"][first] = "初回訪問。サービスの流れを説明"
    return {"type": "C", "label": "同意日が提供の開始より後", "detail": f"初回の提供は{jdate(first)}、訪問介護計画の同意は{jdate(agreed)}"}


def d_vp_extra(u, rng):
    k = rng.choice([x for x in ITEMS if x not in u["items"] and ITEMS[x][0] == "生活"])
    u["cp_items"] = list(u["items"])
    u["items"] = u["items"] + [k]  # 訪問介護計画と記録にはあるが、ケアプランにない
    return {"type": "D", "label": "訪問介護計画がケアプランとずれている", "detail": f"訪問介護計画と記録に「{k}」があるが、ケアプラン第2表にない"}


def d_extra_visits(u, rng):
    extra_wd = rng.choice([x for x in range(5) if x not in u["days"]])
    ds = weekday_dates(extra_wd)[1:4]
    u["extra_visits"] = ds
    return {"type": "E", "label": "計画より訪問の回数が多い", "detail": f"計画は週{len(u['days'])}回だが、{'、'.join(jdate(d) for d in ds)}({WD[extra_wd]}曜日)にも訪問している"}


def d_expired(u, rng):
    u["period"] = (dt.date(2026, 3, 1), dt.date(2026, 8, 31))
    u["cp_made"] = dt.date(2026, 2, 24)
    return {"type": "F", "label": "計画の期間が切れている", "detail": "ケアプランと訪問介護計画の期間が2026年8月31日で終わっている。9月も同じ内容で提供"}


def t_revised(u, rng):
    old = rng.choice(u["days"])
    new = rng.choice([x for x in range(5) if x not in u["days"]])
    frm = dt.date(Y, M, rng.choice([14, 21]))  # 月曜から
    days = sorted([x for x in u["days"] if x != old] + [new])
    u["changes"].append({"from": frm, "days": days})
    made = frm - dt.timedelta(days=4)
    u["revised"] = {"made": made, "agreed": made, "from": frm, "days": days, "start": u["start"],
                    "note": f"本人の希望で{WD[old]}曜日を{WD[new]}曜日に変更。ケアマネジャーのケアプラン変更を受けて作成"}
    u["cp_revised"] = {"date": made - dt.timedelta(days=1), "text": f"訪問介護の曜日を{jdate(frm)}から{'・'.join(WD[x] for x in days)}曜日に変更"}
    u["notes"][weekday_dates(new, after=frm)[0]] = "今週から曜日変更(計画変更済み)"
    return {"type": "trap", "label": "曜日を変えたが、計画も直してある", "detail": f"{jdate(frm)}から曜日変更。ケアプランと訪問介護計画の変更・同意が変更前にある"}


def t_once(u, rng):
    d = rng.choice([d for d, _, _ in schedule(u)][2:-2])
    new = u["start"] + (180 if u["start"] < 12 * 60 else -180)
    u.setdefault("once", {})[d] = new
    u["notes"][d] = "本人の通院のため、本人とケアマネジャーの了承を得て、この日だけ時間を変更(提供票も変更済み)"
    return {"type": "trap", "label": "1回だけの時間変更(了承と記録あり)", "detail": f"{jdate(d)}だけ時間を変更。ケアマネジャーの了承の記録あり"}


def t_hospital(u, rng):
    a = dt.date(Y, M, 10)
    for k in range(11):
        u["cancel"].add(a + dt.timedelta(days=k))
    u.setdefault("extra_notes", {})[a] = "9/10から入院。ケアマネジャーに連絡し、9/20まで訪問を中止"
    u.setdefault("extra_notes", {})[dt.date(Y, M, 21)] = "退院。ケアマネジャーと確認し、9/21から元の計画どおり再開"
    return {"type": "trap", "label": "入院で訪問を中止した", "detail": "9/10〜9/20は入院のため訪問なし。連絡の記録あり"}


def t_sameday(u, rng):
    first = dt.date(Y, M, rng.choice([1, 2, 3, 4]))
    while first.weekday() not in u["days"]:
        first += dt.timedelta(days=1)
    u["new"] = True
    u["first_day"] = first
    u["cp_made"] = first - dt.timedelta(days=6)
    u["period"] = (dt.date(Y, M, 1), dt.date(2027, 2, 28))
    u["vp"] = {"made": first - dt.timedelta(days=2), "agreed": first}
    u["notes"][first] = "初回訪問。サービス開始前に訪問介護計画を説明し、同意の署名をもらってから開始"
    return {"type": "trap", "label": "同意日と初回の提供日が同じ(提供の前に同意)", "detail": f"{jdate(first)}に同意してから初回の提供"}


def t_cancel(u, rng):
    d = rng.choice([d for d, _, _ in schedule(u)][1:-1])
    u["cancel"].add(d)
    u.setdefault("extra_notes", {})[d] = "本人から前日に連絡があり、家族の来訪のためキャンセル"
    return {"type": "trap", "label": "本人の都合のキャンセル", "detail": f"{jdate(d)}は前日のキャンセルで訪問なし"}


PLAN = (
    [d_day_change] * 3 + [d_time_change] * 1 + [d_offplan] * 3 + [d_consent_late] * 2 +
    [d_vp_extra] * 2 + [d_extra_visits] * 2 + [d_expired] * 1 +
    [t_revised] * 2 + [t_once] * 2 + [t_hospital] * 1 + [t_sameday] * 2 + [t_cancel] * 1 +
    [None] * 2
)


def main():
    rng = random.Random(SEED)
    order = PLAN[:]
    rng.shuffle(order)
    (OUT / "docs").mkdir(parents=True, exist_ok=True)
    answers = {}
    for i, fn in enumerate(order, 1):
        u = make_user(i, rng)
        ans = fn(u, rng) if fn else {"type": "clean", "label": "不備なし", "detail": ""}
        if u["kaigo"] and "見守り的援助" in u["items"] and ITEMS["見守り的援助"]:
            pass
        (OUT / "docs" / f"{u['id']}.md").write_text(render(u, rng))
        answers[u["id"]] = ans
    (OUT / "answers.json").write_text(json.dumps(answers, ensure_ascii=False, indent=1))
    from collections import Counter
    print(Counter(a["type"] for a in answers.values()))


if __name__ == "__main__":
    main()
