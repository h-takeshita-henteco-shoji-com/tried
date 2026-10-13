"""文と段落に番号を振る。

区切りの決まりは measures.md の「文と段落に番号を振る」に従う。
- 文は「。」「!」「?」と改行で区切る。かぎかっこの中の「。」では区切らない
- 段落は空行で区切る。1行目は題(t00)
- 位置は、その文が始まる文字数 ÷ 本文の総文字数(空白と改行は数えない)

入力: 1行目が題、空行のあと本文のテキストファイル
"""
import re
import sys

ENDS = "。！？!?"
OPEN = "「『(（"
CLOSE = "」』)）"


def split_sentences(par):
    out, buf, depth = [], "", 0
    for ch in par:
        if ch == "\n":
            if buf.strip():
                out.append(buf.strip())
            buf = ""
            continue
        buf += ch
        if ch in OPEN:
            depth += 1
        elif ch in CLOSE:
            depth = max(0, depth - 1)
        elif ch in ENDS and depth == 0:
            out.append(buf.strip())
            buf = ""
    if buf.strip():
        out.append(buf.strip())
    # 閉じかっこだけが残った文は、前の文に付ける
    merged = []
    for s in out:
        if merged and all(c in CLOSE + ENDS for c in s):
            merged[-1] += s
        else:
            merged.append(s)
    return merged


def nchars(s):
    return len(re.sub(r"\s", "", s))


def load(path):
    text = open(path, encoding="utf-8").read()
    title, body = text.split("\n", 1)
    pars = [p for p in re.split(r"\n\s*\n", body.strip()) if p.strip()]
    sents = []
    for pi, p in enumerate(pars, 1):
        for s in split_sentences(p):
            sents.append({"par": pi, "text": s})
    total = sum(nchars(s["text"]) for s in sents)
    pos = 0
    for i, s in enumerate(sents, 1):
        s["id"] = f"s{i:03d}"
        s["pos"] = pos / total * 100
        s["len"] = nchars(s["text"])
        pos += s["len"]
    return {"title": title.strip(), "sents": sents, "npar": len(pars), "total": total}


if __name__ == "__main__":
    d = load(sys.argv[1])
    print(f"t00\t\t\t{d['title']}")
    for s in d["sents"]:
        print(f"{s['id']}\tp{s['par']:02d}\t{s['pos']:.1f}\t{s['text']}")
