"""月の終わりに、議決と実行を記録から突き合わせる(#100。council-design.md の9.1)。

command-log.txt(MOD のパネルのログ)、council/m<月>-hooks.log、council/m<月>-assembly.json を読み、
型から外れたことを Markdown で標準出力に出す。市政ノートの「型から外れたこと」に貼れる形にする。

    python3 code/ai-mayor/tools/check_council_month.py <運営のフォルダ> <月> [--all-log]

command-log.txt は街を開いてからの全部を持つ。その月の分は、hooks の記録の最初と最後の時刻で切る。
--all-log を付けると切らずに全部を見る。
"""

import argparse
import re
import subprocess
from collections import Counter
from datetime import timedelta
from pathlib import Path

from council_common import (BUREAUS, VOTE_TOOLS, mm, month_file, parse_time, read_command_log, read_hooks_log,
                            read_json)

# その月に置いてよい council/ のファイル(interfaces の2)
EXPECTED = ["policy.md", "bill.md", "bill-2.md", "assembly.md", "assembly-2.md",
            "assembly.json", "hooks.log", "run.json", "minutes.md"] + [f"{b}.md" for b in BUREAUS] \
    + [f"survey-{b}.md" for b in BUREAUS]  # 局の調査の結果(#105 の作り直し)
# 運営のフォルダで、変わってよい場所
FREE = [r"mayor-note\.md", r"command-log(-m\d\d-m\d\d)?\.txt", r"log\.md", r"article\.md", r"attempt\d+/.*", r"assets/.*", r"transcripts/.*", r"council/ledger\.jsonl", r"council/plan-[a-z]+\.md", r"council/plan-year\d+/.*", r"council/ledger-recent\.jsonl", r"council/ledger-older\.md",
        r"council/m\d\d-(" + "|".join(re.escape(e) for e in EXPECTED) + r")"]


def month_range(hooks):
    times = [t for t in (parse_time(r["time"]) for r in hooks) if t]
    if not times:
        return None
    # command-log の時刻は道具を終えた時か始めた時かが分からないので、前後に余裕を持たせる
    return min(times) - timedelta(minutes=1), max(times) + timedelta(minutes=10)


def git_changes(run_dir):
    # 運営のフォルダの中で、変わった・増えたファイル(リポジトリの中にあるときだけ)
    try:
        # core.quotepath=false にしないと、日本語のパスが \343\201.. の形になり、相対パスに直せない(#100)
        git = ["git", "-c", "core.quotepath=false"]
        out = subprocess.run(git + ["status", "--porcelain", "--untracked-files=all", "--", "."],
                             cwd=run_dir, capture_output=True, text=True, check=True).stdout
        top = subprocess.run(git + ["rev-parse", "--show-prefix"], cwd=run_dir,
                             capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    paths = []
    for line in out.splitlines():
        p = line[3:].strip().strip('"')
        if " -> " in p:
            p = p.split(" -> ", 1)[1]
        paths.append(p[len(top):] if p.startswith(top) else p)
    return paths


def check(run_dir, month, all_log=False):
    """見つけたことを辞書で返す。議事録のスクリプトからも使う。"""
    run_dir = Path(run_dir)
    hooks = read_hooks_log(run_dir, month)
    ruling = read_json(month_file(run_dir, month, "assembly.json"))
    approved = set((ruling or {}).get("approvedKinds") or [])
    log = read_command_log(run_dir / "command-log.txt")
    span = None if all_log else month_range(hooks)
    if span:
        log = [r for r in log if r["time"] and span[0] <= r["time"] <= span[1]]

    # 議決が要る道具の呼び出し(実際に動いた OK の行)
    vote_calls, unapproved, emergency = [], [], []
    advanced = False
    for r in log:
        if r["tool"] == "advance" and r["kind"] == "OK":
            advanced = True
            continue
        kind = VOTE_TOOLS.get(r["tool"])
        if not kind or r["kind"] != "OK":
            continue
        vote_calls.append(r)
        if advanced:
            emergency.append((kind, r))
        elif kind not in approved:
            unapproved.append((kind, r))

    # 許されていない Write: hooks が止めたもの、置いてはいけない名前のファイル、運営のフォルダの外れた変更
    write_denied = [h for h in hooks if h["tool"] == "Write" and h["result"] == "deny"]
    cdir = run_dir / "council"
    pre = f"m{mm(month)}-"
    stray = sorted(p.name for p in cdir.glob(pre + "*") if p.name[len(pre):] not in EXPECTED) if cdir.exists() else []
    changes = git_changes(run_dir)
    # council/ の決まりにない名前は stray で数えたので、ここでは重ねない
    outside = None if changes is None else [p for p in changes if not any(re.fullmatch(f, p) for f in FREE)
                                            and p not in {f"council/{x}" for x in stray}]

    # hooks の記録で、実行する市長のほかが議決の要る道具を呼んだ跡
    other_vote = [h for h in hooks if VOTE_TOOLS.get(h["tool"]) and h["result"] in ("ok", "ng")
                  and h["agent"] != "council-mayor-field"]

    denies = [h for h in hooks if h["result"] == "deny"]
    return {
        "month": int(month), "span": span, "approved": sorted(approved), "hasRuling": ruling is not None,
        "voteCalls": vote_calls, "unapproved": unapproved, "emergency": emergency,
        "writeDenied": write_denied, "stray": stray, "outside": outside, "otherVote": other_vote,
        "denies": denies, "warns": [h for h in hooks if h["result"] == "warn"],
        "hooksLines": len(hooks), "logLines": len(log),
    }


def render(f):
    m = mm(f["month"])
    out = [f"### 型から外れたことの確かめ(m{m}、check_council_month.py)", ""]
    if f["span"]:
        a, b = f["span"]
        out.append(f"- 見た範囲: command-log.txt の {a:%Y-%m-%d %H:%M}〜{b:%H:%M}(hooks の記録の時刻から)、道具の行 {f['logLines']}")
    else:
        out.append(f"- 見た範囲: command-log.txt の全部(道具の行 {f['logLines']})")
    out.append(f"- 議会が可決した種類: {'、'.join(f['approved']) or 'なし'}"
               + ("" if f["hasRuling"] else "(assembly.json がない)"))
    out.append(f"- 議決が要る道具の呼び出し: {len(f['voteCalls'])} 回")
    out.append(f"- 議決のない呼び出し: {len(f['unapproved'])} 回")
    out.append(f"- 臨時(advance の後)の呼び出し: {len(f['emergency'])} 回")
    n_write = len(f["writeDenied"]) + len(f["stray"]) + len(f["outside"] or [])
    out.append(f"- 許されていない Write: {n_write} 件")
    out.append(f"- hooks の拒否: {len(f['denies'])} 回")
    out.append("")

    def lines(title, items, fmt):
        if items:
            out.append(f"#### {title}")
            out.append("")
            out.extend("- " + fmt(x) for x in items)
            out.append("")

    lines("議決のない呼び出し", f["unapproved"], lambda x: f"{x[1]['raw_time']}({x[1]['game']}) {x[0]}: `{x[1]['text']}`")
    lines("臨時(advance の後)の呼び出し", f["emergency"], lambda x: f"{x[1]['raw_time']}({x[1]['game']}) {x[0]}: `{x[1]['text']}`")
    lines("実行する市長のほかが議決の要る道具を呼んだ跡(hooks の記録)", f["otherVote"],
          lambda h: f"{h['time']} {h['agent']} `{h['tool']}` {h['result']}")
    lines("hooks が止めた Write", f["writeDenied"], lambda h: f"{h['time']} {h['agent']}: {h['detail']}")
    lines("council/ にある、決まりにない名前のファイル", f["stray"], lambda p: f"`{p}`")
    if f["outside"] is None:
        out += ["- 運営のフォルダの変更は確かめていない(git で読めなかった)", ""]
    else:
        lines("運営のフォルダで、決まりの外の変更(git status)", f["outside"], lambda p: f"`{p}`")
    if f["denies"]:
        out += ["#### hooks の拒否", ""]
        for (agent, tool), n in Counter((h["agent"], h["tool"]) for h in f["denies"]).most_common():
            out.append(f"- {agent} `{tool}`: {n} 回")
        out.append("")
        out += [f"- {h['time']} {h['agent']} `{h['tool']}`: {h['detail']}" for h in f["denies"]]
        out.append("")
    lines("確かめずに通したもの(MOD に届かなかった)", f["warns"], lambda h: f"{h['time']} {h['agent']} `{h['tool']}`")
    return "\n".join(out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("month", type=int)
    ap.add_argument("--all-log", action="store_true")
    a = ap.parse_args()
    print(render(check(a.run_dir, a.month, a.all_log)), end="")


if __name__ == "__main__":
    main()
