"""作った声を音声認識で文字に戻し、台本の読みと比べる(#98)。#132 でも、へんロボの声にそのまま使う。

台本の ttsText と、聞き取った文字を、どちらもカタカナの読みに直して比べる。
似ている割合が低い行を、聞き直す候補として出す。

#132 で、書き起こしを「ひらがな」で出させる形に変えた。
前は、聞き取った文字にも読みの表(tts-readings.tsv)をかけていた。この形では、表そのものの誤り
(「10のAI」を「とお」と書いた)が、台本と書き起こしの両方に同じようにかかり、一致と出てしまった。
今は、Whisper にひらがなの例文を渡して、読みをかなで書かせる。読みの表は、台本の側にしかかけない。
漢字のまま書き起こされた語は、実際の読みが分からない。その語は、出力の「聞き取り」の列を人が見る。

書き起こしは、2つの文と比べる。
- 声に渡した文(ttsText): 低ければ、声が読み違えている
- 台本の元の文(text): 低ければ、読みの表の値が誤っているかもしれない。元の文の読みは pyopenjtalk の推定なので、
  外れと出ても誤りとは限らない。人が「聞き取り」の列を見て決める
長い文では1語の違いが割合に響かない(「10のAI」の行は、元の文との割合が0.94だった)。
そのため、違う箇所を「台本→聞き取り」の形で列に書き出す。割合だけでなく、この列を上から見る。

使い方: ~/.venvs/tried-asr/bin/python listen_check.py <voice フォルダ> [しきい値 0.85]
台本の側は、lines.json の ttsText(読みの表をかけたあとの文)を使う。
出力: <voice フォルダ>/listen-check.tsv
"""
import difflib
import json
import re
import sys

import mlx_whisper
import pyopenjtalk

MODEL = "mlx-community/whisper-large-v3-turbo"
# ひらがなで書き起こさせるための例文(Whisper は、例文の書き方にならう)
KANA_PROMPT = "きょうは、ずめんの はなしを します。わたしは、ひらがなだけで かきます。"


def kana(t):
    t = re.sub(r"[、。,.!?！？…「」『』()（）\s]", "", t)
    return re.sub(r"[’、。？！]", "", pyopenjtalk.g2p(t, kana=True))


def diff(a, b):
    """読みの違う箇所を「台本→聞き取り」の形で並べる。似ている割合では、長い文の1語の違いが埋もれるため。"""
    ops = difflib.SequenceMatcher(None, a, b).get_opcodes()
    return " ".join(f"{a[i1:i2] or '∅'}→{b[j1:j2] or '∅'}" for op, i1, i2, j1, j2 in ops if op != "equal")


def main():
    out = sys.argv[1]
    th = float(sys.argv[2]) if len(sys.argv) > 2 else 0.85
    scenes = json.load(open(f"{out}/lines.json"))
    rows = []
    for sc in scenes:
        for ln in sc["lines"]:
            r = mlx_whisper.transcribe(f"{out}/{ln['file']}", path_or_hf_repo=MODEL, language="ja",
                                       initial_prompt=KANA_PROMPT)
            heard = r["text"].strip()
            a, t, b = kana(ln["ttsText"]), kana(ln["text"]), kana(heard)
            ratio = difflib.SequenceMatcher(None, a, b).ratio()
            ratio_text = difflib.SequenceMatcher(None, t, b).ratio()
            rows.append((ratio, ratio_text, ln["file"], ln["ttsText"], heard, diff(a, b), diff(t, b)))
            print(f"{ratio:.2f} {ratio_text:.2f}", ln["file"], heard, flush=True)
    with open(f"{out}/listen-check.tsv", "w") as f:
        f.write("声に渡した文と\t元の文と\tファイル\t声に渡した文\t聞き取り\t声に渡した文との違い\t元の文との違い\n")
        for r in sorted(rows, key=lambda r: min(r[0], r[1])):
            f.write("\t".join([f"{r[0]:.2f}", f"{r[1]:.2f}", *r[2:]]) + "\n")
    low = [r for r in rows if r[0] < th]
    low_text = [r for r in rows if r[1] < th]
    print("lines", len(rows), "声の読み違いの候補", len(low), "読みの表の誤りの候補", len(low_text))


if __name__ == "__main__":
    main()
