"""8本の本文を、1行目が題、空行のあと本文のテキストにそろえる。

- 原文の A〜C は出典から取り直す。D は 10-08 の article.md から取る
- 書き直しは #47 の rewrites/ から取る
- 見出し、箇条書き、表の行も、読者が読む文として残す

使い方: python prepare.py <リポジトリの 2026 フォルダ> <出力先>
"""
import glob
import html
import os
import re
import sys
import urllib.parse
import urllib.request

A_URL = "https://ja.wikisource.org/w/index.php?title=" + urllib.parse.quote(
    "プログラマが知るべき97のこと/コードは設計である") + "&action=raw"
B_URL = "https://www.aozora.gr.jp/cards/000042/files/2359_13797.html"
C_URL = "https://www.jma.go.jp/jma/kishou/know/toppuu/tornado1-1.html"


def fetch(url, encoding):
    req = urllib.request.Request(url, headers={"User-Agent": "tried-yardstick"})
    with urllib.request.urlopen(req) as r:
        return r.read().decode(encoding)


def strip_tags(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s)


def a_orig():
    raw = fetch(A_URL, "utf-8")
    body = raw[raw.index("想像してみてください"):]
    body = re.sub(r"\n*\{\{.*", "", body, flags=re.S)
    return "コードは設計である", body


def b_orig():
    s = fetch(B_URL, "cp932")
    t = re.search(r'<div class="main_text">(.*?)<div class="bibliographical_information">', s, re.S).group(1)
    t = re.sub(r"<rp>.*?</rp>|<rt>.*?</rt>", "", t)  # ルビ(読み仮名)を除く
    t = strip_tags(t).replace("　", "")
    t = t[:t.rfind("（昭和八年")]
    pars = [x.strip() for x in t.split("\n") if x.strip()]
    return "科学者とあたま", "\n\n".join(pars)


def c_orig():
    s = fetch(C_URL, "utf-8")
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    i = s.index("発達した積乱雲からは")
    lead = strip_tags(s[i:s.index("主な突風の種類</", i)])
    pars = [re.sub(r"\s+", "", x) for x in re.split(r"</p>|\n\s*\n", lead) if x.strip()]
    pars = [p for p in pars if p]
    # 表の各行を「種類:特徴」の1段落にする。説明図(画像だけのセル)は除く
    table = s[s.index("<table", i):s.index("</table>", i)]
    for tr in re.findall(r"<tr.*?</tr>", table, re.S):
        cells = [re.sub(r"\s+", "", strip_tags(c)) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        cells = [c for c in cells if c]
        if len(cells) == 2:
            pars.append("：".join(cells))
    return "竜巻などの激しい突風とは", "\n\n".join(pars)


def md2txt(md):
    """Markdown を、題と本文に直す。"""
    title, out, incode = None, [], False
    for line in md.split("\n"):
        if line.startswith("```"):
            incode = not incode
            continue
        if incode:
            continue
        if title is None and line.startswith("# "):
            title = line[2:].strip()
            continue
        if title is None and re.match(r"^\*\*.*\*\*$", line.strip()):
            title = line.strip().strip("*")
            continue
        if re.match(r"^\|[-| :]+\|$", line.strip()):
            continue
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            line = "：".join(cells) + ("" if cells[-1].endswith("。") else "。")
        line = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", line)
        line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
        line = re.sub(r"^#+\s*", "", line)
        line = re.sub(r"^\s*[-*]\s+", "", line)
        line = re.sub(r"^\s*\d+\.\s+", "", line)
        line = line.replace("**", "").replace("`", "")
        if re.match(r"^\s*(---|<.*>)\s*$", line):
            line = ""
        out.append(line.rstrip())
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    return title, body


def save(out, name, title, body):
    with open(f"{out}/{name}.txt", "w", encoding="utf-8") as f:
        f.write(title + "\n\n" + body.strip() + "\n")


def main(root, out):
    os.makedirs(out, exist_ok=True)
    save(out, "A-orig", *a_orig())
    save(out, "B-orig", *b_orig())
    save(out, "C-orig", *c_orig())
    d = [p for p in glob.glob(f"{root}/10-08-*/article.md") if "-08-湯だまり" in p][0]
    save(out, "D-orig", *md2txt(open(d, encoding="utf-8").read()))
    for p in glob.glob(f"{root}/10-12-*/assets/rewrites/[A-D]-*.md"):
        save(out, f"{os.path.basename(p)[0]}-rewrite", *md2txt(open(p, encoding="utf-8").read()))


if __name__ == "__main__":
    main(*sys.argv[1:3])
