"""article.md を、note のエディタに貼り付ける HTML に変換する。

使い方:
    python3 code/note/article_to_note_html.py <article.md のパス>

出力:
    1行目にタイトル、2行目に本文の HTML を JSON 文字列で出す。
    本文は chrome-devtools MCP の evaluate_script で、エディタ(.ProseMirror)に
    paste イベントとして渡す(手順は README の「noteの公開手順」)。

変換の決まり(前回までの公開記事の形に合わせた):
    - 1行目の `# ` はタイトルとして本文から外す
    - `## ` は h2、`### ` は h3(note の小見出し)
    - 空行で区切った塊を1つの段落にし、塊の中の改行は <br> にする
    - `> ` は引用
    - `**太字**` は strong、`*斜体*` は記号を外して地の文にする
    - `[文字](URL)` は文字にリンクを張る。それ以外の URL はそのままリンクにする
    - ``` で囲んだ塊はコードブロック(pre)にする
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
    links = []

    def keep(m):
        links.append(f'<a href="{m.group(2)}">{m.group(1)}</a>')
        return f"\0{len(links) - 1}\0"

    text = re.sub(r"\[([^\]]+)\]\((https://[^)\s]+)\)", keep, text)
    text = re.sub(r"(https://[^\s\0]+)", r'<a href="\1">\1</a>', text)
    return re.sub(r"\0(\d+)\0", lambda m: links[int(m.group(1))], text)


def convert(markdown):
    lines = markdown.split("\n")
    title = lines[0].lstrip("# ").strip()
    blocks, cur = [], []
    in_code = False
    for line in lines[1:]:
        if line.startswith("```"):
            if in_code:
                cur.append(line)
                blocks.append(cur)
                cur = []
            else:
                if cur:
                    blocks.append(cur)
                cur = [line]
            in_code = not in_code
            continue
        if in_code:
            cur.append(line)
        elif line.strip() == "":
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append(line)
    if cur:
        blocks.append(cur)

    out, figs = [], 0
    for b in blocks:
        if b[0].startswith("```"):
            code = "\n".join(b[1:-1] if b[-1].startswith("```") else b[1:])
            out.append(f"<pre><code>{html.escape(code, quote=False)}</code></pre>")
        elif b[0].startswith("### "):
            out.append(f"<h3>{inline(b[0][4:])}</h3>")
        elif b[0].startswith("## "):
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
