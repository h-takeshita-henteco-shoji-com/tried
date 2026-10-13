"""素材メモから、共通条件に従って文章を1本生成し、分量と形式を確かめる。

素材メモの項目は seed で並べ替え、番号と分類を外して渡す。並びが構成を縛らないようにするため。
claude -p は yardstick の claude() を使う(空のフォルダから呼び、設定とツールを読ませない)。
使い方: python generate.py <assets_dir> <out_dir> <seed> [指示ファイル]
  assets_dir: material-memo.md と generation-conditions.md のあるフォルダ
  指示ファイル: 条件ごとの書き方の指示。省略すると指示なし
出力: <out_dir>/seed<seed>.prompt.txt、.md(生成文)、.json(seed、モデル、並び、確認の結果)
"""
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "yardstick"))
from label import claude  # noqa: E402

MODEL = "claude-sonnet-5-5"
MIN_CHARS, MAX_CHARS = 990, 1210


def memo_items(path):
    text = open(path, encoding="utf-8").read()
    return re.findall(r"^- ([PFC]\d+)\. (.+)$", text, re.M)


def common_prompt(path):
    text = open(path, encoding="utf-8").read()
    return re.search(r"## 共通の指示文.*?```\n(.*?)```", text, re.S).group(1)


def build(assets, seed, style=""):
    items = memo_items(os.path.join(assets, "material-memo.md"))
    order = items[:]
    random.Random(seed).shuffle(order)
    memo = "\n".join(f"- {body}" for _, body in order)
    prompt = common_prompt(os.path.join(assets, "generation-conditions.md"))
    prompt = prompt.replace("<条件ごとの書き方の指示>", style.strip())
    prompt = re.sub(r"\n{3,}", "\n\n", prompt)
    prompt = prompt.replace("<素材メモの項目。並びは seed で変え、番号と分類は外す>", memo)
    return prompt, [i for i, _ in order]


def check(text):
    lines = [l for l in text.strip().split("\n") if l.strip()]
    body = re.sub(r"\s", "", "".join(lines[1:]))
    return {
        "title": lines[0],
        "chars": len(body),
        "paragraphs": len(lines) - 1,
        "in_range": MIN_CHARS <= len(body) <= MAX_CHARS,
        "headings": sum(l.lstrip().startswith("#") for l in lines),
        "bullets": sum(bool(re.match(r"\s*([-*・]|\d+[.)])\s", l)) for l in lines),
        "bold": text.count("**"),
        "blockquotes": sum(l.lstrip().startswith(">") for l in lines),
    }


def main():
    assets, out, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
    style = open(sys.argv[4], encoding="utf-8").read() if len(sys.argv) > 4 else ""
    prompt, order = build(assets, seed, style)
    text = claude(prompt, MODEL)
    os.makedirs(out, exist_ok=True)
    base = os.path.join(out, f"seed{seed}")
    open(base + ".prompt.txt", "w", encoding="utf-8").write(prompt)
    open(base + ".md", "w", encoding="utf-8").write(text.strip() + "\n")
    result = {"seed": seed, "model": MODEL, "order": order, **check(text)}
    json.dump(result, open(base + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 本文は表示しない(読む前の状態を保つため)
    print(json.dumps({k: v for k, v in result.items() if k != "title"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
