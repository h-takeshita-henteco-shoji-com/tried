"""台帳 council/ledger.jsonl に、その月の局の案を1件1行で足す(#100。council-design.md の9.4、interfaces の8)。

council/m<月>-run.json(Workflow の返り値)と各役のファイルから作る。AI には書かせない。
同じ月をもう一度走らせたら、その月の行を置き換える。
前の月の行の review は、今月の局の案のファイルの「前の月の答え合わせ」から埋める(読めなければ null のまま)。

    python3 code/ai-mayor/tools/make_council_ledger.py <運営のフォルダ> <月>
"""

import argparse
import json
import re
from pathlib import Path

from council_common import (BUREAUS, judge_review, labeled, month_file, read_hooks_log, read_json, read_text,
                            seen_tools)

ROLES = ["policy", "guide", "finance", "bill", "bill-2", "assembly", "assembly-2"]


def called_tools(hooks, agent):
    # hooks の記録で、その定義が呼んだ道具(拒否は呼んだうちに数えない)
    return {h["tool"] for h in hooks if h["agent"] == agent and h["result"] in ("ok", "ng")}


def seen_check(md, hooks, agent):
    claimed = seen_tools(md)
    called = called_tools(hooks, agent)
    return {"claimed": claimed, "unlogged": [t for t in claimed if t not in called]}


def priority_of(md, plan_items, priorities):
    """編成方針の重点に当たるか。案のファイルの「市の計画」の欄を先に見て、決まらなければ重点の言葉と施策の番号を比べる。"""
    text = labeled(md, "市の計画") or ""
    if re.search(r"重点[^。\n]*(当たらない|外れ|ではない|でない)", text):
        return False
    if re.search(r"重点[^。\n]*(当たる|に入る|のうち)", text):
        return True
    if plan_items and priorities:
        return any(p in pr for p in plan_items for pr in priorities)
    return None


def find_measure(bill, bureau):
    for m in (bill or {}).get("measures") or []:
        if m.get("fromBureau") == bureau:
            return m
    return None


def executed_state(done, measure_id):
    # done.executed / failed は文字列の並び。施策の id を含むものを探す
    def hit(xs):
        return any(x == measure_id or re.search(re.escape(measure_id) + r"(?!\d)", x or "") for x in xs or [])
    if not done or not measure_id:
        return None
    if hit(done.get("executed")):
        return True
    if hit(done.get("failed")):
        return False
    return None


def rows_for_month(run_dir, month):
    run = read_json(month_file(run_dir, month, "run.json"))
    if not run:
        raise SystemExit(f"{month_file(run_dir, month, 'run.json')} が読めない")
    if not run.get("proposals"):
        raise SystemExit(f"run.json に proposals がない(止まった段: {run.get('stoppedAt', '?')})。台帳には足さない")
    hooks = read_hooks_log(run_dir, month)
    priorities = ((run.get("seen") or {}).get("priorities")) or []
    assessed = (run.get("assessed") or {}).get("assessments") or []
    bill, ruling, done = run.get("bill"), run.get("ruling") or {}, run.get("done")
    rejected = {r.get("bureau"): r.get("reason") for r in (bill or {}).get("rejected") or []}
    rulings = {r.get("measureId"): r for r in ruling.get("rulings") or []}

    rows = []
    for i, bureau in enumerate(BUREAUS):
        p = next((x for x in run["proposals"] if x and x.get("bureau") == bureau), None)
        if p is None and i < len(run["proposals"]) and run["proposals"][i] and not run["proposals"][i].get("bureau"):
            p = run["proposals"][i]
        p = p or {}
        md = read_text(month_file(run_dir, month, f"{bureau}.md")) or ""
        has = bool(p.get("hasProposal"))
        a = next((x for x in assessed if x.get("bureau") == bureau), None)
        measure = find_measure(bill, bureau) if has else None
        mid = measure.get("id") if measure else None
        r = rulings.get(mid) if mid else None
        ok = executed_state(done, mid)
        rows.append({
            "month": int(month),
            "id": f"m{int(month):02d}-{bureau}",
            "bureau": bureau,
            "title": p.get("title", "") if has else "",
            "hasProposal": has,
            "planItems": p.get("planItems") or [],
            "priority": priority_of(md, p.get("planItems") or [], priorities) if has else None,
            "assessment": {"verdict": a.get("verdict"), "reason": a.get("reason")} if a else None,
            "adopted": {"measureId": mid, "reason": None if mid else rejected.get(bureau)},
            "vote": {"needed": bool(measure and measure.get("needsVote")),
                     "verdict": r.get("verdict") if r else None, "point": r.get("point") if r else None},
            # 費用は実際に払った額ではなく、案の建設費(見込み)。払った額は返り値にないため
            "executed": {"ok": ok, "cost": p.get("buildCost") if ok else None},
            "review": None,
            "seenCheck": seen_check(md, hooks, f"council-{bureau}"),
        })
    return rows


def fill_review(rows, run_dir, month):
    # 前の月の行の review を、今月の局の案のファイルから埋める
    filled = []
    for row in rows:
        if row["month"] != int(month) - 1:
            continue
        md = read_text(month_file(run_dir, month, f"{row['bureau']}.md"))
        text = labeled(md, "前の月の答え合わせ") if md else None
        result = judge_review(text)
        if result:
            row["review"] = {"result": result, "reason": " ".join(text.split())}
            filled.append(row["id"])
    return filled


def other_roles(run_dir, month):
    # 局のほかの役の「見たもの」の確かめ(台帳の行はないので、画面に出すだけ)
    hooks = read_hooks_log(run_dir, month)
    agents = {"policy": "council-mayor-desk", "bill": "council-mayor-desk", "bill-2": "council-mayor-desk",
              "guide": "council-finance", "finance": "council-finance",
              "assembly": "council-assembly", "assembly-2": "council-assembly"}
    out = {}
    for name in ROLES:
        md = read_text(month_file(run_dir, month, f"{name}.md"))
        if md:
            out[name] = seen_check(md, hooks, agents[name])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("month", type=int)
    a = ap.parse_args()

    path = Path(a.run_dir) / "council" / "ledger.jsonl"
    old = []
    if path.exists():
        old = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    new = rows_for_month(a.run_dir, a.month)
    rows = [r for r in old if r.get("month") != a.month] + new
    rows.sort(key=lambda r: (r.get("month", 0), BUREAUS.index(r["bureau"]) if r.get("bureau") in BUREAUS else 99))
    filled = fill_review(rows, a.run_dir, a.month)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    replaced = len(old) - len([r for r in old if r.get("month") != a.month])
    print(f"wrote {path}(m{a.month:02d} の {len(new)} 行。置き換えた {replaced} 行。review を埋めた: {', '.join(filled) or 'なし'})")
    for r in new:
        if r["seenCheck"]["unlogged"]:
            print(f"  呼んだ記録のない「見たもの」 {r['id']}: {', '.join(r['seenCheck']['unlogged'])}")
    for name, s in other_roles(a.run_dir, a.month).items():
        if s["unlogged"]:
            print(f"  呼んだ記録のない「見たもの」 m{a.month:02d}-{name}: {', '.join(s['unlogged'])}")


if __name__ == "__main__":
    main()
