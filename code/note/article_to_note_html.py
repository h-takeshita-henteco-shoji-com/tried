"""article.md を、note のエディタに貼り付ける HTML に変換する。

使い方:
    python3 code/note/article_to_note_html.py <article.md のパス>

出力:
    1行目にタイトル、2行目に本文の HTML を JSON 文字列で出す。
    本文は chrome-devtools MCP の evaluate_script で、エディタ(.ProseMirror)に
    paste イベントとして渡す(手順は README の「noteの公開手順」)。

変換の決まり(前回までの公開記事の形に合わせた):
    - 1行目の `# ` はタイトルとして本文から外す
    - `## ` は h2
    - 空行で区切った塊を1つの段落にし、塊の中の改行は <br> にする
    - `> ` は引用
    - `**太字**` は strong、`*斜体*` は記号を外して地の文にする
    - URL はリンクにする
    - 画像の行 `![...](...)` は、目印の段落 [[FIG1]]、[[FIG2]]… に置き換える。
      画像は貼り付けた後に、目印の段落へ1枚ずつアップロードする
"""
import html
import json
import re
import sys


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"(https://\S+)", r'<a href="\1">\1</a>', text)
    return text


def convert(markdown):
    lines = markdown.split("\n")
    title = lines[0].lstrip("# ").strip()
    blocks, cur = [], []
    for line in lines[1:]:
        if line.strip() == "":
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append(line)
    if cur:
        blocks.append(cur)

    out, figs = [], 0
    for b in blocks:
        if b[0].startswith("## "):
            out.append(f"<h2>{inline(b[0][3:])}</h2>")
        elif b[0].startswith("!["):
            figs += 1
            out.append(f"<p>[[FIG{figs}]]</p>")
        elif b[0].startswith("> "):
            out.append("<blockquote><p>" + "<br>".join(inline(x[2:]) for x in b) + "</p></blockquote>")
        else:
            out.append("<p>" + "<br>".join(inline(x) for x in b) + "</p>")
    return title, "".join(out)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        title, body = convert(f.read())
    print(title)
    print(json.dumps(body, ensure_ascii=False))
