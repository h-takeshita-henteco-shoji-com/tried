"""1か月の会議を、時間の順に1本の議事録 council/m<月>-minutes.md にする(#100。council-design.md の9.5)。

各役のファイル、run.json、hooks の記録、台帳をつなぐだけで、新しい判断は書かない。
AI に要約させない(要約で細部が消えるため)。長い欄は、元のファイルへの相対リンクにする。

    python3 code/ai-mayor/tools/make_council_minutes.py <運営のフォルダ> <月>
"""

import argparse
import json
import re
from pathlib import Path

from check_council_month import check, render
from council_common import (BUREAU_NAMES, BUREAUS, THREE, find_section, month_file, parse_time, read_hooks_log,
                            read_json, read_text)

LONG_LINES = 12    # これより長い欄はリンクにする
LONG_CHARS = 900


def anchor(title):
    # GitHub の見出しのリンク。日本語はそのまま使える
    return "#" + title.strip().lower().replace(" ", "-")


def quote_or_link(md, title, fname, label=None):
    """欄が短ければそのまま引き、長ければリンクにする。欄がなければ「(書いていない)」"""
    body = find_section(md, title) if md else None
    label = label or title
    if body is None:
        return [f"- {label}: (書いていない)"]
    lines = [x for x in body.splitlines() if x.strip()]
    if len(lines) > LONG_LINES or len(body) > LONG_CHARS:
        return [f"- {label}: [{fname} の「{title}」]({fname}{anchor(title)})({len(lines)} 行)"]
    if not lines:
        return [f"- {label}: (空)"]
    return [f"- {label}:", ""] + ["  " + x for x in lines] + [""]


def span_of(hooks, agents):
    # hooks の記録から、その役が道具を呼んだ時刻の幅
    ts = [parse_time(h["time"]) for h in hooks if h["agent"] in agents]
    ts = [t for t in ts if t]
    if not ts:
        return ""
    return f"(hooks の記録で {min(ts):%H:%M}〜{max(ts):%H:%M})"


def file_link(run_dir, month, suffix):
    p = month_file(run_dir, month, suffix)
    return f"[{p.name}]({p.name})" if p.exists() else f"{p.name}(ない)"


def build(run_dir, month):
    run_dir = Path(run_dir)
    m = f"{int(month):02d}"
    run = read_json(month_file(run_dir, month, "run.json")) or {}
    hooks = read_hooks_log(run_dir, month)
    md = {s: read_text(month_file(run_dir, month, f"{s}.md"))
          for s in ["policy", "guide", "finance", "bill", "bill-2", "assembly", "assembly-2"] + BUREAUS}
    out = [f"# {int(month)}か月目の議事録", "",
           "make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。",
           "長い欄は元のファイルへのリンクにした。", ""]
    if run.get("stoppedAt"):
        out += [f"- Workflow は「{run['stoppedAt']}」の段で止まった", ""]

    # 1. 市長: 見た数字と、編成方針の重点
    seen = run.get("seen") or {}
    out += [f"## 1. 市長: 見た数字と編成方針{span_of(hooks, {'council-mayor-desk'})}", "",
            f"- 元のファイル: {file_link(run_dir, month, 'policy.md')}",
            f"- ゲーム内の日付: {seen.get('gameDate', '?')}、保存: {seen.get('saveName', '?')}",
            "- 重点: " + ("、".join(seen.get("priorities") or []) or "(なし)")]
    if seen.get("stop"):
        out.append(f"- 止まるべき: {seen.get('stopReason')}")
    out.append("")
    for t in THREE:
        out += quote_or_link(md["policy"], t, f"m{m}-policy.md")
    out.append("")

    # 2. 財政局: 今月の枠
    g = run.get("guide") or {}
    out += [f"## 2. 財政局: 今月の枠{span_of(hooks, {'council-finance'})}", "",
            f"- 元のファイル: {file_link(run_dir, month, 'guide.md')}"]
    if g:
        out.append(f"- 建設費の上限 {g.get('buildCap')}、週の維持費の増えの上限 {g.get('upkeepCap')}、"
                   f"税の幅 ±{g.get('taxRange')}、予算の幅 ±{g.get('budgetRange')}")
    out.append("")

    # 3. 7つの局: 案と、見たもの・判断の根拠・捨てたもの
    out += ["## 3. 7つの局の案", ""]
    props = {p.get("bureau"): p for p in run.get("proposals") or [] if p}
    for b in BUREAUS:
        p = props.get(b) or {}
        name = BUREAU_NAMES[b]
        out += [f"### {name}({b}){span_of(hooks, {f'council-{b}'})}", "",
                f"- 元のファイル: {file_link(run_dir, month, f'{b}.md')}"]
        if p.get("hasProposal"):
            out += [f"- 案: {p.get('title')}",
                    f"- 建設費 {p.get('buildCost')}、週の維持費 +{p.get('upkeepPerWeek')}、"
                    f"{'戻せる' if p.get('reversible') else '戻せない'}",
                    "- 市の計画: " + ("、".join(p.get("planItems") or []) or "(なし)"),
                    f"- 議決: {'要る(' + p.get('voteKind', '') + ')' if p.get('needsVote') else '要らない'}"]
        elif p:
            out.append("- 案: なし")
        else:
            out.append("- 返り値がない")
        out.append("")
        for t in THREE:
            out += quote_or_link(md[b], t, f"m{m}-{b}.md")
        out.append("")

    # 4. 財政局: 査定
    a = run.get("assessed")
    out += ["## 4. 財政局: 査定", ""]
    if a:
        out.append(f"- 元のファイル: {file_link(run_dir, month, 'finance.md')}")
        for x in a.get("assessments") or []:
            out.append(f"- {BUREAU_NAMES.get(x.get('bureau'), x.get('bureau'))}: {x.get('verdict')}。{x.get('reason')}")
        tp = a.get("taxProposal") or {}
        out.append(f"- 税の案: {tp.get('summary') if tp.get('exists') else 'なし'}")
        out.append(f"- 市長が選ぶときの上限: {a.get('totalCap')}")
        out.append("")
        for t in THREE:
            out += quote_or_link(md["finance"], t, f"m{m}-finance.md")
    else:
        out.append("- 査定はなかった(7つとも案なし、または止まった)")
    out.append("")

    # 5. 市長: 採った施策と採らなかった案
    bill = run.get("bill")
    out += ["## 5. 市長: 採った施策と採らなかった案", ""]
    if bill:
        out.append(f"- 元のファイル: {file_link(run_dir, month, 'bill.md')}"
                   + (f"、直した議案 {file_link(run_dir, month, 'bill-2.md')}" if md["bill-2"] else ""))
        for x in bill.get("measures") or []:
            vote = f"議決が要る({x.get('voteKind')})" if x.get("needsVote") else "議決は要らない"
            out.append(f"- 採った {x.get('id')}: {x.get('title')}(元 {BUREAU_NAMES.get(x.get('fromBureau'), x.get('fromBureau'))}、{vote})")
        for x in bill.get("rejected") or []:
            out.append(f"- 採らなかった {BUREAU_NAMES.get(x.get('bureau'), x.get('bureau'))}: {x.get('reason')}")
        out.append("")
        last = "bill-2" if md["bill-2"] else "bill"
        for t in THREE:
            out += quote_or_link(md[last], t, f"m{m}-{last}.md")
    else:
        out.append("- まとめはなかった")
    out.append("")

    # 6. 議会: 可決と否決
    ruling = run.get("ruling")
    aj = read_json(month_file(run_dir, month, "assembly.json"))
    out += [f"## 6. 議会: 可決と否決{span_of(hooks, {'council-assembly'})}", ""]
    if ruling or aj:
        out.append(f"- 元のファイル: {file_link(run_dir, month, 'assembly.md')}"
                   + (f"、2回目 {file_link(run_dir, month, 'assembly-2.md')}" if md["assembly-2"] else ""))
        for r in (ruling or aj or {}).get("rulings") or []:
            pt = f"(点 {r.get('point')})" if r.get("point") else ""
            out.append(f"- {r.get('measureId')} {r.get('kind', '')}: {r.get('verdict')}{pt}。{r.get('reason')}")
        out.append("- 可決した種類(hooks が見る): " + ("、".join((aj or {}).get("approvedKinds") or []) or "なし"))
        out.append("")
        last = "assembly-2" if md["assembly-2"] else "assembly"
        for t in THREE:
            out += quote_or_link(md[last], t, f"m{m}-{last}.md")
    else:
        out.append("- 議案はなかった")
    out.append("")

    # 7. 実行する市長: 実行の結果、見回り、臨時
    done = run.get("done") or {}
    out += [f"## 7. 実行する市長: 実行と見回り{span_of(hooks, {'council-mayor-field'})}", "",
            "- 実行してよい施策: " + ("、".join(run.get("allowed") or []) or "なし"),
            "- 実行した: " + ("、".join(done.get("executed") or []) or "なし"),
            "- 失敗した: " + ("、".join(done.get("failed") or []) or "なし"),
            f"- 臨時: {'あり' if done.get('emergency') else 'なし'}"]
    if done.get("stop"):
        out.append(f"- 止まった: {done.get('stopReason')}")
    for p in done.get("patrols") or []:
        out.append(f"- 見回り {p.get('gameDate')}: 人口 {p.get('population')}、所持金 {p.get('money')}、"
                   f"週の収支 {p.get('weeklyBalance')}、幸福度 {p.get('happiness')}" + ("、警報あり" if p.get("alert") else ""))
    rep = (done.get("report") or "").strip()
    if rep:
        if len(rep) > LONG_CHARS:
            out.append(f"- 報告: 長いので [市政ノート](../mayor-note.md) を見る({len(rep)} 字)")
        else:
            out += ["- 報告:", ""] + ["  " + x for x in rep.splitlines() if x.strip()]
    out.append("")

    # 8. hooks の拒否と、型から外れたこと
    out += ["## 8. hooks の拒否と、型から外れたこと", ""]
    out.append(render(check(run_dir, month)))

    # 台帳へのリンク
    ledger = run_dir / "council" / "ledger.jsonl"
    if ledger.exists():
        n = sum(1 for x in ledger.read_text(encoding="utf-8").splitlines() if x.strip() and json.loads(x).get("month") == int(month))
        out += ["", f"台帳: [ledger.jsonl](ledger.jsonl)(この月の行 {n})"]
    # 空行が3つ以上続くところは2つにする
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("month", type=int)
    a = ap.parse_args()
    path = month_file(a.run_dir, a.month, "minutes.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build(a.run_dir, a.month), encoding="utf-8")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
