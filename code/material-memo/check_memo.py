"""生成した文章を素材メモと照合し、抜けた項目と足された主張を出す。

AI(Claude Opus 5.5)に、毎回新しい会話で照合させる。判定の基準は generation-conditions.md の「生成した後の確かめ」。
使い方: python check_memo.py <assets_dir> <文章.md>...
  assets_dir: material-memo.md のあるフォルダ
出力: 各文章と同じ場所に <名前>.check.json。標準出力に1行ずつ要約
"""
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "yardstick"))
from label import claude  # noqa: E402

MODEL = "claude-opus-5-5"
PROMPT = """ツールは一切使わないでください。
次の「文章」が、「素材メモ」の内容だけで書かれているかを照合してください。

判定の基準:
- 抜け: 素材メモの項目のうち、文章に内容が出てこないもの。言い回しが違っても、内容が出ていれば使ったとみなす。項目の中の一部(「/」で区切った要素)だけが抜けた場合も、抜けとして要素を書く
- 足し: 素材メモにない事実や主張。次は足しに数えない
  - 素材メモの事実や主張の言い換え、要約、繰り返し
  - 素材メモの主張を比喩で言い換えたもの(例: 「小さな火でもよい」)
  - 筆者の感情や語りのつなぎ(「私はそう思う」「話は変わるが」など)
- 足しに数えるもの: 比喩が新しい主張を生んだもの(例: 「消さずにいた者だけが、のちに大きな仕事を手にする」)、素材メモにない人物、逸話、科学の知識、数字
- 足しかどうか迷うものは、「迷い」に入れる

出力は次の JSON だけにしてください。
{{"missing": [{{"id": "項目番号", "what": "抜けた内容"}}], "added": [{{"quote": "文章からの抜き出し", "why": "足しと判断した理由"}}], "unsure": [{{"quote": "文章からの抜き出し", "why": "迷った理由"}}]}}

素材メモ:
{memo}

文章:
{text}
"""


def check(memo, path):
    text = open(path, encoding="utf-8").read()
    out = claude(PROMPT.format(memo=memo, text=text), MODEL)
    result = json.loads(re.search(r"\{.*\}", out, re.S).group(0))
    json.dump(result, open(path[:-3] + ".check.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return path, result


def main():
    memo = open(os.path.join(sys.argv[1], "material-memo.md"), encoding="utf-8").read()
    memo = memo[memo.index("## 人物と場面"):]
    with ThreadPoolExecutor(6) as ex:
        for path, r in ex.map(lambda p: check(memo, p), sys.argv[2:]):
            print(f"{path}\tmissing={len(r['missing'])}\tadded={len(r['added'])}\tunsure={len(r['unsure'])}")


if __name__ == "__main__":
    main()
