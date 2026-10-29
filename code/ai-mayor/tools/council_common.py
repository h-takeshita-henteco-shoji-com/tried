"""市役所と議会のハーネスの、確かめと記録のスクリプトが共に使う読み方(#100)。

形は code/ai-mayor/mayor/council-interfaces.md に合わせる。
check_council_month.py、make_council_ledger.py、make_council_minutes.py から読み込む。
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

# 案を出す局。並びは council-interfaces.md の1のとおり
BUREAUS = ["urban", "roads", "port", "economy", "health", "education", "fire", "finance"]
BUREAU_NAMES = {
    "finance": "財政局", "urban": "住宅都市みどり局", "roads": "道路下水道局", "port": "港湾空港局",
    "economy": "経済観光文化局", "health": "保健環境局", "education": "教育委員会", "fire": "消防局",
}

# 議決が要る道具と、その種類(council-interfaces.md の4)
VOTE_TOOLS = {
    "set_tax": "税",
    "set_budget": "予算", "set_transport_line_budget": "予算",
    "take_loan": "融資",
    "bulldoze": "取り壊し", "remove_line": "取り壊し", "remove_transport_line": "取り壊し",
}

MCP_PREFIX = "mcp__cities-skylines__"
THREE = ["見たもの", "判断の根拠", "捨てたもの"]


def mm(month):
    return f"{int(month):02d}"


def council_dir(run_dir):
    return Path(run_dir) / "council"


def month_file(run_dir, month, suffix):
    # 例: suffix="assembly.json" → council/m03-assembly.json
    return council_dir(run_dir) / f"m{mm(month)}-{suffix}"


def read_json(path):
    # 読めなければ None
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return None


def read_hooks_log(run_dir, month):
    """hooks の記録を辞書の並びで返す。形は council-interfaces.md の6(タブ区切り5列)。"""
    rows = []
    text = read_text(month_file(run_dir, month, "hooks.log")) or ""
    for line in text.splitlines():
        cols = line.split("\t")
        if len(cols) < 4:
            continue
        cols += [""] * (5 - len(cols))
        rows.append({"time": cols[0], "agent": cols[1], "tool": cols[2], "result": cols[3], "detail": cols[4]})
    return rows


def parse_time(s):
    # hooks.log は ISO8601(時差つき)、command-log.txt は「YYYY-MM-DD HH:MM:SS」の手元の時刻。手元の時刻にそろえる
    try:
        t = datetime.fromisoformat(s.strip().replace(" ", "T", 1))
    except ValueError:
        return None
    return t.astimezone().replace(tzinfo=None) if t.tzinfo else t


def read_command_log(path):
    """command-log.txt の道具の行(OK と NG)を返す。形: 実時間<TAB>ゲーム内の日付<TAB>種類<TAB>内容"""
    rows = []
    text = read_text(path) or ""
    for line in text.lstrip("﻿").splitlines():
        if line.startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) < 4 or cols[2] not in ("OK", "NG"):
            continue
        tool = cols[3].split(" ", 1)[0]
        rows.append({"time": parse_time(cols[0]), "raw_time": cols[0], "game": cols[1], "kind": cols[2],
                     "tool": tool, "text": cols[3]})
    return rows


def sections(md, level=2):
    """Markdown を見出し(## の段)ごとに切る。{見出し: 本文} を返す。同じ見出しは後のものを使う。"""
    out, name, buf = {}, None, []
    mark = "#" * level + " "
    in_code = False
    for line in (md or "").splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith(mark):
            if name is not None:
                out[name] = "\n".join(buf).strip()
            name, buf = line[len(mark):].strip(), []
        elif name is not None:
            buf.append(line)
    if name is not None:
        out[name] = "\n".join(buf).strip()
    return out


def find_section(md, title):
    # 見出しの段は問わない。見出しの頭が title で始まれば当たりとする(「見たもの(数字)」なども拾う)
    for level in (2, 3, 4):
        for k, v in sections(md, level).items():
            if k.startswith(title):
                return v
    return None


def seen_tools(md):
    """「見たもの」の行の頭の `道具` を拾う(council-interfaces.md の9)。重ねずに出た順で返す。"""
    body = find_section(md, "見たもの") or ""
    tools = []
    for line in body.splitlines():
        m = re.match(r"\s*[-*]\s*`([^`]+)`", line)
        if m:
            name = m.group(1).strip().replace(MCP_PREFIX, "")
            name = re.split(r"[\s(]", name, 1)[0]
            if name and name not in tools:
                tools.append(name)
    return tools


def labeled(md, label):
    """「施策: ...」「- **費用**: ...」「## 費用」などの形で書かれた欄の中身を返す。なければ None。"""
    sec = find_section(md, label)
    if sec is not None:
        return sec
    lines = (md or "").splitlines()
    pat = re.compile(r"^(\s*)(?:[-*]\s*)?(?:\*\*)?" + re.escape(label) + r"(?:\*\*)?\s*[:：]?(?:\*\*)?\s*(.*)$")
    for i, line in enumerate(lines):
        m = pat.match(line)
        if not m:
            continue
        indent, out = len(m.group(1)), [m.group(2).strip()]
        # 続く字下げの行(箇条書きの子)も中身に含める
        for nxt in lines[i + 1:]:
            if nxt.strip() and len(nxt) - len(nxt.lstrip()) > indent:
                out.append(nxt.strip())
            else:
                break
        return "\n".join(x for x in out if x)
    return None


def judge_review(text):
    """答え合わせの文から 当たり / 外れ / 半分 を読む。読めなければ None。"""
    if not text:
        return None
    first = text.strip().splitlines()[0] if text.strip() else ""
    for line in [first, text]:
        if re.search(r"半分|一部", line):
            return "半分"
        if re.search(r"外れ", line):
            return "外れ"
        if re.search(r"当たり|当たった", line):
            return "当たり"
    return None


def rel(path, base):
    # base から見た相対パス(リンク用)
    return os.path.relpath(path, base)
