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

ROLES = ["policy", "bill", "bill-2", "assembly", "assembly-2"]


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


def find_measure(bill, proposal_id):
    # 施策の fromBureau は、元にした案の id(カンマ区切りで複数)。案の id が含まれる施策を探す(#124)
    for m in (bill or {}).get("measures") or []:
        sources = [x.strip() for x in str(m.get("fromBureau") or "").split(",")]
        if proposal_id in sources:
            return m
    return None


def proposal_section(md, proposal_id):
    """局の案のファイルから、その案の「## 案<番号>」の節を返す。案が1件だけの古い形(節なし)は全体を返す。"""
    if not md:
        return md
    parts = re.split(r"(?m)^(?=##\s*案\d)", md)
    sections = [x for x in parts if re.match(r"##\s*案\d", x)]
    if not sections:
        return md
    n = proposal_id.rsplit("-", 1)[-1]
    for sec in sections:
        if re.search(r"案の id[:：]\s*" + re.escape(proposal_id) + r"(?!\d)", sec) or re.match(r"##\s*案" + re.escape(n) + r"\b", sec):
            return sec
    return None


def failed_reason(done, measure_id):
    # 実行する市長が返した、打てなかった理由(#105)。翌月の局が読む
    for r in (done or {}).get("failedReasons") or []:
        if r.get("id") == measure_id:
            return r.get("reason")
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
    rejected = {r.get("proposal") or r.get("bureau"): r.get("reason") for r in (bill or {}).get("rejected") or []}
    rulings = {r.get("measureId"): r for r in ruling.get("rulings") or []}

    rows = []
    for i, bureau in enumerate(BUREAUS):
        p = next((x for x in run["proposals"] if x and x.get("bureau") == bureau), None)
        if p is None and i < len(run["proposals"]) and run["proposals"][i] and not run["proposals"][i].get("bureau"):
            p = run["proposals"][i]
        p = p or {}
        md = read_text(month_file(run_dir, month, f"{bureau}.md")) or ""
        # 案ごとに1行。案がない局は、案なしの1行
        items = p.get("proposals") or []
        if not items:
            items = [{"id": None}]
        for k, item in enumerate(items, 1):
            has = item.get("id") is not None
            pid = item.get("id") or f"{bureau}-{k}"
            sec = proposal_section(md, pid) if has else md
            a = next((x for x in assessed if x.get("proposalId") == pid), None) if has else None
            if has and a is None:
                a = next((x for x in assessed if x.get("bureau") == bureau and not x.get("proposalId")), None)
            measure = find_measure(bill, pid) if has else None
            mid = measure.get("id") if measure else None
            r = rulings.get(mid) if mid else None
            ok = executed_state(done, mid)
            rows.append({
                "month": int(month),
                "id": f"m{int(month):02d}-{pid}" if has else f"m{int(month):02d}-{bureau}",
                "proposalId": pid if has else None,
                "bureau": bureau,
                "title": item.get("title", "") if has else "",
                "hasProposal": has,
                "planItems": item.get("planItems") or [],
                "priority": priority_of(sec or "", item.get("planItems") or [], priorities) if has else None,
                "assessment": {"verdict": a.get("verdict"), "reason": a.get("reason")} if a else None,
                "adopted": {"measureId": mid, "reason": None if mid else rejected.get(pid)},
                "vote": {"needed": bool(measure and measure.get("needsVote")),
                         "verdict": r.get("verdict") if r else None, "point": r.get("point") if r else None},
                # 費用は実際に払った額ではなく、案の建設費(見込み)。払った額は返り値にないため
                "executed": {"ok": ok, "cost": item.get("buildCost") if ok else None,
                             "reason": failed_reason(done, mid) if ok is False else None},
                "review": None,
                "seenCheck": seen_check(md, hooks, f"council-{bureau}") if k == 1 else {"claimed": [], "unlogged": []},
            })
    return rows


def fill_review(rows, run_dir, month):
    # 前の月の行の review を、今月の局の案のファイルから埋める
    filled = []
    for row in rows:
        if row["month"] != int(month) - 1:
            continue
        md = read_text(month_file(run_dir, month, f"{row['bureau']}.md"))
        # 前の月の案の答え合わせは、今月の同じ局の案のどれかに書かれる。案が複数あるときは、前の月の案の id が出てくる節を探す
        text = None
        if md:
            for sec in re.split(r"(?m)^(?=##\s*案\d)", md):
                if row.get("proposalId") and row["proposalId"] in sec and labeled(sec, "前の月の答え合わせ"):
                    text = labeled(sec, "前の月の答え合わせ")
                    break
            if text is None:
                text = labeled(md, "前の月の答え合わせ")
        result = judge_review(text)
        if result:
            row["review"] = {"result": result, "reason": " ".join(text.split())}
            filled.append(row["id"])
    return filled


def other_roles(run_dir, month):
    # 局のほかの役の「見たもの」の確かめ(台帳の行はないので、画面に出すだけ)
    hooks = read_hooks_log(run_dir, month)
    agents = {"policy": "council-mayor-desk", "bill": "council-mayor-desk", "bill-2": "council-mayor-desk",
              "assembly": "council-assembly", "assembly-2": "council-assembly"}
    out = {}
    for name in ROLES:
        md = read_text(month_file(run_dir, month, f"{name}.md"))
        if md:
            out[name] = seen_check(md, hooks, agents[name])
    return out


def write_views(path, rows, month):
    """文脈を軽くするため、台帳の読みやすい写しを2つ作る(#124)。
    ledger-recent.jsonl: 直近3か月(今月を含む)の行。ledger-older.md: それより前の案の、1行ずつの要約。
    局と市長は、全部の台帳ではなく、この2つを読む。"""
    recent = [r for r in rows if r.get("month", 0) > month - 3]
    older = [r for r in rows if r.get("month", 0) <= month - 3 and r.get("hasProposal")]
    d = path.parent
    (d / "ledger-recent.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recent), encoding="utf-8")
    lines = ["# 台帳の要約(直近3か月より前)", "",
             "1行が1案。採られたか、打てたか、理由(60字まで)。全部の行は ledger.jsonl にある。", ""]
    for r in older:
        adopted = (r.get("adopted") or {})
        ex = (r.get("executed") or {})
        state = "採用" if adopted.get("measureId") else "不採用"
        if ex.get("ok") is True:
            state += "・実行できた"
        elif ex.get("ok") is False:
            state += "・打てなかった"
        why = (adopted.get("reason") or ex.get("reason") or "").replace("\n", " ")[:60]
        lines.append(f"- {r.get('id')} ({r.get('bureau')}) {str(r.get('title'))[:30]}: {state}" + (f"。{why}" if why else ""))
    (d / "ledger-older.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    rows.sort(key=lambda r: (r.get("month", 0), BUREAUS.index(r["bureau"]) if r.get("bureau") in BUREAUS else 99, r.get("proposalId") or ""))
    filled = fill_review(rows, a.run_dir, a.month)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    write_views(path, rows, a.month)
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
