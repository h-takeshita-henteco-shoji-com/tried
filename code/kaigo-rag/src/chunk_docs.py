"""告示・省令・通知のテキストを、見出しをたどってチャンクに切る。

入力: data/raw/roken_<uid>.txt(全老健 法令・Q&A検索システムから取得した本文)
出力: data/chunks_docs.jsonl
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"

# uid -> (種類, 略称, 正式名, 版の目安)
DOCS = {
    11: ("告示", "告示19号", "指定居宅サービスに要する費用の額の算定に関する基準", "R8.3"),
    22: ("告示", "告示95号", "厚生労働大臣が定める基準", "R8.3"),
    14: ("告示", "告示94号", "厚生労働大臣が定める基準に適合する利用者等", "R6.3"),
    6: ("省令", "省令37号", "指定居宅サービス等の事業の人員、設備及び運営に関する基準", "R6.12"),
    19: ("通知", "老企25号", "指定居宅サービス等及び指定介護予防サービス等に関する基準について", "R6.7"),
    17: ("通知", "老企36号", "指定居宅サービスに要する費用の額の算定に関する基準…の制定に伴う実施上の留意事項について", "R8.3"),
}

NUM = "0-9０-９"
KAN = "一二三四五六七八九十百"
# (level, pattern)。小さい level ほど上位。
HEADINGS = [
    (0, re.compile(rf"^第[{KAN}]+章　")),
    (1, re.compile(rf"^第[{KAN}]+節　")),
    (2, re.compile(rf"^第[{KAN}]+条(の[{KAN}]+)?　")),
    (2, re.compile(rf"^第[{KAN}]+　")),
    (2, re.compile(r"^別表")),
    (2, re.compile(rf"^[{KAN}]+　")),  # 告示の号(一、二、…)
    (3, re.compile(rf"^[{NUM}]+　")),
    (4, re.compile(rf"^[\(（][{NUM}]+[\)）]　")),
]
# チャンクを分けるときの小さな境目
MINOR = re.compile(rf"^([①-⑳]|[イロハニホヘトチリヌルヲワカヨタレソツネナラム]　|注[{NUM}]*　|[\(（][{KAN}]+[\)）]　)")

MAX_CHARS = 900
TARGET = 600


def body_lines(text: str) -> list[str]:
    lines = [l.strip().replace("　", "　") for l in text.splitlines()]
    start = next(i for i, l in enumerate(lines) if l.startswith("更新日："))
    end = next((i for i, l in enumerate(lines) if "ページトップへ" in l), len(lines))
    return [l for l in lines[start + 1 : end] if l]


def heading_level(line: str):
    for lv, pat in HEADINGS:
        if pat.match(line):
            return lv
    return None


def split_sentences(line: str) -> list[str]:
    """MAX_CHARS を超える1行を、句点で分ける。"""
    if len(line) <= MAX_CHARS:
        return [line]
    out, cur = [], ""
    for s in re.split(r"(?<=。)", line):
        if cur and len(cur) + len(s) > TARGET:
            out.append(cur)
            cur = ""
        cur += s
    if cur:
        out.append(cur)
    return out


def split_long(lines: list[str]) -> list[list[str]]:
    """長い節を、小さな境目か段落で TARGET 字前後に分ける。"""
    lines = [s for l in lines for s in split_sentences(l)]
    parts, cur, size = [], [], 0
    for l in lines:
        if cur and size >= TARGET and (MINOR.match(l) or size + len(l) > MAX_CHARS):
            parts.append(cur)
            cur, size = [], 0
        cur.append(l)
        size += len(l)
    if cur:
        parts.append(cur)
    return parts


def chunk_doc(uid: int):
    kind, short, name, ver = DOCS[uid]
    lines = body_lines((RAW / f"roken_{uid}.txt").read_text())
    stack: dict[int, str] = {}
    sections: list[tuple[list[str], list[str]]] = []  # (path, lines)
    cur: list[str] = []
    cur_path: list[str] = []
    for l in lines:
        lv = heading_level(l)
        if lv is not None:
            if cur:
                sections.append((cur_path, cur))
            stack = {k: v for k, v in stack.items() if k < lv}
            stack[lv] = l[:60]
            cur_path = [stack[k] for k in sorted(stack)]
            cur = [l]
        else:
            cur.append(l)
    if cur:
        sections.append((cur_path, cur))

    # 見出しだけの小さな節は、次の節の頭に寄せる
    merged, carry = [], []
    for path, sec in sections:
        if sum(len(x) for x in sec) < 80:
            carry += sec
            continue
        merged.append((path, carry + sec))
        carry = []
    if carry:
        merged.append((sections[-1][0], carry))

    out = []
    for path, sec in merged:
        text_len = sum(len(x) for x in sec)
        pieces = split_long(sec) if text_len > MAX_CHARS else [sec]
        for j, p in enumerate(pieces):
            out.append(
                {
                    "doc_type": kind,
                    "doc": short,
                    "doc_name": name,
                    "version": ver,
                    "current": 1,
                    "path": " > ".join(path),
                    "part": j,
                    "text": "\n".join(p),
                }
            )
    return out


def main():
    allc = []
    for uid in DOCS:
        cs = chunk_doc(uid)
        print(DOCS[uid][1], len(cs), "chunks", "avg", sum(len(c["text"]) for c in cs) // len(cs))
        allc += cs
    with open(ROOT / "data" / "chunks_docs.jsonl", "w") as f:
        for c in allc:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print("total", len(allc))


if __name__ == "__main__":
    main()
